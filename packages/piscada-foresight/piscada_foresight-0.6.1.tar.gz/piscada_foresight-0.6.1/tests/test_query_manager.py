import json

import pytest
from graphql import parse, print_ast

from src.piscada_foresight.queries_templates.query_manager import QueryManager
from tests.utils.test_utils import load_file_content


def test_singleton_behavior():
    """
    Ensure that QueryManager is a singleton.
    """
    # Create two instances with different domains
    qm1 = QueryManager(domain="domain1")
    qm2 = QueryManager(domain="domain2")

    assert (
        qm1 is qm2
    ), "QueryManager should return the same instance regardless of constructor args."


def test_load_queries_build_dict():
    """
    Test that _load_queries populates the _query_dict with discovered .j2 and .graphql files.
    """
    qm = QueryManager(domain="fake_domain")

    # Get the query dictionary
    qdict = qm.get_query_dict()

    # Expected values in the _query_dict
    expected_dict = {
        "get_aggregated_values": "graphql_queries/timeseries/get_aggregated_values.j2",
        "get_domains": "graphql_queries/domains/get_domains.graphql",
        "get_latest_value": "graphql_queries/timeseries/get_latest_value.j2",
        "get_raw_values": "graphql_queries/timeseries/get_raw_values.j2",
    }

    # Verify the actual query dictionary matches the expected values
    assert (
        qdict == expected_dict
    ), "The query dictionary does not match the expected values."

    # Additional checks to ensure individual keys are present
    for key in expected_dict.keys():
        assert key in qdict, f"Key '{key}' is missing from the query dictionary."


def test_load_query_not_found():
    """
    If we request a query name that doesn't exist, we should get a ValueError.
    """
    qm = QueryManager("fake_domain")
    with pytest.raises(
        ValueError, match="Query 'does_not_exist' not found in _query_dict"
    ):
        qm.load_query("does_not_exist", [])


def test_load_query_j2():
    """
    Test loading a Jinja (.j2) query file. We verify the final query text is the
    rendered version from the Jinja environment.
    """
    qm = QueryManager("fake_domain")
    entity_ids = [0, 1]
    entity_variables = {
        f"entityId_{i}": entity_id for i, entity_id in enumerate(entity_ids)
    }
    rendered_text = qm.load_query(
        "get_raw_values",
        entity_variables.keys(),
    )
    expected_text = load_file_content("assert_results/rendered_jinja_raw.graphql")
    # qm_json = json.loads(qm.query_text)

    # Parse both GraphQL strings into Abstract Syntax Trees (ASTs)
    rendered_ast = parse(rendered_text)
    expected_ast = parse(expected_text)

    # Convert the ASTs back to normalized strings
    rendered_normalized = print_ast(rendered_ast)
    expected_normalized = print_ast(expected_ast)

    assert rendered_normalized == expected_normalized
    # assert qm_json == rendered_json, "QueryManager.query should store the rendered text"


def test_load_query_graphql():
    """
    Loading a .graphql file should read its contents directly and not use Jinja.
    """
    qm = QueryManager("fake_domain")
    query_text = qm.load_query("get_domains", [])
    assert query_text == load_file_content(
        "../../src/piscada_foresight/queries_templates/graphql_queries/domains/get_domains.graphql"
    )
    assert qm.query_text == query_text


def test_load_query_unsupported_extension():
    """
    If the file extension is not .j2 or .graphql, we raise a ValueError.
    (We'll simulate this by manually inserting an unsupported extension in _query_dict.)
    """
    qm = QueryManager("fake_domain")
    # Manually insert an unsupported extension
    qm._query_dict["bad_query"] = "folder/bad_query.txt"

    with pytest.raises(
        ValueError, match="Unsupported query file type: 'folder/bad_query.txt'"
    ):
        qm.load_query("bad_query", [])
