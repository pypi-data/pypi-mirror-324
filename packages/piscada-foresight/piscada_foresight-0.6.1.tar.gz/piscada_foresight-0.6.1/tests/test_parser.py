import logging
from datetime import datetime, timezone

import pytest
from pandas import DataFrame

from src.piscada_foresight.parser_graphql_to_df.TimeSeries.timeseries_response_parser import (
    TimeseriesResponseParser,
)
from tests.utils.fixtures import (
    aggregated_empty_sublists,
    aggregated_no_values,
    aggregated_one_empty_sublist_response,
    aggregated_tag_missing,
    aggregated_timeseries_response,
    mock_query_manager,
    raw_missing_values_tag_response,
    raw_timeseries_response,
)


def test_get_values_aggregated_missing_values(
    mock_query_manager, aggregated_no_values, caplog
):
    """
    Checks behavior when no aggregator data is available (empty values arrays).
    Ensure a warning is logged and an empty DataFrame is returned.
    """
    mock_query_manager.run_query.return_value = aggregated_no_values

    parser = TimeseriesResponseParser()

    entity_variables = {
        f"entityId_{i}": entity_id
        for i, entity_id in enumerate(["entityId_0", "entityId_1"])
    }

    with caplog.at_level("WARNING"):
        result = parser.parse(
            response=aggregated_no_values,
            entity_variables=entity_variables,
            start="2023-01-01",
            end="2023-01-02",
            query_type="aggregated",
        )

        # Check warning is logged
        assert "No data found for the requested time range" in caplog.text

        # Check result is an empty DataFrame
        assert isinstance(result, DataFrame)
        assert result.empty


@pytest.fixture
def parser():
    return TimeseriesResponseParser()


def test_parse_raw_values_success(parser, raw_timeseries_response):
    """
    Test parsing a valid 'raw' timeseries response.
    The response includes multiple eventTimes and numeric values.
    """
    entity_variables = {
        "entityId_0": "brick:Supply_Air_Temperature_Sensor:00000000-0000-0000-0000-000000000001",
        "entityId_1": "brick:Effective_Supply_Air_Temperature_Setpoint:00000000-0000-0000-0000-000000000002",
    }

    df = parser.parse(
        response=raw_timeseries_response,
        entity_variables=entity_variables,
        start=datetime(2025, 1, 14, 9, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 14, 11, 0, 0, tzinfo=timezone.utc),
        query_type="raw",
    )

    # We expect two columns, one per entity name
    assert isinstance(df, DataFrame)
    assert not df.empty, "DataFrame should not be empty for valid raw data"
    assert "360001 Temperature" in df.columns
    assert "360001 Temperature Setpoint" in df.columns

    # Check some expected values
    # (the parser forward-fills missing times by default, so you might see more rows than raw data)
    # Just confirm the first row has the expected value
    first_temp = df["360001 Temperature"].iloc[0]
    first_setpoint = df["360001 Temperature Setpoint"].iloc[0]
    assert (
        first_setpoint == 19.5 # noqa: PLR2004
    ), "Incorrect setpoint value in first row"


def test_parse_raw_values_missing_keys(parser, raw_missing_values_tag_response):
    """
    Ensures a RuntimeError is raised if required keys are missing from the raw response
    (e.g., 'quantity' or 'values').
    """
    # Missing 'values' key

    entity_variables = {"entityId_0": "fake_entity_id"}

    with pytest.raises(
        RuntimeError, match="Could not retrieve raw values for entity 'fake_entity_id'"
    ):
        parser.parse(
            response=raw_missing_values_tag_response,
            entity_variables=entity_variables,
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
            query_type="raw",
        )


def test_parse_raw_values_entity_none(parser):
    """
    If 'response[variable_name]' is None, a TypeError will occur when accessing subkeys,
    which should be turned into a RuntimeError by the parser.
    """
    response = {"entityId_0": None}  # This will cause a TypeError
    entity_variables = {"entityId_0": "fake_entity_id"}

    with pytest.raises(RuntimeError, match="Could not find entity 'fake_entity_id'"):
        parser.parse(
            response=response,
            entity_variables=entity_variables,
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
            query_type="raw",
        )


def test_parse_raw_values_no_entities(parser, caplog):
    """
    If the response is empty or if entity_variables is empty, we expect an empty DataFrame.
    """
    response = {}
    entity_variables = {}

    with caplog.at_level(logging.WARNING):
        df = parser.parse(
            response=response,
            entity_variables=entity_variables,
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
            query_type="raw",
        )
    assert (
        df.empty
    ), "Should return an empty DataFrame when no entities or data are present."


