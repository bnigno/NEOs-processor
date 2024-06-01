import csv
import os
import unittest

from neo_data_pipeline.csv_writer import CsvWriter


class TestCsvWriter(unittest.TestCase):
    def setUp(self):
        self.csv_writer = CsvWriter()
        self.test_data = [
            {
                "Id": 1,
                "Nome": "Test NEO",
                "Data de Aproximação": "2024-05-01",
                "Diâmetro Mínimo (km)": 0.1,
                "Diâmetro Máximo (km)": 0.2,
                "Velocidade (m/s)": 10000,
                "Distância da Terra (km)": 1000000,
                "Categoria Diâmetro": "Médio",
                "Categoria Proximidade": "Próximo",
                "Potencialmente Perigoso": False,
                "Tipo de Órbita": "APO",
            }
        ]
        self.fieldnames = [
            "Id",
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
        self.test_file = "test_neo_data.csv"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_to_csv(self):
        self.csv_writer.save_to_csv(self.test_data, self.fieldnames, self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

        with open(self.test_file, "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["Nome"], "Test NEO")


if __name__ == "__main__":
    unittest.main()
