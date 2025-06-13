from flask import Flask, render_template, request, jsonify
from src.chatbot import odpovedet
from src.database import get_weather_history

app = Flask(__name__, static_url_path='/static', static_folder='static')


@app.route("/", methods=["GET", "POST"])
def index():
    historie = get_weather_history()
    odpoved = ""
    if request.method == "POST":
        zprava = request.form.get("zprava", "").strip()
        if zprava:
            odpoved = odpovedet(zprava)
            timestamp = request.form.get("timestamp", "")
            historie = get_weather_history()  # Aktualizace historie
            return jsonify({"odpoved": odpoved, "timestamp": timestamp})
    return render_template("index.html", odpoved=odpoved, historie=historie)


@app.route("/clear_history", methods=["POST"])
def clear_history():
    # Logika pro vymazání historie (např. smazání databáze nebo tabulky)
    # Tady by měla být implementace v src.database.clear_history()
    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
