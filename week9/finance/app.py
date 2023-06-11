import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd, registerTransaction, checkBalance, getBalance, createIndexTable, createHistoryTable, search

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    totalSummary = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]

    # create summary table

    summaryList, totalSummary = createIndexTable(totalSummary, db)

    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    displayCash = usd(cash[0]["cash"])
    message = "Loged In"
    totalSummary = usd(totalSummary)

    return render_template("index.html", summaryList=summaryList, cash=displayCash, message=message, total=totalSummary)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # check for input errors

        if not request.form.get("symbol"):
            return apology("Please enter a symbol", 403)
        elif lookup(request.form.get("symbol")) == None:
            return apology("Please enter an existing symbol")
        elif not request.form.get("shares"):
            return apology("Enter amount of shares", 400)

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Shares must be an integer")

        if shares < 0:
            return apology("Shares must be a positive integer")

        # variable declaration

        shares = int(request.form.get("shares"))
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        curPrice = quote["price"]  # float
        shares = int(shares)
        total = curPrice * shares

        balance = getBalance(db)

        if checkBalance(total, balance) == False:
            return apology("You don't have enough cash in your wallet to buy these shares")

        displayCash, new_balance = registerTransaction(symbol, shares, total, curPrice, balance, db)

        totalSummary = new_balance

        summaryList, totalSummary = createIndexTable(totalSummary, db)

        totalSummary = usd(totalSummary)

        message = "Bought"

        return render_template("index.html", summaryList=summaryList, cash=displayCash, message=message, total=totalSummary)

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    balance = getBalance(db)

    transactionHistory = createHistoryTable(db)

    # create variable for total that can be changed into usd-format

    return render_template("history.html", transactions=transactionHistory)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        cash = usd(rows[0]["cash"])
        message = "Loged In"

        # Redirect user to home page
        return render_template("index.html", cash=cash, message=message)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # check for input errors when POST

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        elif lookup(request.form.get("symbol")) == None:
            return apology("Symbol not found", 400)

        quote = lookup(request.form.get("symbol"))
        price = usd(quote["price"])
        return render_template("quoted.html", price=price, quote=quote)
    else:
        return render_template("quote.html")  # shows template if not POST (Submit-Button not clicked)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # check for input errors

        if not request.form.get("username") or db.execute("SELECT * from users WHERE username = ?", request.form.get("username")):
            return apology("must provide username", 400)

        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password", 400)

        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # insert new registered user into database

        db.execute("INSERT INTO users (username, hash) VALUES (?,?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

    else:
        return render_template("register.html")

    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        # check for input errors

        if not request.form.get("shares"):
            return apology("Please enter amount of shares")
        elif not request.form.get("symbol"):
            return apology("Please select a symbol")
        elif int(request.form.get("shares")) < 0:
            return apology("Please enter positive integer")

        symbol = request.form.get("symbol")

        # check how many shares of each symbol are in the wallet

        shareSumList = db.execute(
            "SELECT SUM(shares) FROM transactions WHERE symbol = :curSymbol AND user_id = :user_id", curSymbol=symbol, user_id=session["user_id"])

        shareSum = int(shareSumList[0]["SUM(shares)"])
        shares = int(request.form.get("shares"))

        if shares > shareSum:
            return apology("You don't have that much Shares")

        # get information about stock from API

        quote = lookup(symbol)
        curPrice = quote["price"]  # float
        shares = (-1) * int(request.form.get("shares"))
        total = curPrice * shares

        balance = getBalance(db)

        displayCash, totalSummary = registerTransaction(symbol, shares, total, curPrice, balance, db)

        summaryList, totalSummary = createIndexTable(totalSummary, db)

        totalSummary = usd(totalSummary)

        message = "Sold"

        return render_template("index.html", summaryList=summaryList, cash=displayCash, message=message, total=totalSummary)

    else:
        buySymbols = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])

        return render_template("sell.html", buyTransactions=buySymbols)


@app.route("/cash", methods=["GET", "POST"])
@login_required
def addCash():
    """Add additional cash to stock"""

    if request.method == "POST":

        # check for input errors

        if not request.form.get("cash"):
            return apology("Please enter amount of cash")

        elif int(request.form.get("cash")) < 0:
            return apology("Please enter positive integer")

        cash = int(request.form.get("cash"))

        balance = getBalance(db)

        new_balance = balance + cash

        db.execute("UPDATE users SET cash = :curCash WHERE id = :user_id", curCash=new_balance, user_id=session["user_id"])

        transactions = db.execute("SELECT * FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])

        totalSummary = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]

        # create summary table

        summaryList, totalSummary = createIndexTable(totalSummary)

        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        displayCash = usd(cash[0]["cash"])

        message = "Cash was successfully added to your wallet!"

        totalSummary = usd(totalSummary)

        return render_template("index.html", summaryList=summaryList, cash=displayCash, message=message, total=totalSummary)

    else:
        return render_template("cash.html")  # template stays until submit-button is clicked


@app.route("/symbols", methods=["GET", "POST"])
@login_required
def searchSymbols():
    """search for a symbol via the company name"""

    if request.method == "POST":
        if not request.form.get("name"):
            return apology("Please enter Company Name")

        name = request.form.get("name")

        symbol = search(name)

        quote = lookup("symbol")

        companyName = quote["name"]

        if name in companyName:
            return render_template("symbolsearch.html", name = companyName, symbol = symbol)

        else:
            return apology("Company not found")

    else:
        return render_template("symbols.html")