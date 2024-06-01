from concurrent.futures import ThreadPoolExecutor
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

    def process(self, neo_data, api_client):
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_neo = {
                executor.submit(api_client.fetch_neo_orbit_type, neo["id"]): neo
                for date in neo_data
                for neo in neo_data[date]
            }
            for future in future_to_neo:
                neo = future_to_neo[future]
                name = neo.get("name")
                approach_data = (
                    neo.get("close_approach_data")[0]
                    if neo.get("close_approach_data")
                    else None
                )

                if approach_data:
                    approach_date = self.standardize_date(
                        approach_data.get("epoch_date_close_approach")
                    )
                    speed_kmh = (
                        float(
                            approach_data.get("relative_velocity", {}).get(
                                "kilometers_per_hour", 0
                            )
                        )
                        or None
                    )
                    distance = (
                        float(
                            approach_data.get("miss_distance", {}).get("kilometers", 0)
                        )
                        or None
                    )
                else:
                    approach_date = None
                    speed_kmh = None
                    distance = None

                diameter_min = (
                    neo.get("estimated_diameter", {})
                    .get("kilometers", {})
                    .get("estimated_diameter_min")
                )
                diameter_max = (
                    neo.get("estimated_diameter", {})
                    .get("kilometers", {})
                    .get("estimated_diameter_max")
                )

                speed_ms = self.convert_kmh_to_ms(speed_kmh) if speed_kmh else None
                hazardous = neo.get("is_potentially_hazardous_asteroid")
                diameter_category = (
                    self.categorize_diameter(diameter_max) if diameter_max else None
                )
                proximity_category = (
                    self.categorize_proximity(distance) if distance else None
                )
                orbit_type = future.result()

                yield {
                    "Id": neo.get("id"),
                    "Nome": name,
                    "Data de Aproximação": approach_date,
                    "Diâmetro Mínimo (km)": diameter_min,
                    "Diâmetro Máximo (km)": diameter_max,
                    "Velocidade (m/s)": speed_ms,
                    "Distância da Terra (km)": distance,
                    "Categoria Diâmetro": diameter_category,
                    "Categoria Proximidade": proximity_category,
                    "Potencialmente Perigoso": hazardous,
                    "Tipo de Órbita": orbit_type,
                }
