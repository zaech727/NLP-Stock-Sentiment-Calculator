from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sentiment_analysis

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    sentiment = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Stock %r>" % self.symbol + " " + str(self.sentiment)


# create database
# with app.app_context():
#     db.create_all()
# exit()

sentiment_analysis = sentiment_analysis.SentimentAnalysis()


def getStockSentiment(stock_symbol):
    sentiment_value = sentiment_analysis.getSentiment(stock_symbol)
    return round(sentiment_value, 3)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        stock_symbol = request.form["content"]
        stock = Stock.query.filter_by(symbol=stock_symbol).first()
        if not stock:
            new_stock = Stock(
                symbol=stock_symbol, sentiment=getStockSentiment(stock_symbol)
            )

            try:
                db.session.add(new_stock)
                db.session.commit()
                return redirect("/")
            except:
                return "Unable to add stock to database"
        return redirect("/")

    else:
        stocks = Stock.query.order_by(Stock.symbol).all()
        return render_template("home.html", stocks=stocks)


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
