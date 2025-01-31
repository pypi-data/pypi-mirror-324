import pyarrow as pa
from pydantic import Field, field_validator, model_validator

from ..base import ResultBase
from ..context import DateRangeContext
from ..exttypes import ArrowTable

__all__ = (
    "ArrowResult",
    "ArrowDateRangeResult",
)


class ArrowResult(ResultBase):
    table: ArrowTable

    @field_validator("table", mode="before")
    def _from_dataframe(cls, v):
        if not isinstance(v, pa.Table):
            import polars as pl

            if isinstance(v, pl.DataFrame):
                return v.to_arrow()

            import pandas as pd

            if isinstance(v, pd.DataFrame):
                return pa.Table.from_pandas(v)
        return v


class ArrowDateRangeResult(ArrowResult):
    """Extension of ArrowResult for representing a table over a date range that can be divided by date,
    such that generation of any sub-range of dates gives the same results as the original table filtered for those dates.

    Use of this ResultType assumes the data satisfies the condition above!

    This is useful for representing the results of queries of daily data. Furthermore, because the identity of the column
    containing the underlying date is known, it can be used to partition the data for future queries and caching.
    With the generic ArrowResult there is no way to know which column might correspond to the dates in the date range.
    """

    date_col: str = Field("The column corresponding to the date of the record. It must align with the context dates.")
    context: DateRangeContext = Field(
        description="The context that generated the result. Validation will check that all the dates in the date_col are within the context range."
    )

    @model_validator(mode="after")
    def _validate_date_col(self):
        import pyarrow.compute

        if self.date_col not in self.table.column_names:
            raise ValueError("date_col must be a column in table")
        col_type = self.table.schema.field(self.date_col).type
        if not pa.types.is_date(col_type):
            raise ValueError(f"date_col must be of date type, not {col_type}")
        dates = self.table[self.date_col]
        if len(dates):
            min_date = pyarrow.compute.min(dates).as_py()
            max_date = pyarrow.compute.max(dates).as_py()
            start_date = self.context.start_date
            end_date = self.context.end_date
            if min_date < start_date:
                raise ValueError(f"The min date value ({min_date}) is smaller than the start date of the context ({start_date})")
            if max_date > end_date:
                raise ValueError(f"The max date value ({max_date}) is smaller than the end date of the context ({end_date})")
        return self
