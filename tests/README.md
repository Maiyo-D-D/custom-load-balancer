# Testing Suite Documentation

This README file provides an overview of the testing suite for the load balancer project. It includes instructions on how to run the tests, interpret the results, and contribute to the testing process.

## Overview

The testing suite is designed to ensure the reliability and correctness of the load balancer and its components. It includes unit tests, integration tests, and performance analysis scripts.

## Running Tests

To run the tests, ensure that you have the necessary dependencies installed. You can install them using the following command:

```
pip install -r requirements.txt
```

Once the dependencies are installed, you can run the tests using the following command:

```
pytest
```

This will execute all the tests in the `tests` directory.

## Test Structure

- **Unit Tests**: Located in `test_server.py` and `test_consistent_hash.py`, these tests verify the functionality of individual components.
- **Integration Tests**: Located in `test_load_balancer.py`, these tests check the interaction between the load balancer and the server.
- **Performance Analysis**: The `performance_analysis.py` script can be used to analyze the performance of the application and generate relevant metrics.

## Interpreting Results

After running the tests, you will see a summary of the results in the terminal. Each test will indicate whether it passed or failed. In case of failures, the output will provide details on what went wrong, allowing you to debug the issue.