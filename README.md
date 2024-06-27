It is a Python project designed to fetch, process, and store data about Near Earth Objects (NEOs) from NASA's public
API. The processed data is saved into a CSV file.

## Requirements

- Python 3.11 (Project tested with Python 3.11, but it should work with other versions compatible with the dependencies
  specified)
- pip

## Installation

1. Clone the repository.

2. Create a virtual environment.

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Obtain a NASA API key by registering at [NASA API](https://api.nasa.gov/).

2. Run the `run.py` script with your API key and desired date range (up to 7 days):

    ```sh
    python run.py NASA_API_KEY YYYY-MM-DD YYYY-MM-DD
     ```
   Replace NASA_API_KEY with your actual API key and YYYY-MM-DD with the start and end dates.

## Testing

1. Ensure you have all dependencies installed.
2. Run the tests using unittest:
    ```sh
    python -m unittest discover -s tests
    ```

## CI/CD

The project uses GitHub Actions for Continuous Integration. The workflow defined in `.github/workflows/tests.yml` runs
tests on each pull request to the `main` branch.
