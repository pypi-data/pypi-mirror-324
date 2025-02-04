import logging

from pandas import DataFrame, concat, to_datetime

log = logging.getLogger(__name__)


class TimeseriesResponseParser:
    """
    A class responsible for converting GraphQL timeseries responses
    into Pandas DataFrames.

    Methods
    -------
    parse(
        response: dict,
        entity_variables: dict,
        start: datetime,
        end: datetime,
        query_type: str
    ) -> DataFrame
        High-level entry point. Decides which parser to call based on `query_type`.

    _parse_raw_values(
        response: dict,
        entity_variables: dict,
        start: datetime,
        end: datetime
    ) -> DataFrame
        Parses response from a 'get_raw_values' GraphQL query.

    _parse_aggregated_values(
        response: dict,
        entity_variables: dict,
        start: datetime,
        end: datetime
    ) -> DataFrame
        Parses response from a 'get_aggregated_values' GraphQL query.
    """

    def parse(
        self, response, entity_variables, start, end, query_type="raw"
    ) -> DataFrame:
        """
        Dispatch to the appropriate parser method based on `query_type`.

        Parameters
        ----------
        response : dict
            The raw GraphQL response (already converted to Python dict).
        entity_variables : dict
            A mapping like {"entityId_0": "some_entity_id", ...}.
        start : datetime
            The start time used in the query (for error messages).
        end : datetime
            The end time used in the query (for error messages).
        query_type : str
            Determines which parser to use, e.g. "raw" or "aggregated".

        Returns
        -------
        DataFrame
            The parsed DataFrame.
        """
        if query_type == "raw":
            return self._parse_raw_values(response, entity_variables, start, end)
        elif query_type == "aggregated":
            return self._parse_aggregated_values(response, entity_variables, start, end)
        else:
            raise ValueError(f"Unknown query_type: {query_type}")

    def _parse_raw_values(self, response, entity_variables, start, end) -> DataFrame:
        """
        Parses a 'get_raw_values' style response, which typically has
            response = {
              "entityId_0": {
                "name": "...",
                "trait": {
                  "quantity": {
                    "values": [
                      { "eventTime": "...", "value": "..." },
                      ...
                    ]
                  }
                }
              },
              ...
            }
        """
        series_list = []

        for variable_name, entity_id in entity_variables.items():
            try:
                entity_data = response[variable_name]
                name = entity_data["name"]
                values = entity_data["trait"]["quantity"]["values"]

                # Convert to Series
                frame = DataFrame(values).set_index("eventTime")["value"]
                frame.index = to_datetime(frame.index, format="ISO8601")
                frame = frame.astype(float)
                frame.name = name
                series_list.append(frame)

            except KeyError as exc:
                msg = (
                    f"Could not retrieve raw values for entity '{entity_id}' "
                    f"in time range {start} - {end}. Missing key: {exc}"
                )
                log.error(msg)
                raise RuntimeError(msg) from exc
            except TypeError as exc:
                msg = f"Could not find entity '{entity_id}'."
                log.error(msg)
                raise RuntimeError(msg) from exc

        if not series_list:
            return DataFrame()

        # Merge all entities' series side by side
        df = concat(series_list, axis=1)
        df = df.ffill()  # optional forward-fill
        return df

    def _parse_aggregated_values(
        self, response, entity_variables, start, end
    ) -> DataFrame:
        """
        Parses a 'get_aggregated_values' style response, which typically has
            response = {
              "entityId_0": {
                "name": "...",
                "trait": {
                  "quantity": {
                    "aggregatedTimeseries": [
                      [ { "eventTime": "...", "value": "...", "aggregationFunction": "min" }, ... ],
                      [ { "eventTime": "...", "value": "...", "aggregationFunction": "max" }, ... ],
                      ...
                    ]
                  }
                }
              },
              ...
            }
        """
        all_frames = []

        for variable_name, entity_id in entity_variables.items():
            try:
                entity_data = response[variable_name]
                name = entity_data["name"]
                agg_series_list = entity_data["trait"]["quantity"][
                    "aggregatedTimeseries"
                ]
            except KeyError as exc:
                msg = (
                    f"Could not retrieve aggregated values for entity '{entity_id}' "
                    f"in time range {start} - {end}. Missing key: {exc}"
                )
                log.error(msg)
                raise RuntimeError(msg) from exc

            frames_for_this_entity = []
            for sublist in agg_series_list:
                if not sublist:
                    continue
                tmp_df = DataFrame(sublist).set_index("eventTime")
                tmp_df.index = to_datetime(tmp_df.index, format="ISO8601")

                # aggregator name is typically the same for all rows
                aggregator = tmp_df["aggregationFunction"].iloc[0]
                col_name = f"{name}|{aggregator}"

                tmp_df["value"] = tmp_df["value"].astype(float)
                tmp_df.rename(columns={"value": col_name}, inplace=True)

                # keep only the aggregator column
                frames_for_this_entity.append(tmp_df[[col_name]])

            if frames_for_this_entity:
                entity_df = concat(frames_for_this_entity, axis=1)
                all_frames.append(entity_df)

        if not all_frames:
            log.warning(
                f"No data found for the requested time range {start} - {end}. Returning an empty DataFrame."
            )
            return DataFrame()

        # Merge horizontally across all entities
        df = concat(all_frames, axis=1)
        df = df.ffill()
        return df
