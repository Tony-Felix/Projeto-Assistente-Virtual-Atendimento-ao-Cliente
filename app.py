from flask import Flask, redirect, render_template  # type: ignore

app = Flask(__name__)


# Rotas básicas
@app.route("/")
def index():
    return render_template("index.html")


# Rota do chat
@app.route("/chat")
def chat_render():
    return redirect("http://127.0.0.1:7860")


if __name__ == "__main__":
    app.run(debug=True)
