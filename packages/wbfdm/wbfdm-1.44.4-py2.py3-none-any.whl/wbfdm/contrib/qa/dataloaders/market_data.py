from contextlib import suppress
from functools import reduce
from itertools import batched
from datetime import date
from enum import Enum
from typing import Iterator
import pypika as pk
from pypika import Column, MSSQLQuery, functions as fn
from pypika.enums import SqlTypes, Order
from pypika.terms import ValueWrapper, LiteralValue

from django.db import ProgrammingError, connections
from wbcore.contrib.dataloader.dataloaders import Dataloader
from wbcore.contrib.dataloader.utils import dictfetchall
from wbfdm.dataloaders.protocols import MarketDataProtocol
from wbfdm.contrib.qa.dataloaders.utils import create_table
from wbfdm.dataloaders.types import MarketDataDict
from wbfdm.enums import Frequency, MarketData


class DS2MarketData(Enum):
    OPEN = ("Open_", 1)
    CLOSE = ("Close_", 1)
    HIGH = ("High", 1)
    LOW = ("Low", 1)
    BID = ("Bid", 1)
    ASK = ("Ask", 1)
    VWAP = ("VWAP", 1)
    VOLUME = ("Volume", 1)
    MARKET_CAPITALIZATION = ("ConsolMktVal", 1_000_000)
    SHARES_OUTSTANDING = ("ConsolNumShrs", 1_000)


class DatastreamMarketDataDataloader(MarketDataProtocol, Dataloader):
    def market_data(
        self,
        values: list[MarketData] | None = [MarketData.CLOSE],
        from_date: date | None = None,
        to_date: date | None = None,
        exact_date: date | None = None,
        frequency: Frequency = Frequency.DAILY,
        target_currency: str | None = None,
        **kwargs,
    ) -> Iterator[MarketDataDict]:
        """Get market data for instruments.

        Args:
            queryset (QuerySet["Instrument"]): The queryset of instruments.
            values (list[MarketData]): List of values to include in the results.
            from_date (date | None): The starting date for filtering prices. Defaults to None.
            to_date (date | None): The ending date for filtering prices. Defaults to None.
            frequency (Frequency): The frequency of the requested data

        Returns:
            Iterator[MarketDataDict]: An iterator of dictionaries conforming to the DailyValuationDict.
        """

        lookup = {
            f"{k[0]},{k[1]}": v for k, v in self.entities.values_list("dl_parameters__market_data__parameters", "id")
        }
        value_mapping = [(DS2MarketData[x.name].value, x.value) for x in values or []]

        # Define tables
        pricing = pk.Table("vw_DS2Pricing")
        market_val = pk.Table("DS2MktVal")
        fx_code = pk.Table("DS2FxCode")
        fx = pk.Table("DS2FxRate")

        mapping, create_mapping_table = create_table(
            "#ds2infoexchcode", Column("InfoCode", SqlTypes.INTEGER), Column("ExchIntCode", SqlTypes.INTEGER)
        )

        # Base query to get data we always need unconditionally
        query = (
            pk.MSSQLQuery.from_(pricing)
            .select(
                fn.Concat(pricing.InfoCode, ",", pricing.ExchIntCode).as_("external_identifier"),
                fn.Concat(
                    pricing.InfoCode, ",", pricing.ExchIntCode, "_", fn.Cast(pricing.MarketDate, SqlTypes.DATE)
                ).as_("id"),
                fn.Cast(pricing.MarketDate, SqlTypes.DATE).as_("valuation_date"),
                ValueWrapper("qa-ds2").as_("source"),
            )
            .left_join(market_val)
            .on((pricing.InfoCode == market_val.InfoCode) & (pricing.MarketDate == market_val.ValDate))
            # We join on _codes, which removes all instruments not in _codes - implicit where
            .join(mapping)
            .on((pricing.InfoCode == mapping.InfoCode) & (pricing.ExchIntCode == mapping.ExchIntCode))
            .where(pricing.AdjType == 2)
            .orderby(pricing.MarketDate, order=Order.desc)
        )

        # If we need to convert to a target currency, we need the fx rate table and multiply all values with the fx rate
        if target_currency:
            query = (
                query.select(
                    ValueWrapper(target_currency).as_("currency"),
                    *[
                        (LiteralValue(value[0][0]) * fn.Coalesce(fx.midrate, 1) * value[0][1]).as_(value[1])
                        for value in value_mapping
                    ],
                )
                .left_join(fx_code)
                .on(
                    (fx_code.FromCurrCode == target_currency)
                    & (fx_code.ToCurrCode == pricing.Currency)
                    & (fx_code.RateTypeCode == "SPOT")
                )
                .left_join(fx)
                .on((fx_code.ExRateIntCode == fx.ExRateIntCode) & (fx.ExRateDate == pricing.MarketDate))
            )
        else:
            query = query.select(
                pricing.Currency.as_("currency"),
                *[(LiteralValue(value[0][0]) * value[0][1]).as_(value[1]) for value in value_mapping],
            )

        # Add conditional where clauses
        if from_date:
            query = query.where(pricing.MarketDate >= from_date)

        if to_date:
            query = query.where(pricing.MarketDate <= to_date)

        if exact_date:
            query = query.where(pricing.MarketDate == exact_date)

        with connections["qa"].cursor() as cursor:
            with suppress(ProgrammingError):
                cursor.execute(create_mapping_table.get_sql())
                for batch in batched(
                    self.entities.values_list("dl_parameters__market_data__parameters", flat=True), 1000
                ):
                    cursor.execute(reduce(lambda x, y: x.insert(y), batch, MSSQLQuery.into(mapping)).get_sql())

            cursor.execute(query.get_sql())

            for row in dictfetchall(cursor, MarketDataDict):
                row["instrument_id"] = lookup[row["external_identifier"]]
                yield row

            cursor.execute(MSSQLQuery.drop_table(mapping).get_sql())
