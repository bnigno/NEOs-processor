from datetime import datetime


class Processor:
    @staticmethod
    def convert_kmh_to_ms(speed_kmh):
        return speed_kmh * 1000 / 3600

    @staticmethod
    def categorize_diameter(diameter_max):
        if diameter_max < 0.1:
            return "Pequeno"
        elif diameter_max < 0.5:
            return "Médio"
        else:
            return "Grande"

    @staticmethod
    def categorize_proximity(distance):
        if distance < 1000000:
            return "Muito Próximo"
        elif distance < 5000000:
            return "Próximo"
        else:
            return "Distante"

    @staticmethod
    def standardize_date(epoch_approach):
        return (
            datetime.utcfromtimestamp(float(epoch_approach) / 1000).date().isoformat()
        )

    def process(self, neo_data):
        for idx, date_array in neo_data.items():
            for item in date_array:
                name = item["name"]
                approach_data = item["close_approach_data"][0]
                approach_date = self.standardize_date(
                    approach_data["epoch_date_close_approach"]
                )
                diameter_min = item["estimated_diameter"]["kilometers"][
                    "estimated_diameter_min"
                ]
                diameter_max = item["estimated_diameter"]["kilometers"][
                    "estimated_diameter_max"
                ]
                speed_kmh = float(
                    approach_data["relative_velocity"]["kilometers_per_hour"]
                )
                speed_ms = self.convert_kmh_to_ms(speed_kmh)
                distance = float(approach_data["miss_distance"]["kilometers"])
                hazardous = item["is_potentially_hazardous_asteroid"]
                diameter_category = self.categorize_diameter(diameter_max)
                proximity_category = self.categorize_proximity(distance)

                yield {
                    "Nome": name,
                    "Data de Aproximação": approach_date,
                    "Diâmetro Mínimo (km)": diameter_min,
                    "Diâmetro Máximo (km)": diameter_max,
                    "Velocidade (m/s)": speed_ms,
                    "Distância da Terra (km)": distance,
                    "Categoria Diâmetro": diameter_category,
                    "Categoria Proximidade": proximity_category,
                    "Potencialmente Perigoso": hazardous,
                }
