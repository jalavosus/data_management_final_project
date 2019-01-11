import json
from pprint import pprint


def calc_change(data):
  for i, d in enumerate(data):
    if i == len(data) - 1:
      break
    diff = data[i]["close"] - data[i+1]["close"]
    percent_change = (diff / data[i]["close"]) * 100
    d["percent_change"] = percent_change


def main():
  with open("igv_historical_prices.json", "r") as historical:
    data = json.load(historical)

  data.reverse()

  calc_change(data)

  with open("igv_historical_prices.json", "w") as new_historical:
    json.dump(data, new_historical)


if __name__ in '__main__':
  main()
