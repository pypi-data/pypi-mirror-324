from unittest.mock import Mock

import pytest

from src.piscada_foresight.parser_graphql_to_df.TimeSeries.timeseries_response_parser import (
    TimeseriesResponseParser,
)
from tests.utils.test_utils import load_file_content


@pytest.fixture
def parser():
    return TimeseriesResponseParser()


# ---- Fixtures ----
@pytest.fixture
def mock_query_manager():
    """
    Provides a mock implementation of the QueryManager.
    """
    return Mock()


@pytest.fixture
def aggregated_timeseries_response():
    return load_file_content("responses/aggregated_timeseries.json")


@pytest.fixture
def aggregated_one_empty_sublist_response():
    return load_file_content("responses/aggregated_one_empty_sublist.json")


@pytest.fixture
def aggregated_tag_missing():
    return load_file_content("responses/aggregated_tag_missing.json")


@pytest.fixture
def aggregated_empty_sublists():
    return load_file_content("responses/aggregated_empty_sublists.json")


# Fixtures
@pytest.fixture
def aggregated_no_values():
    return load_file_content("responses/aggregated_no_values.json")


@pytest.fixture
def raw_missing_values_tag_response():
    return load_file_content("responses/raw_missing_values_tag.json")


@pytest.fixture
def raw_timeseries_response():
    return load_file_content("responses/raw_timeseries.json")


@pytest.fixture
def no_values_response(raw_timeseries_response):
    response = raw_timeseries_response
    response["entityId_0"]["trait"]["quantity"]["values"] = []
    response["entityId_1"]["trait"]["quantity"]["values"] = []
    return response
