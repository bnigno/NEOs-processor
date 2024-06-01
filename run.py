import sys

from neo_data_pipeline.pipeline import DataPipeline

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python run.py <api_key> <start_date> <end_date>")
        sys.exit(1)

    api_key = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]

    pipeline = DataPipeline(api_key)
    pipeline.run(start_date, end_date)
