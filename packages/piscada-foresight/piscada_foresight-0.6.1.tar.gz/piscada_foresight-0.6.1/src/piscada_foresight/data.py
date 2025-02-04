"""Access to Foresight timeseries data."""

import logging
import re
from datetime import datetime, timezone
from json import loads
from typing import List
from uuid import UUID

from pandas import DataFrame, to_datetime

from src.piscada_foresight.parser_graphql_to_df.TimeSeries.timeseries_response_parser import (
    TimeseriesResponseParser,
)
from src.piscada_foresight.queries_templates.query_manager import QueryManager

log = logging.getLogger(__name__)


def get_value(
    query_manager: QueryManager, entity_id: UUID, moment: datetime | None = None
) -> float:
    """
    Retrieve the latest value of a `foresight:Datapoint` entity before a point in time (default=now).
    """
    if not moment:
        moment = datetime.now(tz=timezone.utc)

    variables = {"entityId": entity_id, "eventTime": moment.isoformat()}
    response = query_manager.run_query("get_latest_value", query_variables=variables)

    try:
        return float(response["entity"]["trait"]["quantity"]["value"]["value"])
    except KeyError:
        raise RuntimeError("Cloud not retrieve value.")
    except ValueError as exc:
        val_str = response["entity"]["trait"]["quantity"]["value"]["value"]
        raise RuntimeError(f"Could not parse value {val_str}") from exc


def get_raw_timeseries(
    query_manager: QueryManager,
    entity_ids: List[str],
    start: datetime,
    end: datetime | None = None,
) -> DataFrame:
    """
    Retrieve values of `foresight:Datapoint` entities for a time range (raw timeseries).
    """
    if end is None:
        end = datetime.now(tz=timezone.utc)
    if start.tzinfo is None or start.tzinfo.utcoffset(start) is None:
        raise ValueError("The start parameter must be timezone aware.")
    if end.tzinfo is None or end.tzinfo.utcoffset(end) is None:
        raise ValueError("The end parameter must be timezone aware.")
    if start > end:
        raise ValueError(
            "The 'start' datetime cannot be later than the 'end' datetime."
        )

    entity_variables = {
        f"entityId_{i}": entity_id for i, entity_id in enumerate(entity_ids)
    }
    variables = {
        **entity_variables,
        "startEventTime": start.isoformat(),
        "endEventTime": end.isoformat(),
    }

    response = query_manager.run_query(
        "get_raw_values",
        jinja_variables=list(entity_variables.keys()),
        query_variables=variables,
    )

    parser = TimeseriesResponseParser()
    df = parser.parse(response, entity_variables, start, end, query_type="raw")
    return df


def get_aggregated_timeseries(  # noqa: PLR0913
    query_manager: QueryManager,
    entity_ids: list[str],
    start: datetime,
    end: datetime | None = None,
    interval: str = "",
    aggregation_functions: List[str] | None = None,
) -> DataFrame:
    """
    Retrieve aggregated values of `foresight:Datapoint` entities for a given time range.
    """
    if end is None:
        end = datetime.now(tz=timezone.utc)
    if start.tzinfo is None or start.tzinfo.utcoffset(start) is None:
        raise ValueError("The start parameter must be timezone aware.")
    if end.tzinfo is None or end.tzinfo.utcoffset(end) is None:
        raise ValueError("The end parameter must be timezone aware.")
    if start > end:
        raise ValueError(
            "The 'start' datetime cannot be later than the 'end' datetime."
        )

    if aggregation_functions is None:
        aggregation_functions = []

    valid_aggregators = {"min", "max", "avg", "count", "last"}
    if not all(func in valid_aggregators for func in aggregation_functions):
        raise ValueError(
            f"Invalid aggregation function provided. "
            f"Only the following are allowed: {valid_aggregators}"
        )

    entity_variables = {
        f"entityId_{i}": entity_id for i, entity_id in enumerate(entity_ids)
    }

    query_variables = {
        **entity_variables,
        "startEventTime": start.isoformat(),
        "endEventTime": end.isoformat(),
        "interval": interval,
        "aggregationFunctions": aggregation_functions,
    }

    response = query_manager.run_query(
        "get_aggregated_values",
        jinja_variables=list(entity_variables.keys()),
        query_variables=query_variables,
    )
    parser = TimeseriesResponseParser()
    df = parser.parse(response, entity_variables, start, end, query_type="aggregated")
    return df


def get_values(  # noqa: PLR0913
    query_manager: QueryManager,
    entity_ids: List[str],
    start: datetime,
    end: datetime | None = None,
    interval: str = "",
    aggregation_functions: List[str] | None = None,
) -> DataFrame:
    """
    Dispatches either to raw or aggregated timeseries based on whether `aggregation_functions` is set.
    """
    if not aggregation_functions:
        return get_raw_timeseries(query_manager, entity_ids, start, end)
    else:
        return get_aggregated_timeseries(
            query_manager, entity_ids, start, end, interval, aggregation_functions
        )


def get_all_values(text: str) -> List[DataFrame]:
    """
    Extract all pairs of id, name, and values from a GraphQL query response string
    and return them as a list of DataFrames.
    """
    values_regex = re.compile(
        r"'id'\:\s*'([\:\w\s\-_]*?)',\s*'name'\:\s*'([\w\s\-_]*?)',\s*'trait':\s*{'quantity'\:\s*\{'values'\:\s*\[([\{'\w\:\-\s\.\},]*)"
    )
    dfs = []
    for match in values_regex.findall(text):
        eid = match[0].split(":")[-1]
        name = match[1]
        # Convert single quotes to double quotes for JSON parsing
        values_str = f"[{match[2]}]".replace("'", '"')

        parsed_values = loads(values_str)
        data = [
            {"ts": item["eventTime"], f"{name}|{eid}": float(item["value"])}
            for item in parsed_values
        ]
        df = DataFrame(data).set_index("ts")
        df.index = to_datetime(df.index, format="ISO8601")
        dfs.append(df)

    return dfs
