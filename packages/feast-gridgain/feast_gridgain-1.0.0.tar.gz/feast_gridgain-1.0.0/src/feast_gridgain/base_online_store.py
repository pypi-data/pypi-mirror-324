from datetime import datetime
from typing import Sequence, Union, List, Optional, Tuple, Dict, Callable, Any

import json
from feast import RepoConfig, FeatureView, FeatureService, Entity
from feast.infra.key_encoding_utils import serialize_entity_key
from feast.infra.online_stores.online_store import OnlineStore
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto
from dateutil import parser
import logging
import sys
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

class BaseOnlineStore(OnlineStore):
    """
    The base online store implementation.
    NOTE: The class *must* end with the `OnlineStore` suffix.
    """

    def _get_conn(self, config: RepoConfig):
        """
        Establishes a connection to the gridgain/ignite cluster.

        Args:
            config: The Feast repository configuration object containing gridgain/ignite connection details.

        Returns:
            A gridgain/ignite client instance connected to the cluster.
        """
        pass

    def online_write_batch(
        self,
        config: RepoConfig,
        table: Union[FeatureView, FeatureService], 
        data: List[
            Tuple[EntityKeyProto, Dict[str, ValueProto], datetime, Optional[datetime]]
        ],
        progress: Optional[Callable[[int], Any]],
    ) -> None:
        
        """
        Writes a batch of feature data to the gridgain/ignite online store.

        Args:
            config: The Feast repository configuration.
            table: The FeatureView or FeatureService defining the schema.
            data: A list of tuples containing (entity_key, features, timestamp, created_timestamp).
            progress: A callback function to track progress (optional).
        """

        try:
            client = self._get_conn(config)

            # Construct the cache name based on project and table name
            cache_name = f"feast_{config.project}_{table.name}"
            cache = client.get_or_create_cache(cache_name)
            
            # Iterate over each feature data item
            for entity_key, features, timestamp, created in data:

                # Serialize the entity key to a hexadecimal string
                entity_key_bin = serialize_entity_key(entity_key).hex()  # Serialize the entity key

                # Extract the ID (first join key) and subject_id from the entity key
                id = entity_key.join_keys[0]
                try:
                    id_value = entity_key.entity_values[0].int64_val
                except:
                    raise

                # Create a dictionary for storing the feature values with ID and id_value
                result_dict = {id: id_value}
                for feature_name, val in features.items():
                    match val.WhichOneof("val"):
                        case "unix_timestamp_val":
                            timestamp_seconds = val.unix_timestamp_val
                            # Convert to datetime object in UTC
                            dt_object = datetime.utcfromtimestamp(timestamp_seconds)
                            # Format the datetime to your desired format
                            result_dict[feature_name] = dt_object.strftime("%Y-%m-%d %H:%M:%S")
                        case "int64_val":
                            result_dict[feature_name] = val.int64_val
                        case "float_val":
                            result_dict[feature_name] = val.float_val
                        case "string_val":
                            result_dict[feature_name] = val.string_val
                        case "int32_val":
                            result_dict[feature_name] = val.int32_val
                        case _:  # Default case for unsupported types
                            result_dict[feature_name] = val.string_val

                # Convert the result dictionary to JSON string
                json_string = json.dumps(result_dict)

                # Put the JSON string into the gridgain/ignite cache against a key
                cache.put(entity_key_bin, json_string)

                # Print the JSON string

                # Optional progress reporting
                if progress:
                    progress(1)
        except:
            logging.exception("Error while writing to the gridgain/ignite online store")
        finally:
            client.close()

    def online_read(
        self,
        config: RepoConfig,
        table: Union[FeatureView, FeatureService], 
        entity_keys: List[EntityKeyProto],
        requested_features: Optional[List[str]] = None,
    ) -> List[Tuple[Optional[datetime], Optional[Dict[str, ValueProto]]]]:

        """
        Reads feature values from the gridgain/ignite online store.

        Args:
            config: The Feast repository configuration.
            table: The FeatureView or FeatureService defining the schema.
            entity_keys: A list of entity keys to retrieve features for.
            requested_features: A list of specific features to retrieve (optional).

        Returns:
            A list of tuples containing (event_timestamp, features), where features is a dictionary of {feature_name: value}.
        """
        start_time = time.perf_counter_ns()
        client = self._get_conn(config)

        # Construct the cache name based on project and table name
        cache_name = f"feast_{config.project}_{table.name}"

        # Get the cache from gridgain/ignite
        start_time_get_cache = time.perf_counter_ns()
        cache = client.get_cache(cache_name)
        self.log("get_online_features", "base_online_store", "get_cache", time.perf_counter_ns()-start_time_get_cache)

        # Initialize the result list
        result: List[Tuple[Optional[datetime], Optional[Dict[str, ValueProto]]]] = []

        # Iterate over entity keys
        for entity_key in entity_keys:
            # Serialize the entity key
            entity_key_bin = serialize_entity_key(entity_key).hex()
            # Fetch the JSON string from gridgain/ignite cache

            start_time_cache_get = time.perf_counter_ns()
            values_str = cache.get(entity_key_bin)  # Fetch directly from cache
            self.log("get_online_features", "base_online_store", "cache.get", time.perf_counter_ns()-start_time_cache_get)

            # If the value exists in the cache
            start_time_cache_process = time.perf_counter_ns()
            if values_str:
                # Deserialize the JSON string to a dictionary
                values = json.loads(values_str)  # Deserialize from JSON string to Dict

                # Filter the dictionary to only include the requested features, if provided
                if requested_features:
                    res = BaseOnlineStore.json_to_value_proto(
                        {feature: values.get(feature) for feature in requested_features}
                    )
                else:
                    res = BaseOnlineStore.json_to_value_proto(values)
                # Extract event_ts if needed (depends on how you store it in gridgain)
                # For example, if event_ts is stored as a separate key-value pair in the same cache entry:
                # TODO: Implement timestamp extraction logic
                res_ts = values.get('event_ts', None)  # Replace with actual timestamp extraction logic
                result.append((datetime.fromtimestamp(res_ts) if res_ts else None, res))
            else:
                result.append((None, None))
            self.log("get_online_features", "base_online_store", "postprocess", time.perf_counter_ns()-start_time_cache_process)
            self.log("get_online_features", "base_online_store", "total", time.perf_counter_ns()-start_time)

        # Return the results for all entity keys
        return result

    def update(
        self,
        config: RepoConfig,
        tables_to_delete: Sequence[Union[FeatureView, FeatureService]],
        tables_to_keep: Sequence[Union[FeatureView, FeatureService]],
        entities_to_delete: Sequence[Entity],
        entities_to_keep: Sequence[Entity],
        partial: bool,
    ):
        """
        Updates the gridgain/ignite online store based on changes to the feature repository.

        This method handles adding new feature views/services, removing old ones, and updating existing ones.

        Args:
            config: The Feast repository configuration.
            tables_to_delete: A sequence of FeatureView or FeatureService objects to delete.
            tables_to_keep: A sequence of FeatureView or FeatureService objects to keep.
            entities_to_delete: A sequence of Entity objects to delete.
            entities_to_keep: A sequence of Entity objects to keep.
            partial: Whether this is a partial update (only update specified tables/entities).
        """

        client = self._get_conn(config)

        # Handle tables (feature views/services) that need to be kept
        for table in tables_to_keep:
            cache_name = f"feast_{config.project}_{table.name}" # Construct cache name
            # Check if the cache already exists
            if cache_name not in client.get_cache_names():
                # If it doesn't exist, create it
                client.create_cache(cache_name)

        # Handle tables (feature views/services) that need to be deleted
        for table in tables_to_delete:
            cache_name = f"feast_{config.project}_{table.name}"

            # Destroy the cache if it exists
            if cache_name in client.get_cache_names():
                client.get_cache(cache_name).destroy()


    def teardown(
        self,
        config: RepoConfig,
        tables: Sequence[Union[FeatureView, FeatureService]],
        entities: Sequence[Entity],
    ):
        """
        Cleans up (tears down) the gridgain/ignite online store.

        This method destroys all caches associated with the specified tables and entities.

        Args:
            config: The Feast repository configuration.
            tables: A sequence of FeatureView or FeatureService objects to delete.
            entities: A sequence of Entity objects to delete.
        """

        client = self._get_conn(config)

        # Iterate over the tables (FeatureView or FeatureService objects) to be removed
        for table in tables:
            # Construct the cache name for this table, following the naming convention "feast_{project_name}_{table_name}"
            cache_name = f"feast_{config.project}_{table.name}"

            # Check if the cache exists in gridgain/ignite
            if cache_name in client.get_cache_names():
                cache = client.get_cache(cache_name)
                cache.destroy()

    @staticmethod
    def json_to_value_proto(features: Dict[str, any]) -> Dict[str, ValueProto]:
        """
        Converts a dictionary of JSON values to a dictionary of ValueProtos,
        handling int64, float, string, and timestamp types.
        """
        result_dict = {}
        for feature_name, val in features.items():
            if isinstance(val, int):
                result_dict[feature_name] = ValueProto(int64_val=val)
            elif isinstance(val, float):
                result_dict[feature_name] = ValueProto(float_val=val)
            elif isinstance(val, str):
                # Try parsing as ISO timestamp
                try:
                    dt_obj = parser.parse(val)
                    unix_timestamp = int(dt_obj.timestamp())
                    result_dict[feature_name] = ValueProto(unix_timestamp_val=unix_timestamp)
                except parser.ParserError:
                    # If not a timestamp, store as string
                    result_dict[feature_name] = ValueProto(string_val=val)
            else:
                raise ValueError(
                    f"Unsupported value type for feature '{feature_name}': {type(val)}"
                )
        return result_dict

    def log(self,feature, layer, event, timetaken):
        """
        Function to be called from your other scripts (producer, consumer, online store).
        Prepares the log message and sends it to the central logging server.
        """
        timetakeninmicro = timetaken/1000
        timetakeninmillis = timetakeninmicro/1000
        message = {
            "feature": feature,
            "layer": layer,
            "event": event,
            "timetaken": timetaken,
            "timetakeninmicro": timetakeninmicro,
            "timetakeninmillis": timetakeninmillis
        }
        logging.info(message)  # Run the async function in an event loop