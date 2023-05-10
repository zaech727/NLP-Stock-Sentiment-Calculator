from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
web_scraper = WebScraper()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        selected_option = request.json["dropdown"]
        prediction = web_scraper.get_prediction(selected_option)
        return jsonify({"prediction": prediction})
    return render_template("home.html")

@app.route("/get_prediction", methods=["POST"])
def get_prediction():
    selected_option = request.json["dropdown"]
    prediction = web_scraper.get_prediction(selected_option)
    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    app.run(debug=True)
