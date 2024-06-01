import csv


class CsvWriter:
    @staticmethod
    def save_to_csv(data, fieldnames, filename="neo_data.csv"):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(data)
