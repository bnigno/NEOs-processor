import unittest
from concurrent.futures import Future
from unittest.mock import MagicMock

from neo_data_pipeline.processor import Processor


class TestNeoDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = Processor()

    def test_convert_kmh_to_ms(self):
        self.assertEqual(self.processor.convert_kmh_to_ms(900), 250)

    def test_categorize_diameter(self):
        self.assertEqual(self.processor.categorize_diameter(0.09), "Pequeno")
        self.assertEqual(self.processor.categorize_diameter(0.4), "Médio")
        self.assertEqual(self.processor.categorize_diameter(0.6), "Grande")

    def test_categorize_proximity(self):
        self.assertEqual(self.processor.categorize_proximity(900000), "Muito Próximo")
        self.assertEqual(self.processor.categorize_proximity(4000000), "Próximo")
        self.assertEqual(self.processor.categorize_proximity(6000000), "Distante")

    def test_standardize_date(self):
        self.assertEqual(self.processor.standardize_date(1717175726000), "2024-05-31")

    def test_process(self):
        # Mock the api_client
        mock_api_client = MagicMock()

        # Create a Future object to simulate the result of a ThreadPoolExecutor
        future = Future()
        future.set_result("Orbit Type")

        # Mock the fetch_neo_orbit_type method to return the future object
        mock_api_client.fetch_neo_orbit_type.return_value = future.result()

        neo_data = {
            "2024-06-01": [
                {
                    "id": "1",
                    "name": "Test NEO",
                    "close_approach_data": [
                        {
                            "epoch_date_close_approach": 1609459200000,
                            "relative_velocity": {"kilometers_per_hour": "900"},
                            "miss_distance": {"kilometers": "500000"},
                        }
                    ],
                    "estimated_diameter": {
                        "kilometers": {
                            "estimated_diameter_min": 0.1,
                            "estimated_diameter_max": 0.2,
                        }
                    },
                    "is_potentially_hazardous_asteroid": True,
                }
            ]
        }

        results = list(self.processor.process(neo_data, mock_api_client))

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["Nome"], "Test NEO")
        self.assertEqual(result["Data de Aproximação"], "2021-01-01")
        self.assertEqual(result["Diâmetro Mínimo (km)"], 0.1)
        self.assertEqual(result["Diâmetro Máximo (km)"], 0.2)
        self.assertAlmostEqual(result["Velocidade (m/s)"], 250)
        self.assertAlmostEqual(result["Distância da Terra (km)"], 500000)
        self.assertEqual(result["Categoria Diâmetro"], "Médio")
        self.assertEqual(result["Categoria Proximidade"], "Muito Próximo")
        self.assertTrue(result["Potencialmente Perigoso"])
        self.assertEqual(result["Tipo de Órbita"], "Orbit Type")


if __name__ == "__main__":
    unittest.main()
