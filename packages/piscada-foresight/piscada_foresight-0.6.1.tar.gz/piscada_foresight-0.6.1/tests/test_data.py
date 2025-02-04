from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pytest

from src.piscada_foresight.data import get_values
from src.piscada_foresight.queries_templates.query_manager import QueryManager
from tests.utils.fixtures import (
    aggregated_timeseries_response,
    mock_query_manager,
    no_values_response,
    raw_timeseries_response,
)
from tests.utils.test_utils import compare_dataframes, load_dataframe, save_dataframe


def test_get_values_success(mock_query_manager, raw_timeseries_response):
    """
    Tests that get_values successfully returns a DataFrame with expected data.
    """
    mock_query_manager.run_query.return_value = raw_timeseries_response
    df = get_values(
        mock_query_manager,
        entity_ids=[
            "brick:Supply_Air_Temperature_Sensor:00000000-0000-0000-0000-000000000001",
            "brick:Effective_Supply_Air_Temperature_Setpoint:00000000-0000-0000-0000-000000000002",
        ],
        start=datetime.now(tz=timezone.utc),
    )
    assert len(df) == 8  # noqa: PLR2004
    assert pd.isna(df["360001 Temperature"].iloc[0])


def test_get_values_missing_values(mock_query_manager, no_values_response):
    """
    Tests that get_values raises a RuntimeError when no data is available.
    """
    # No data for the tags at the specified time range
    mock_query_manager.run_query.return_value = no_values_response
    with pytest.raises(RuntimeError):
        get_values(
            mock_query_manager,
            entity_ids=[
                "brick:Supply_Air_Temperature_Sensor:00000000-0000-0000-0000-000000000001",
                "brick:Effective_Supply_Air_Temperature_Setpoint:00000000-0000-0000-0000-000000000002",
            ],
            start=datetime(1993, 2, 12, tzinfo=timezone.utc),
            end=datetime(1993, 2, 13, tzinfo=timezone.utc),
        )


def test_get_values_start_later_than_end(mock_query_manager):
    """
    Tests that get_values raises a ValueError when start > end.
    """
    with pytest.raises(
        ValueError,
        match="The 'start' datetime cannot be later than the 'end' datetime.",
    ):
        get_values(
            query_manager=mock_query_manager,
            entity_ids=["entity1", "entity2"],
            start=datetime(2023, 2, 1, tzinfo=timezone.utc),
            end=datetime(2023, 1, 31, tzinfo=timezone.utc),
        )


def test_get_values_start_or_end_not_timezone_aware(mock_query_manager):
    """
    Tests that get_values raises a ValueError if start or end is not timezone-aware.
    """
    with pytest.raises(ValueError, match="The start parameter must be timezone aware."):
        get_values(
            query_manager=mock_query_manager,
            entity_ids=["entity1", "entity2"],
            start=datetime(2023, 2, 1),
            end=datetime(2023, 1, 31, tzinfo=timezone.utc),
        )
        get_values(
            query_manager=mock_query_manager,
            entity_ids=["entity1", "entity2"],
            start=datetime(2023, 2, 1),
            end=datetime(2023, 1, 31),
        )
    with pytest.raises(ValueError, match="The end parameter must be timezone aware."):
        get_values(
            query_manager=mock_query_manager,
            entity_ids=["entity1", "entity2"],
            start=datetime(2023, 2, 1, tzinfo=timezone.utc),
            end=datetime(2023, 1, 31),
        )


def test_get_values_aggregated_success(
    mock_query_manager, aggregated_timeseries_response
):
    """
    Checks that get_values successfully retrieves and parses aggregated data
    when valid aggregation functions are provided.
    """
    # Mock the QueryManager
    mock_query_manager.run_query.return_value = aggregated_timeseries_response

    df = get_values(
        query_manager=mock_query_manager,
        entity_ids=[
            "brick:Supply_Air_Temperature_Sensor:00000000-0000-0000-0000-000000000001",
            "brick:Effective_Supply_Air_Temperature_Setpoint:00000000-0000-0000-0000-000000000002",
        ],
        start=datetime(2025, 1, 14, 9, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 14, 11, 0, 0, tzinfo=timezone.utc),
        interval="1h",
        aggregation_functions=["min", "max", "avg", "count", "last"],
    )
    # Assert the DataFrame is not empty
    assert not df.empty, "DataFrame should not be empty for valid aggregated data"

    # Example: Check if specific columns exist in the DataFrame
    expected_columns = [
        "360001 Temperature|min",
        "360001 Temperature|max",
        "360001 Temperature|avg",
        "360001 Temperature|count",
        "360001 Temperature|last",
    ]
    for col in expected_columns:
        assert col in df.columns, f"Missing expected column: {col}"


