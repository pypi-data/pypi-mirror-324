from typing import TYPE_CHECKING

from pypika.terms import ValueWrapper
from pypika import Column, MSSQLQuery, Table

if TYPE_CHECKING:
    from pypika.terms import Term
    from pypika.queries import CreateQueryBuilder


def compile_source(source: str) -> "Term":
    return ValueWrapper(source).as_("source")


SOURCE_DS2 = compile_source("qa-ds2")
SOURCE_RKD = compile_source("qa-rkd")
SOURCE_IBES = compile_source("qa-ibes")


def create_table(tablename: "str", *columns: "Column") -> tuple[Table, "CreateQueryBuilder"]:
    table = Table(tablename)
    return table, MSSQLQuery.create_table(table).columns(*columns)
