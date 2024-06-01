import requests

from neo_data_pipeline.api_client import NasaNeoApiClient
from neo_data_pipeline.csv_writer import CsvWriter
from neo_data_pipeline.processor import Processor


class DataPipeline:
    def __init__(self, api_key):
        self.api_client = NasaNeoApiClient(api_key)
        self.data_processor = Processor()
        self.csv_writer = CsvWriter()
        self.fieldnames = [
            "Nome",
            "Data de Aproximação",
            "Diâmetro Mínimo (km)",
            "Diâmetro Máximo (km)",
            "Velocidade (m/s)",
            "Distância da Terra (km)",
            "Categoria Diâmetro",
            "Categoria Proximidade",
            "Potencialmente Perigoso",
            "Tipo de Órbita",
        ]

    def run(self, start_date, end_date, output_filename="neo_data.csv"):
        try:
            neo_data = self.api_client.fetch_neo_data(start_date, end_date)
            processed_data = self.data_processor.process(neo_data, self.api_client)
            self.csv_writer.save_to_csv(
                processed_data, self.fieldnames, output_filename
            )
            print(f"Data successfully saved to {output_filename}")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred while fetching data from the NASA API: {e}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data from the NASA API: {e}")
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