def test_get_values_aggregated_invalid_aggregator(mock_query_manager):
    """
    Verifies that ValueError is raised if any aggregator is invalid.
    """

    with pytest.raises(ValueError, match="Invalid aggregation function provided"):
        get_values(
            query_manager=mock_query_manager,
            entity_ids=["entityId_0"],
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
            interval="1d",
            aggregation_functions=["min", "max", "foo"],  # 'foo' is not valid
        )


def test_get_values_aggregated_multiple_aggregators(
    mock_query_manager, aggregated_timeseries_response
):
    """
    Ensures that multiple valid aggregation functions can be handled correctly.
    """
    mock_query_manager.run_query.return_value = aggregated_timeseries_response

    df = get_values(
        query_manager=mock_query_manager,
        entity_ids=["entityId_0", "entityId_1"],
        start=datetime(2025, 1, 14, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, tzinfo=timezone.utc),
        interval="1h",
        aggregation_functions=["min", "max", "avg"],
    )

    assert not df.empty
    for func in ["min", "max", "avg"]:
        col_0 = f"360001 Temperature|{func}"
        col_1 = f"360002 Temperature Setpoint|{func}"
        assert col_0 in df.columns, f"Missing {col_0} aggregator column"
        assert col_1 in df.columns, f"Missing {col_1} aggregator column"


def test_get_values_aggregated_interval_none_uses_default(
    mock_query_manager, aggregated_timeseries_response
):
    """
    If interval=None is passed, ensure get_values defaults to e.g. '1d'.
    Here, we just confirm no error is raised and that the query can run.
    Optionally, check that the client sees 'interval': '1d'.
    """
    mock_query_manager.run_query.return_value = aggregated_timeseries_response

    df = get_values(
        query_manager=mock_query_manager,
        entity_ids=["entityId_0"],
        start=datetime(2025, 1, 14, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, tzinfo=timezone.utc),
        interval=None,
        aggregation_functions=["min", "max", "avg", "count", "last"],
    )
    assert not df.empty, "Should return aggregated data with default interval."


def test_get_values_aggregated_start_later_than_end_raises_error(mock_query_manager):
    """
    Ensures ValueError is raised when start > end.
    """

    with pytest.raises(
        ValueError,
        match="The 'start' datetime cannot be later than the 'end' datetime.",
    ):
        get_values(
            query_manager=mock_query_manager,
            entity_ids=["entityId_0"],
            start=datetime(2025, 1, 15, tzinfo=timezone.utc),
            end=datetime(2025, 1, 14, tzinfo=timezone.utc),
            aggregation_functions=["min"],
        )


def test_get_values_aggregated_start_or_end_not_timezone_aware_raises_error(
    mock_query_manager,
):
    """
    Checks that ValueError is raised if start or end is not timezone aware.
    """

    with pytest.raises(ValueError, match="The start parameter must be timezone aware."):
        get_values(
            query_manager=mock_query_manager,
            entity_ids=["entityId_0"],
            start=datetime(2025, 1, 14),  # no tzinfo
            end=datetime(2025, 1, 15, tzinfo=timezone.utc),
            aggregation_functions=["min"],
        )

    with pytest.raises(ValueError, match="The end parameter must be timezone aware."):
        get_values(
            query_manager=mock_query_manager,
            entity_ids=["entityId_0"],
            start=datetime(2025, 1, 14, tzinfo=timezone.utc),
            end=datetime(2025, 1, 15),  # no tzinfo
            aggregation_functions=["min"],
        )
