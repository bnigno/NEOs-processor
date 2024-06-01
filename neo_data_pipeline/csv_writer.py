import csv


class CsvWriter:
    """
    A utility class for writing data to a CSV file.

    This class provides methods to save data to a CSV file with specified fieldnames.
    """

    @staticmethod
    def save_to_csv(data, fieldnames, filename="neo_data.csv"):
        """
        Save data to a CSV file with specified fieldnames.

        Args:
            data (iterable): An iterable (e.g., list, generator) of dictionaries containing the data to be written.
            fieldnames (list of str): A list of strings representing the header names for the CSV file.
            filename (str, optional): The name of the file to which the data will be written. Defaults to "neo_data.csv".
        """
        with open(filename, "w", newline="", encoding="utf-8") as f:
            dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(data)
