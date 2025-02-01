# feast-gridgain

This package enables the use of Apache Ignite or GridGain as an online store for Feast, providing high-performance, in-memory data storage and retrieval for feature serving.

## Table of Contents
1. [Features](#features)
2. [Setup Instructions](#setup-instructions)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
3. [API Reference](#api-reference)
4. [Documentation](#documentation)
5. [Example](#example)

## Features

- **Ignite/GridGain Integration:** Leverages Ignite's in-memory database to provide online features for real-time model predictions.
- **Feature Management:** Feast manages feature definitions, versioning, and the synchronization between online and offline stores.

## Project Structure

The project consists of two main components:

1. **Ignite Online Store (`online_store.py`):** Sets up Apache Ignite as the online feature store.
2. **GridGain Online Store (`gridgain_online_store.py`):** Configures GridGain as the online feature store.

Both implementations provide similar functionality but are tailored to their respective systems.

## Setup Instructions

### Prerequisites

* Python 3.11.7
* Running Apache Ignite or GridGain cluster

### Installation

Install the package using pip:

```bash
pip install feast-gridgain
```

## API Reference

### IgniteOnlineStore / GridGainOnlineStore

Both classes implement the following methods:

- `online_read(config, table, entity_keys, requested_features)`: Reads feature values from the online store.
- `online_write_batch(config, table, data, progress)`: Writes a batch of feature data to the online store.
- `update(config, tables_to_delete, tables_to_keep, entities_to_delete, entities_to_keep, partial)`: Updates the online store based on changes to the feature repository.
- `teardown(config, tables, entities)`: Cleans up the online store.

For detailed information on these methods, refer to the docstrings in the source code.

## Documentation

For an up-to-date documentation, see the [GridGain Docs](https://www.gridgain.com/docs/extensions/vector/feast).

## Example

For a comprehensive, real-world example of how to use this package, please refer to the following GitHub repository:

[CGM Ignite Feast Kafka Example](https://github.com/GridGain-Demos/ignite_feast_cgm_demo)

This repository provides a detailed implementation that demonstrates the integration of Ignite Online Store with Feast in a Continuous Glucose Monitoring (CGM) use case. It includes examples of configuration, feature definitions, and usage in different environments.