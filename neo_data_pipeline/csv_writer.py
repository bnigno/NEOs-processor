import csv


class CsvWriter:
    @staticmethod
    def save_to_csv(data, filename="neo_data.csv"):
        with open(filename, "w", newline="") as f:
            fieldnames = [
                "Nome",
                "Data de Aproximação",
                "Diâmetro Mínimo (km)",
                "Diâmetro Máximo (km)",
                "Velocidade (m/s)",
                "Distância da Terra (km)",
                "Categoria Diâmetro",
                "Categoria Proximidade",
                "Potencialmente Perigoso",
            ]
            dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(data)
