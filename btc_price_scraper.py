import json
import arrow
import requests
import multiprocessing as mp
from pprint import pprint
from bs4 import BeautifulSoup


HEADERS = [ "date", "open", "high", "low", "close", "volume", "market_cap" ]


def get_data():
  # Get BTC price data from 2013-12-27, the first date that has
  # trading volume data available
  url = "https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20131227&end=20190110"

  r = requests.get(url)
  soup = BeautifulSoup(r.text, "lxml")

  # I could do proper HTML tree traversal, but this is faster
  div = soup.find("div", { "id": "historical-data" })
  tbody = div.find("tbody")
  rows = tbody.find_all("tr")

  return rows


def parse_data(row):
  # Quick one-liner to create a dict object by calling zip() on HEADERS
  # and each td in the row.
  parsed_row = dict(zip(HEADERS, [td.text for td in row.find_all("td")]))

  # the next two loops just mutate the dict fields to their proper types
  for field in [ "open", "high", "low", "close" ]:
    parsed_row[field] = float(parsed_row[field])

  # technically, using the same loop variable can cause some funky memory
  # un-fun things, but it's probably fine here.
  for field in [ "volume", "market_cap" ]:
    parsed_row[field] = int(parsed_row[field].replace(",", ""))

  # use arrow to reformat the date field to ISO-8601 format
  parsed_row["date"] = arrow.get(parsed_row["date"], "MMM DD, YYYY").format("YYYY-MM-DD")

  return parsed_row


def main():
  data = get_data()
  parsed_data = [parse_data(d) for d in data]

  with open("historical_btc_prices.json", "w") as historical:
    json.dump(parsed_data, historical)


if __name__ in '__main__':
  main()
