import requests
from bs4 import BeautifulSoup


def get_stock_data(ticker_symbol):
    yahoo_url = f"https://finance.yahoo.com/quote/{ticker_symbol}"
    yahoo_response = requests.get(yahoo_url)
    yahoo_soup = BeautifulSoup(yahoo_response.text, "html.parser")
    valuation_tag = yahoo_soup.find(
        "div", {"class": "Fw(b) Fl(end)--m Fz(s) C($primaryColor)"}
    )
    valuation = valuation_tag.text if valuation_tag is not None else None

    # Use a different website to get the stock price
    other_url = "https://www.marketwatch.com/investing/stock/" + ticker_symbol
    other_response = requests.get(other_url)
    other_soup = BeautifulSoup(other_response.text, "html.parser")
    price_tag = other_soup.find("bg-quote", {"class": "value"})
    price = price_tag.text if price_tag is not None else None

    return price, valuation


def is_overvalued(ticker_symbol):
    stock_price, valuation = get_stock_data(ticker_symbol)
    return stock_price, "overvalued" in valuation.lower(), valuation


ticker_symbol = input("Enter the stock ticker: ").upper()
stock_price, is_overvalued, valuation = is_overvalued(ticker_symbol)
if is_overvalued:
    print(
        f"{ticker_symbol} is overvalued. Current price: {stock_price}. Valuation: {valuation} "
    )
else:
    print(
        f"{ticker_symbol} is undervalued. Current price: {stock_price}. Valuation: {valuation}"
    )
