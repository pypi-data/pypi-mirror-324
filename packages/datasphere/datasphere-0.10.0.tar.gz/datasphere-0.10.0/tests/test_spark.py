import json

import pytest
from pytest import raises

from datasphere.spark import (
    ConnectionMode,
    SparkConfig,
    load_spark_config,
    parse_spark_config,
)


def test_parse_spark_config():
    parse_spark_config({'master_node_host': 'localhost', 'connection_mode': 'SPARK_CONTEXT', 'session_params': {'spark.app.name': 'test'}}) == SparkConfig('localhost', ConnectionMode.CONTEXT, {'spark.app.name': 'test'})

    parse_spark_config({'master_node_host': 'localhost', 'connection_mode': 'SPARK_CONNECT', 'session_params': {'spark.app.name': 'test'}}) == SparkConfig('localhost', ConnectionMode.CONNECT, {'spark.app.name': 'test'})

    invalid_cases = [
        ("illegal-config", "Config must be a dict"),
        ({}, "Master node host is not specified"),
        ({'master_node_host': []}, "Master node host must be a string"),
        ({'master_node_host': 'localhost'}, "Connection mode is not specified"),
        (
            {'master_node_host': 'localhost', 'connection_mode': 'random-mode', 'session_params': {'spark.app.name': 'test'}},
            "Unknown mode 'random-mode'"
        ),
        (
            {'master_node_host': 'localhost', 'connection_mode': 'SPARK_CONTEXT', 'session_params': []},
            "Spark session params must be a dict of strings"
        ),
        (
            {'master_node_host': 'localhost', 'connection_mode': 'SPARK_CONTEXT', 'session_params': {123: "test"}},
            "Spark session params must be a dict of strings"
        ),
        (
            {'master_node_host': 'localhost', 'connection_mode': 'SPARK_CONTEXT', 'session_params': {'test': 123}},
            "Spark session params must be a dict of strings"
        ),
    ]
    for cfg, error_message in invalid_cases:
        with raises(ValueError, match=error_message):
            parse_spark_config(cfg)


def test_load_spark_config(tmp_path):

    with raises(FileNotFoundError, match="Config path 'non-existent-file' is not found or is not a regular file"):
        load_spark_config('non-existent-file')

    config_path = tmp_path / 'spark_config.json'
    config_path.write_text(json.dumps({'master_node_host': 'localhost', 'connection_mode': 'SPARK_CONTEXT', 'session_params': {'spark.app.name': 'test'}}))
    load_spark_config(config_path) == SparkConfig('localhost', ConnectionMode.CONTEXT, {'spark.app.name': 'test'})
