from typing import List, Optional

import pendulum
from fastapi import APIRouter, Query

from lacity_data_api.services.reports import run_report

router = APIRouter()

filter_regex = "^(\w+)([>=<]+)([\w-]+)$"  # noqa
dt = pendulum.today()


# TODO: add end of previous month filter.
# might be a problem with multiple default filters.
@router.get("")
async def get_report(
    field: Optional[List[str]] = Query(
        ["type_name", "created_date"],
        description="ex. created_date",
        regex="""(created_year|created_month|created_dow|created_hour|created_date|council_name|type_name|agency_name|source_name)"""  # noqa
    ),
    filter: Optional[List[str]] = Query(
        [
            f"created_date>={ dt.subtract(months=1).start_of('month').format('YYYY-MM-DD') }"  # noqa
        ],
        description="""
            Field then operator then value
            (ex. created_date>=2021-01-01 or council_name=Arleta
            """,
        regex=filter_regex
    )
):
    results = await run_report(field, filter)
    return results
