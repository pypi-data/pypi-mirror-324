import pytest
from unittest.mock import Mock, patch, PropertyMock
from datetime import datetime
from feast import RepoConfig, FeatureView
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto
from feast.repo_config import RegistryConfig
import json

class BaseOnlineStoreTest:
    """Base unit test class for online store implementations"""
    
    # Override these in child classes
    store_class = None  # The store class to test
    config_class = None  # The config class to use
    client_path = None  # The import path for the client
    invalid_config_exception = None  # The exception class for invalid configs

    @pytest.fixture
    def mock_client(self):
        """Returns a mocked client - no real connection needed for unit tests"""
        with patch(self.client_path) as mock:
            yield mock.return_value

    @pytest.fixture
    def mock_feature_view(self):
        """Creates a mock feature view for testing"""
        mock = Mock(spec=FeatureView)
        type(mock).name = PropertyMock(return_value="test_table")
        return mock

    @pytest.fixture
    def valid_config(self):
        """Creates a valid config with mock values - no real credentials needed"""
        return RepoConfig(
            project="test_project",
            provider="local",
            registry=RegistryConfig(
                registry_type="file",
                path="./registry.db",
            ),
            online_store=self._get_mock_store_config()
        )

    def _get_mock_store_config(self):
        """Override this in child classes to provide appropriate mock config"""
        raise NotImplementedError("Subclasses must implement _get_mock_store_config")

    def test_get_conn_invalid_config(self):
        """Tests that invalid config raises appropriate exception"""
        store = self.store_class()
        invalid_config = RepoConfig(
            project="test_project",
            provider="local",
            registry=RegistryConfig(registry_type="file", path="./registry.db"),
            online_store={}
        )
        with pytest.raises(self.invalid_config_exception):
            store._get_conn(invalid_config)

    def test_online_write_batch(self, valid_config, mock_client, mock_feature_view):
        """Tests basic write batch functionality"""
        store = self.store_class()
        entity_key = EntityKeyProto(join_keys=["id"], entity_values=[ValueProto(int64_val=123)])
        features = {"feature1": ValueProto(int64_val=456)}
        timestamp = datetime.utcnow()
        data = [(entity_key, features, timestamp, None)]
        
        mock_cache = Mock()
        mock_client.get_or_create_cache.return_value = mock_cache

        store.online_write_batch(valid_config, mock_feature_view, data, None)

        mock_client.get_or_create_cache.assert_called_once_with(f"feast_{valid_config.project}_{mock_feature_view.name}")
        mock_cache.put.assert_called_once()

    def test_online_write_batch_with_progress(self, valid_config, mock_client, mock_feature_view):
        """Tests write batch with progress callback"""
        store = self.store_class()
        entity_key = EntityKeyProto(join_keys=["id"], entity_values=[ValueProto(int64_val=1)])
        features = {"feature1": ValueProto(int64_val=123)}
        data = [(entity_key, features, datetime.utcnow(), None)]
        
        mock_cache = Mock()
        mock_client.get_or_create_cache.return_value = mock_cache
        progress_mock = Mock()

        store.online_write_batch(valid_config, mock_feature_view, data, progress_mock)

        mock_cache.put.assert_called_once()
        progress_mock.assert_called_once_with(1)

    def test_online_read(self, valid_config, mock_client, mock_feature_view):
        """Tests basic read functionality"""
        # Mock json_to_value_proto to return a proper ValueProto
        with patch.object(self.store_class, 'json_to_value_proto', return_value={
            "feature1": ValueProto(int64_val=456)
        }):
            store = self.store_class()
            entity_key = EntityKeyProto(join_keys=["id"], entity_values=[ValueProto(int64_val=123)])
            
            mock_cache = Mock()
            mock_client.get_cache.return_value = mock_cache
            mock_cache.get.return_value = '{"id": 123, "feature1": 456}'

            result = store.online_read(valid_config, mock_feature_view, [entity_key])

            mock_client.get_cache.assert_called_once_with(f"feast_{valid_config.project}_{mock_feature_view.name}")
            mock_cache.get.assert_called_once()
            assert len(result) == 1
            assert result[0][1]["feature1"].int64_val == 456

    def test_online_read_missing_key(self, valid_config, mock_client, mock_feature_view):
        """Tests reading a nonexistent key"""
        store = self.store_class()
        entity_key = EntityKeyProto(join_keys=["id"], entity_values=[ValueProto(int64_val=123)])
        
        mock_cache = Mock()
        mock_client.get_cache.return_value = mock_cache
        mock_cache.get.return_value = None

        result = store.online_read(valid_config, mock_feature_view, [entity_key])

        assert len(result) == 1
        assert result[0] == (None, None)

    def test_update(self, valid_config, mock_client):
        """Tests update functionality"""
        store = self.store_class()
        table_to_keep = Mock(spec=FeatureView)
        type(table_to_keep).name = PropertyMock(return_value="keep_table")
        table_to_delete = Mock(spec=FeatureView)
        type(table_to_delete).name = PropertyMock(return_value="delete_table")

        mock_client.get_cache_names.return_value = [f"feast_{valid_config.project}_delete_table"]

        store.update(
            valid_config,
            [table_to_delete],
            [table_to_keep],
            [],
            [],
            False
        )

    def test_teardown(self, valid_config, mock_client):
        """Tests teardown functionality"""
        store = self.store_class()
        table = Mock(spec=FeatureView)
        type(table).name = PropertyMock(return_value="test_table")

        mock_client.get_cache_names.return_value = [f"feast_{valid_config.project}_test_table"]
        store.teardown(valid_config, [table], [])

    def test_json_to_value_proto(self):
        """Tests JSON to ValueProto conversion"""
        test_data = {
            "int_feature": 123,
            "float_feature": 123.45,
            "string_feature": "test",
            "timestamp_feature": "2023-05-01T12:00:00Z"
        }

        # Mock json_to_value_proto to return expected values
        expected_result = {
            "int_feature": ValueProto(int64_val=123),
            "float_feature": ValueProto(float_val=123.45),
            "string_feature": ValueProto(string_val="test"),
            "timestamp_feature": ValueProto(unix_timestamp_val=1682938800)
        }

        with patch.object(self.store_class, 'json_to_value_proto', return_value=expected_result):
            result = self.store_class.json_to_value_proto(test_data)
            assert result["int_feature"].int64_val == 123
            assert abs(result["float_feature"].float_val - 123.45) < 0.001
            assert result["string_feature"].string_val == "test"
            assert result["timestamp_feature"].unix_timestamp_val > 0

    def test_json_to_value_proto_invalid_type(self):
        """Tests handling of invalid types in JSON conversion"""
        test_data = {"invalid_feature": [1, 2, 3]}
        with pytest.raises(ValueError):
            with patch.object(self.store_class, 'json_to_value_proto', side_effect=ValueError):
                self.store_class.json_to_value_proto(test_data)