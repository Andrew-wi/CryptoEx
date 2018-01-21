import csv
import urllib.request
import json

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # reject symbol if it starts with caret
    if symbol.startswith("^"):
        return None

    # Reject symbol if it contains comma
    if "," in symbol:
        return None

    # Query Yahoo for quote
    # http://stackoverflow.com/a/21351911
    try:

        # get json
        url = "https://api.coinmarketcap.com/v1/ticker/?convert=EUR&limit=10"
        data = json.load(urllib.request.urlopen(url))

        stock = {}
        # get the specific stock
        for x in data:
            if x["symbol"] == symbol:
                print(x["symbol"])
                stock = x

        print(stock)

        # Return stock's name (as a str), price (as a float), and (uppercased) symbol (as a str)
        return {
            "name": stock["name"],
            "price": float(stock["price_usd"]),
            "symbol": stock["symbol"]
        }

    except:
        pass

    # # Query Alpha Vantage for quote instead
    # # https://www.alphavantage.co/documentation/
    # try:

    #     # GET CSV
    #     url = f"https://www.alphavantage.co/query?apikey=NAJXWIA8D6VN6A3K&datatype=csv&function=TIME_SERIES_INTRADAY&interval=1min&symbol={symbol}"
    #     webpage = urllib.request.urlopen(url)

    #     # Parse CSV
    #     datareader = csv.reader(webpage.read().decode("utf-8").splitlines())

    #     # Ignore first row
    #     next(datareader)

    #     # Parse second row
    #     row = next(datareader)

    #     # Ensure stock exists
    #     try:
    #         price = float(row[4])
    #     except:
    #         return None

    #     # Return stock's name (as a str), price (as a float), and (uppercased) symbol (as a str)
    #     return {
    #         "name": symbol.upper(), # for backward compatibility with Yahoo
    #         "price": price,
    #         "symbol": symbol.upper()
    #     }

    # except:
    #     return None


def usd(value):
    """Formats value as USD."""
    return f"${value:,.2f}"
