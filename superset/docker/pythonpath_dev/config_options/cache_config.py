from datetime import timedelta
from superset.key_value.types import JsonKeyValueCodec

CACHE_DEFAULT_TIMEOUT = int(timedelta(days=1).total_seconds())

# Default cache for Superset objects
CACHE_CONFIG = {"CACHE_TYPE": "NullCache"}

# Cache for datasource metadata and query results
DATA_CACHE_CONFIG = {"CACHE_TYPE": "NullCache"}

# Cache for dashboard filter state. `CACHE_TYPE` defaults to `SupersetMetastoreCache`
# that stores the values in the key-value table in the Superset metastore, as it's
# required for Superset to operate correctly, but can be replaced by any
# `Flask-Caching` backend.
FILTER_STATE_CACHE_CONFIG = {
    "CACHE_TYPE": "SupersetMetastoreCache",
    "CACHE_DEFAULT_TIMEOUT": int(timedelta(days=90).total_seconds()),
    # Should the timeout be reset when retrieving a cached value?
    "REFRESH_TIMEOUT_ON_RETRIEVAL": True,
    # The following parameter only applies to `MetastoreCache`:
    # How should entries be serialized/deserialized?
    "CODEC": JsonKeyValueCodec(),
}

# Cache for explore form data state. `CACHE_TYPE` defaults to `SupersetMetastoreCache`
# that stores the values in the key-value table in the Superset metastore, as it's
# required for Superset to operate correctly, but can be replaced by any
# `Flask-Caching` backend.
EXPLORE_FORM_DATA_CACHE_CONFIG = {
    "CACHE_TYPE": "SupersetMetastoreCache",
    "CACHE_DEFAULT_TIMEOUT": int(timedelta(days=7).total_seconds()),
    # Should the timeout be reset when retrieving a cached value?
    "REFRESH_TIMEOUT_ON_RETRIEVAL": True,
    # The following parameter only applies to `MetastoreCache`:
    # How should entries be serialized/deserialized?
    "CODEC": JsonKeyValueCodec(),
}
