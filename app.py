from flask import Flask, render_template, request, jsonify
import sentiment_analysis

app = Flask(__name__)
sentiment_analysis = sentiment_analysis.SentimentAnalysis()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        selected_option = request.json["dropdown"]
        prediction = sentiment_analysis.getSentiment(selected_option)
        return jsonify({"prediction": prediction})
    return render_template("home.html")


@app.route("/get_prediction", methods=["GET", "POST"])
def get_prediction():
    selected_option = request.json["dropdown"]
    prediction = sentiment_analysis.getSentiment(selected_option)
    return jsonify({"prediction": prediction})


if __name__ == "__main__":
    app.run(debug=True)
