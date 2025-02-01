import pytest
from datetime import datetime
from feast import RepoConfig
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto
from feast.repo_config import RegistryConfig
from feast_gridgain.ignite_online_store import (
    IgniteOnlineStore,
    IgniteOnlineStoreConfig,
)
from tests.integration.base_test_online_store import BaseOnlineStoreIntegrationTest

class TestIgniteOnlineStoreIntegration(BaseOnlineStoreIntegrationTest):
    """Integration tests for Ignite online store implementation"""
    
    store_class = IgniteOnlineStore
    config_class = IgniteOnlineStoreConfig

    @pytest.fixture
    def config(self):
        """Creates a config with real Ignite connection details"""
        return RepoConfig(
            project="ignite_integration_test",
            provider="local",
            registry=RegistryConfig(
                registry_type="file",
                path="./registry.db",
            ),
            online_store=IgniteOnlineStoreConfig(
                host="localhost",  # Replace if using different host
                port=10800
            )
        )

    @pytest.mark.integration
    def test_ignite_specific_feature(self, config, feature_view, online_store):
        """Test Ignite-specific functionality if any"""
        # Add any Ignite-specific test cases here
        pass

    @pytest.mark.integration
    def test_default_connection_values(self, feature_view, online_store):
        """Test Ignite's default connection behavior"""
        config = RepoConfig(
            project="ignite_integration_test",
            provider="local",
            registry=RegistryConfig(
                registry_type="file",
                path="./registry.db",
            ),
            online_store=IgniteOnlineStoreConfig()  # No explicit host/port
        )
        
        # Should use default localhost:10800
        entity_key = EntityKeyProto(
            join_keys=["id"], 
            entity_values=[ValueProto(int64_val=1)]
        )
        features = {"test_feature": ValueProto(int64_val=100)}
        timestamp = datetime.utcnow()
        test_data = [(entity_key, features, timestamp, None)]
        
        online_store.online_write_batch(config, feature_view, test_data, None)
        result = online_store.online_read(config, feature_view, [entity_key])
        assert len(result) == 1
        assert result[0][1] is not None