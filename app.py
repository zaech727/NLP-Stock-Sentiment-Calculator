from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sentiment_analysis
import re
from stock_price import get_stock_price

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.secret_key = 'apple123'
db = SQLAlchemy(app)

def time_diff_in_minutes(time):
    now = datetime.utcnow()
    diff = now - time
    return diff.seconds//60

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    sentiment = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Stock %r>" % self.symbol + " " + str(self.sentiment)

sentiment_analysis = sentiment_analysis.SentimentAnalysis()

def getStockSentiment(stock_symbol):
    sentiment_value = sentiment_analysis.getSentiment(stock_symbol)
    return round(sentiment_value, 3)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        stock_symbol = request.form["content"].strip().upper()
        return create_stock(stock_symbol)
    else:
        stocks = Stock.query.order_by(Stock.symbol).all()
        stock_prices = {}
        for stock in stocks:
            symbol = stock.symbol
            stock_prices[symbol] = get_stock_price(symbol)

        return render_template("home.html", stocks=stocks, stock_prices=stock_prices, time_diff_in_minutes=time_diff_in_minutes)

def create_stock(stock_symbol):
    stock_symbol = stock_symbol.strip().upper()

    # Check if input is blank or invalid
    if not stock_symbol:
        flash("Error: You cannot submit a blank stock symbol.")
        return redirect("/")
    if not re.match(r"^[A-Z]{1,5}$", stock_symbol):
        flash(
            "Error: Invalid stock symbol. Please enter 1-5 uppercase alphabetical characters."
        )
        return redirect("/")

    stock = Stock.query.filter_by(symbol=stock_symbol).first()
    if stock:
        flash("Error: This stock symbol has already been added.")
        return redirect("/")

    flash("Processing: fetching sentiment for " + stock_symbol)
    new_stock = Stock(symbol=stock_symbol, sentiment=getStockSentiment(stock_symbol))

    try:
        db.session.add(new_stock)
        db.session.commit()
        flash("Success: " + stock_symbol + " added successfully!")
    except:
        flash("Error: Unable to add stock to database.")

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    stock_entry = Stock.query.get_or_404(id)

    try:
        db.session.delete(stock_entry)
        db.session.commit()
        return redirect("/")
    except:
        return "Unable to delete stock from database"

@app.route("/update/<int:id>")
def update(id):
    stock_entry = Stock.query.get_or_404(id)

    try:
        stock_entry.sentiment = getStockSentiment(stock_entry.symbol)
        stock_entry.created = datetime.utcnow()
        db.session.commit()
        return redirect("/")
    except:
        return "Unable to update stock in database"

if __name__ == "__main__":
    app.run(debug=True)