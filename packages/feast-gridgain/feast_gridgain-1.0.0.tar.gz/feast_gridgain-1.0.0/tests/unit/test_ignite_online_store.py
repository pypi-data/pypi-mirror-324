import pytest
from feast import RepoConfig
from feast.repo_config import RegistryConfig
from feast_gridgain.ignite_online_store import (
    IgniteOnlineStore,
    IgniteOnlineStoreConfig,
    IgniteInvalidConfig,
)
from .base_test_online_store import BaseOnlineStoreTest

class TestIgniteOnlineStore(BaseOnlineStoreTest):
    """Unit tests for Ignite online store implementation"""
    
    store_class = IgniteOnlineStore
    config_class = IgniteOnlineStoreConfig
    client_path = 'feast_gridgain.ignite_online_store.Client'
    invalid_config_exception = IgniteInvalidConfig

    def _get_mock_store_config(self):
        """Provides mock configuration for unit tests"""
        return IgniteOnlineStoreConfig(
            host="localhost",
            port=10800
        )

    def test_get_conn_valid_config(self, valid_config, mock_client):
        """Tests connection with valid configuration"""
        store = self.store_class()
        conn = store._get_conn(valid_config)
        assert conn == mock_client
        mock_client.connect.assert_called_once_with("localhost", 10800)

    def test_get_conn_default_values(self, valid_config, mock_client):
        """Tests connection with default configuration values"""
        store = self.store_class()
        valid_config.online_store.host = None
        valid_config.online_store.port = None
        conn = store._get_conn(valid_config)
        assert conn == mock_client
        mock_client.connect.assert_called_once_with("localhost", 10800)