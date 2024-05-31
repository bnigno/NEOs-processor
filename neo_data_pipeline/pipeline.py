import requests


class DataPipeline:
    def __init__(self, api_client, data_processor, csv_writer):
        self.api_client = api_client
        self.data_processor = data_processor
        self.csv_writer = csv_writer

    def run(self, start_date, end_date, output_filename):
        try:
            neo_data = self.api_client.fetch_neo_data(start_date, end_date)
            processed_data = self.data_processor.process(neo_data)
            self.csv_writer.save_to_csv(processed_data, output_filename)
            print(f"Data successfully saved to {output_filename}")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred while fetching data from the NASA API: {e}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data from the NASA API: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
