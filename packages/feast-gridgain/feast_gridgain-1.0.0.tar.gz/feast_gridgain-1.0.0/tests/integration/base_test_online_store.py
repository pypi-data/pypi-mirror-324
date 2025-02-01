import pytest
from datetime import datetime
from unittest.mock import Mock, PropertyMock
from typing import Dict

from feast import RepoConfig, FeatureView
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto
from feast.repo_config import RegistryConfig

class BaseOnlineStoreIntegrationTest:
    """Base integration test class for online store implementations"""
    
    # Override these in child classes
    store_class = None  # The store class to test
    config_class = None  # The config class to use

    @pytest.fixture
    def feature_view(self):
        """Creates a feature view for testing"""
        mock = Mock(spec=FeatureView)
        type(mock).name = PropertyMock(return_value="integration_test_table")
        return mock

    @pytest.fixture
    def config(self):
        """Override this in child classes to provide appropriate config with real connection details"""
        raise NotImplementedError("Subclasses must implement config")

    @pytest.fixture
    def online_store(self):
        """Creates an instance of the online store"""
        return self.store_class()

    @pytest.fixture
    def test_data(self):
        """Provides test data with different types of features"""
        entity_keys = [
            EntityKeyProto(
                join_keys=["id"], 
                entity_values=[ValueProto(int64_val=i)]
            ) for i in range(1, 4)
        ]
        
        features_list = [
            {
                "int_feature": ValueProto(int64_val=i * 100),
                "float_feature": ValueProto(float_val=i * 0.5),
                "string_feature": ValueProto(string_val=f"value_{i}"),
                "timestamp_feature": ValueProto(unix_timestamp_val=int(datetime.now().timestamp()))
            } for i in range(1, 4)
        ]
        
        timestamp = datetime.utcnow()
        return list(zip(entity_keys, features_list, [timestamp]*3, [None]*3))

    def verify_feature_values(self, actual: Dict[str, ValueProto], expected: Dict[str, ValueProto]):
        """Helper method to verify feature values"""
        assert actual is not None
        for feature_name, expected_value in expected.items():
            # Skip timestamp features
            if expected_value.WhichOneof("val") == "unix_timestamp_val":
                continue
                
            assert feature_name in actual
            actual_value = actual[feature_name]
            
            # Check the type of value stored
            actual_type = actual_value.WhichOneof("val")
            expected_type = expected_value.WhichOneof("val")
            
            # Types should match
            assert actual_type == expected_type
            
            # Compare the actual values based on their type
            if actual_type == "int64_val":
                assert actual_value.int64_val == expected_value.int64_val
            elif actual_type == "float_val":
                assert abs(actual_value.float_val - expected_value.float_val) < 0.001
            elif actual_type == "string_val":
                assert actual_value.string_val == expected_value.string_val

    @pytest.mark.integration
    def test_write_and_read(self, config, feature_view, online_store, test_data):
        """Test writing data and reading it back"""
        # Write test data
        online_store.online_write_batch(config, feature_view, test_data, None)
        
        # Read back each entity and verify
        for entity_key, features, _, _ in test_data:
            result = online_store.online_read(config, feature_view, [entity_key])
            assert len(result) == 1
            timestamp, read_features = result[0]
            self.verify_feature_values(read_features, features)

    @pytest.mark.integration
    def test_nonexistent_key(self, config, feature_view, online_store):
        """Test reading a nonexistent key returns None"""
        nonexistent_key = EntityKeyProto(
            join_keys=["id"], 
            entity_values=[ValueProto(int64_val=999)]
        )
        result = online_store.online_read(config, feature_view, [nonexistent_key])
        assert len(result) == 1
        assert result[0] == (None, None)

    @pytest.mark.integration
    def test_update_and_teardown(self, config, feature_view, online_store):
        """Test cache creation and deletion"""
        # Update (create a new cache)
        online_store.update(config, [], [feature_view], [], [], False)

        # Write some test data
        entity_key = EntityKeyProto(
            join_keys=["id"],
            entity_values=[ValueProto(int64_val=1)]
        )
        features = {
            "test_feature": ValueProto(int64_val=100)
        }
        timestamp = datetime.utcnow()
        test_data = [(entity_key, features, timestamp, None)]

        online_store.online_write_batch(config, feature_view, test_data, None)

        # Verify data is readable
        result = online_store.online_read(config, feature_view, [entity_key])
        assert len(result) == 1
        assert result[0][1] is not None

        # Teardown - just verify this doesn't raise any errors
        online_store.teardown(config, [feature_view], [])

    @pytest.mark.integration
    def test_multiple_feature_types(self, config, feature_view, online_store):
        """Test writing and reading different types of features"""
        entity_key = EntityKeyProto(
            join_keys=["id"], 
            entity_values=[ValueProto(int64_val=1)]
        )
        
        features = {
            "int_feature": ValueProto(int64_val=42),
            "float_feature": ValueProto(float_val=3.14),
            "string_feature": ValueProto(string_val="test_value"),
            "timestamp_feature": ValueProto(unix_timestamp_val=int(datetime.now().timestamp()))
        }
        
        timestamp = datetime.utcnow()
        test_data = [(entity_key, features, timestamp, None)]
        
        # Write data
        online_store.online_write_batch(config, feature_view, test_data, None)
        
        # Read and verify
        result = online_store.online_read(config, feature_view, [entity_key])
        assert len(result) == 1
        self.verify_feature_values(result[0][1], features)

    @pytest.mark.integration
    def test_batch_operations(self, config, feature_view, online_store, test_data):
        """Test batch operations with multiple entities"""
        # Write batch data
        online_store.online_write_batch(config, feature_view, test_data, None)
        
        # Read all entities at once
        entity_keys = [entity_key for entity_key, _, _, _ in test_data]
        results = online_store.online_read(config, feature_view, entity_keys)
        
        assert len(results) == len(test_data)
        for i, (_, features, _, _) in enumerate(test_data):
            self.verify_feature_values(results[i][1], features)

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