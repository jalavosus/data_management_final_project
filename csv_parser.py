import csv
import json
from pprint import pprint


def load_csv_data(filename):
  fieldnames = [ "date", "open", "high", "low", "close", "adj_close", "volume" ]
  with open(filename, "r") as csvfile:
    data = [dict(row) for row in csv.DictReader(csvfile, fieldnames=fieldnames)][1:]

  return data


def parse_data(row):
  for field in [ "open", "high", "low", "close", "adj_close" ]:
    row[field] = float(row[field])
  row["volume"] = int(row["volume"])

  return row


def main():
  filename = "igv_historical_prices"
  data = load_csv_data(f"{filename}.csv")
  parsed_data = [parse_data(d) for d in data]

  with open(f"{filename}.json", "w") as historical:
    json.dump(parsed_data, historical)


if __name__ in '__main__':
  main()