def test_parse_aggregated_values_success(parser, aggregated_timeseries_response):
    """
    Test parsing a valid 'aggregated' timeseries response.
    The response includes several aggregationFunctions for each entity.
    """

    entity_variables = {
        "entityId_0": "brick:Supply_Air_Temperature_Sensor:0000-0000-0000-0000-000000000001",
        "entityId_1": "brick:Effective_Supply_Air_Temperature_Setpoint:0000-0000-0000-0000-000000000002",
    }

    df = parser.parse(
        response=aggregated_timeseries_response,
        entity_variables=entity_variables,
        start=datetime(2025, 1, 14, 9, tzinfo=timezone.utc),
        end=datetime(2025, 1, 14, 11, tzinfo=timezone.utc),
        query_type="aggregated",
    )

    # We expect columns like "360001 Temperature|min", "360001 Temperature|max", etc.
    expected_cols_entity0 = [
        "360001 Temperature|min",
        "360001 Temperature|max",
        "360001 Temperature|avg",
        "360001 Temperature|count",
        "360001 Temperature|last",
    ]
    for col in expected_cols_entity0:
        assert col in df.columns

    expected_cols_entity1 = [
        "360002 Temperature Setpoint|min",
        "360002 Temperature Setpoint|max",
        "360002 Temperature Setpoint|avg",
        "360002 Temperature Setpoint|count",
        "360002 Temperature Setpoint|last",
    ]
    for col in expected_cols_entity1:
        assert col in df.columns

    # Check some values
    assert (
        df.loc["2025-01-14 09:59:59.786000+00:00", "360001 Temperature|min"] == 19.5 # noqa: PLR2004
    )
    assert (
        df.loc["2025-01-14 09:59:59.786000+00:00", "360002 Temperature Setpoint|last"]
        == 19.8 # noqa: PLR2004
    )


def test_parse_aggregated_values_missing_key(parser, aggregated_tag_missing):
    """
    Test that if the aggregated response is missing essential keys,
    a RuntimeError is raised.
    """
    entity_variables = {"entityId_0": "brick:Supply_Air_Temperature_Sensor:0000-0000"}

    with pytest.raises(
        RuntimeError,
        match="Could not retrieve aggregated values for entity 'brick:Supply_Air_Temperature_Sensor:0000-0000'",
    ):
        parser.parse(
            response=aggregated_tag_missing,
            entity_variables=entity_variables,
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
            query_type="aggregated",
        )


def test_parse_aggregated_values_all_empty(parser, aggregated_empty_sublists, caplog):
    """
    If every sublist in 'aggregatedTimeseries' is empty, we expect a warning and an empty DataFrame.
    """

    entity_variables = {"entityId_0": "brick:Supply_Air_Temperature_Sensor:0000-0000"}

    with caplog.at_level(logging.WARNING):
        df = parser.parse(
            response=aggregated_empty_sublists,
            entity_variables=entity_variables,
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
            query_type="aggregated",
        )

    assert (
        df.empty
    ), "Should return empty DataFrame if no aggregator sublists have data."
    assert "No data found for the requested time range" in caplog.text


def test_parse_aggregated_values_partial_empty(
    parser, aggregated_one_empty_sublist_response
):
    """
    If some sublists of 'aggregatedTimeseries' are empty and others have data,
    the parser should return only the non-empty columns.
    """
    entity_variables = {"entityId_0": "brick:Supply_Air_Temperature_Sensor:0000-0000"}

    df = parser.parse(
        response=aggregated_one_empty_sublist_response,
        entity_variables=entity_variables,
        start=datetime(2025, 1, 14, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, tzinfo=timezone.utc),
        query_type="aggregated",
    )
    assert (
        not df.empty
    ), "Should not be empty if at least one aggregator sublist has data"
    assert "360001 Temperature|max" in df.columns
    assert (
        "360001 Temperature|min" not in df.columns
    ), "Empty aggregator sublist shouldn't appear as a column"
    assert df.iloc[0, 0] == 19.7  # noqa: PLR2004


def test_parse_unknown_query_type(parser):
    """
    Passing an unknown query_type should raise ValueError.
    """
    with pytest.raises(ValueError, match="Unknown query_type: invalid_type"):
        parser.parse(
            response={},
            entity_variables={},
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
            query_type="invalid_type",
        )
