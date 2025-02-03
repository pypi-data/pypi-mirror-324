# Voltus Python Client

This is a Python client for interacting with the Voltus feature store API. It provides a convenient way to programmatically access Voltus functionalities, such as adding datasets, applying feature functions, and retrieving results.

## Installation

You can install the client using pip:

```bash
pip install voltus
```

## Usage

### Initialization

First, you need to initialize the client with your Voltus API base URL and a user authentication token:

```python
import os
from voltus.client import VoltusClient
from dotenv import load_dotenv
load_dotenv(verbose=True)

BASE_URL = os.getenv("BASE_URL", None)
USER_TOKEN = os.getenv("USER_TOKEN", None)

# Initialize the client
client = VoltusClient(api_base_url=BASE_URL, token=USER_TOKEN, verify_requests=True)
```

Make sure to set the `BASE_URL` and `USER_TOKEN` environment variables before running the script.

### Basic Operations

Here's how to perform common operations with the client:

#### Healthcheck

Check if the server is healthy

```python
# Check server health
if client.healthcheck():
    print("Server is healthy")
else:
    print("Server is not healthy")
```

#### Current Authenticated User

Retrieve information about the currently authenticated user.

```python
# Get the current authenticated user
user_data = client.get_current_authenticated_user()
print(f"Current User: {user_data['user']['username']}")
```

#### Get Task Status

Retrieve status of background tasks

```python
# Get task status for a specific task id
task_status = client.get_task_status(task_id='your_task_id')
print(task_status)

# Get status of all tasks
all_tasks_status = client.get_task_status()
print(all_tasks_status)
```

#### Add Dataset
Add a Pandas dataframe as a dataset on the server.

```python
import pandas as pd

# Create a sample pandas DataFrame
data = {
    "timestamp": pd.to_datetime(
        ["2023-01-01 00:00:00", "2023-01-01 01:00:00", "2023-01-01 02:00:00"], utc=True
    ),
    "power": [10, 12, 15],
    "unit": ["MW", "MW", "MW"],
}
df = pd.DataFrame(data)

# Add a dataset
dataset_name = "my_test_dataset"
client.add_dataset(df, dataset_name=dataset_name)
print(f"Dataset '{dataset_name}' added")
```
#### List Datasets
List all dataset names in the user's account.

```python
# List datasets
datasets = client.list_datasets()
print(f"Datasets available: {datasets}")
```

#### Retrieve Dataset
Retrieve a dataset in JSON format.

```python
# Retrieve a dataset
retrieved_dataset = client.retrieve_dataset(dataset_name=dataset_name)
print(f"Retrieved dataset: {retrieved_dataset['data'][:2]}")
```

#### Delete Datasets
Delete multiple datasets using a list of dataset names.

```python
# delete dataset(s)
client.delete_datasets(dataset_names=[dataset_name, "test_kmeans_from_data"])
print("Datasets deleted")
```

#### List Available Example Datasets
Lists all available example datasets.
```python
# List example datasets
example_dataset_names = client.list_example_datasets()
print(f"Example datasets available: {example_dataset_names}")
```
#### Retrieve Example Datasets
Retrieve the contents of a specific example dataset.
```python
# retrieve example dataset
example_dataset = client.retrieve_example_dataset(dataset_name="Power Usage")
print(f"Example dataset: {example_dataset['data'][:2]}")
```

#### Apply Feature Function to Dataset
Apply a feature function to a dataset that already exists on the server, creating a new dataset in the process.
```python
# Apply feature function
ff_response = client.apply_feature_function_to_dataset(
    feature_function_name="k_means_clustering",
    original_datasets=[dataset_name],
    generated_dataset_name="test_kmeans_from_data",
    kwargs={"num_clusters": 2},
    process_synchronously=False
)
print(f"Applying feature function. Response: {ff_response}")
```

#### List Available Feature Functions
Lists available feature functions on the server.
```python
# List available functions
available_functions = client.list_feature_functions()
print(f"Available functions: {[f['name'] for f in available_functions]}")
```
#### List Available Feature Functions Tags
Lists available feature functions tags on the server.
```python
# List available tags
available_tags = client.list_feature_functions_tags()
print(f"Available function tags: {available_tags}")
```

## Error Handling

The client raises exceptions if there are issues with the API requests, including network errors, authentication failures, and server-side errors.

## Examples

For more complete examples, see the `tests/test_client.py` file in the project repository.

## Contributing

Feel free to submit pull requests to the repository, in order to improve this library.
