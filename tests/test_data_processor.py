import unittest

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
        neo_data = {
            "2024-05-01": [
                {
                    "name": "Test NEO",
                    "close_approach_data": [
                        {
                            "epoch_date_close_approach": 1704201240000,
                            "relative_velocity": {"kilometers_per_hour": "36000"},
                            "miss_distance": {"kilometers": "1000000"},
                        }
                    ],
                    "estimated_diameter": {
                        "kilometers": {
                            "estimated_diameter_min": 0.1,
                            "estimated_diameter_max": 0.2,
                        }
                    },
                    "is_potentially_hazardous_asteroid": False,
                }
            ]
        }

        processed = list(self.processor.process(neo_data))
        self.assertEqual(len(processed), 1)
        self.assertEqual(processed[0]["Nome"], "Test NEO")
        self.assertEqual(processed[0]["Data de Aproximação"], "2024-01-02")


if __name__ == "__main__":
    unittest.main()
