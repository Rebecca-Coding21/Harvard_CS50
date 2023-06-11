import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from cs50 import SQL


def apology(message, code=400):
    """Render message as an apology to user."""
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

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def registerTransaction(symbol, shares, total, curPrice, balance, db):

    # variable declaration

    quote = lookup(request.form.get("symbol"))
    name = quote["name"]

    # calculate new balance according to bought/sold stocks

    new_balance = balance - total

    symbol = str.upper(request.form.get("symbol"))

    db.execute("UPDATE users SET cash = :curCash WHERE id = :user_id", curCash=new_balance, user_id=session["user_id"])

    # insert new transaction into database

    db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, datetime, total) VALUES (:user_id, :symbol1 ,:name1, :shares1, :price, CURRENT_TIMESTAMP, :total)",
               user_id=session["user_id"], symbol1=symbol, name1=name, shares1=shares, price=curPrice, total=total)

    # declare variables for templates

    displayCash = usd(new_balance)

    return displayCash, new_balance


def createIndexTable(totalSummary, db):
    """ create summary table """

    summaryList = []
    symbols = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])

    for s in symbols:
        s = s["symbol"]
        shareSumList = db.execute(
            "SELECT SUM(shares), name FROM transactions WHERE symbol = :curSymbol AND user_id = :user_id", curSymbol=s, user_id=session["user_id"])
        shareSum = int(shareSumList[0]["SUM(shares)"])
        name = shareSumList[0]["name"]
        quote = lookup(s)
        totalSummary += quote["price"] * shareSum

        entry = {
            "symbol": s,
            "name": name,
            "shares": int(shareSum),
            "price": usd(quote["price"]),
            "total": usd(quote["price"] * shareSum)
        }
        summaryList.append(entry)

    return summaryList, totalSummary


def getBalance(db):

    # get cash of current user

    user = db.execute("SELECT cash FROM users WHERE id = :user_name", user_name=session["user_id"])
    balance = user[0]["cash"]

    return balance


def checkBalance(total, balance):

    if balance < total:
        return False

    return True


def createHistoryTable(db):
    """ create summary table for history template"""

    # 1. Get all transactions
    # 2. Loop transactions (list of dicts)
    # 3. override total with usd(total) (dictionary)
    #   4. return transactions

    transactionHistory = db.execute(
        "SELECT symbol, name, shares, price, total, datetime FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])

    for t in transactionHistory:
        if t["total"] < 1:
            t["total"] = (-1) * t["total"]

        t["total"] = usd(t["total"])

    return transactionHistory


def search(companyName):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(companyName)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()

        if companyName == quote["companyName"]:
            symbol = quote["symbol"]
        else:
            return apology("Company Name does not exist")

        return symbol
        #{
         #   "name": quote["companyName"],
          #  "price": float(quote["latestPrice"]),
          #  "symbol": quote["symbol"]
       # }
    except (KeyError, TypeError, ValueError):
        return None