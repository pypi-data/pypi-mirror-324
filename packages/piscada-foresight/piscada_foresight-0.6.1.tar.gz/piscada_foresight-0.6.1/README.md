# Piscada Foresight

_*Access knowledge-graph and timeseries data.*_


## Overview

This library provides access to the knowledge-graph and timeseries data in the Foresight platform. It implements a Transport using [HTTPX](https://www.python-httpx.org/) to be used with the [GQL](https://gql.readthedocs.io/) GraphQL client. It provides the following modules:

- `data` module: Read timeseries values as [Pandas](https://pandas.pydata.org/) DataFrames or Series
  - `get_value()`: Get latest value before a given time
  - `get_values()`: Get values between start and end time
  - `get_all_values()`: Extract all values from a graph query response

- `domains` module: Access domain definitions and trait hierarchies
  - `Domain` class: Contains traits and relationships for a domain
    - `get_trait_by_id()`: Gets a trait by its ID
  - `get_domains()`: Retrieve list of all available domains
  - `get_trait_by_id()`: Get a trait from any domain by its ID string
  - `get_parent_traits()`: Get all parent traits for a given trait

- `http` module: OAuth2 authenticated transport
  - `ForesightHTTPXTransport` class: HTTPX transport with OAuth2 authentication
    - `connect()`: Establish authenticated connection


## Installation

```bash
pip install piscada-foresight
```

You will need access to a Piscada Foresight instance. The library uses the OAuth2 Authorization Code Flow with Proof Key for Code Exchange (PKCE) to act on behalf of your user. After an initial interactive login, the library persists the session state in `$HOME/.<client_id>_state` and will use that to authenticate non-interactive the next time.


## Usage

```python
from datetime import datetime, timedelta, timezone

from piscada_foresight.data import get_value, get_values
from piscada_foresight.queries.query_manager import QueryManager

domain = "foresight.piscada.cloud"
query_manager = QueryManager(domain)

# Retrieve timeseries values for two specific entites:
get_values(
  query_manager,
  entity_ids=["ENTITY_ID", "ENTITY_ID2"],
  start=datetime.now(tz=timezone.utc) - timedelta(hours=8),
)

# Retrieve aggregated timeseries values for two specific entites:
get_values(
  query_manager,
  entity_ids=["ENTITY_ID", "ENTITY_ID2"],
  start=datetime.now(tz=timezone.utc) - timedelta(hours=8),
  interval="1h",
  aggregation_functions=["min", "max", "avg", "count", "last"],
)


```

## Contributing

Contributions are welcome! You can contact us at [foresight@piscada.com](mailto:foresight@piscada.com).


## Support

If you have any questions, issues, or suggestions, please contact us at [foresight@piscada.com](mailto:foresight@piscada.com).


## Copyright

© Piscada AS 2024
