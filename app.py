import threading
from flask import Flask, redirect, render_template  # type: ignore
import gradio as gr  # type: ignore
from gemini_config import gradio_wrapper

app = Flask(__name__)


# Rotas básicas
@app.route("/")
def index():
    return render_template("index.html")


# Crie e lance a interface do chat com suporte a arquivos
chat_interface = gr.ChatInterface(
    fn=gradio_wrapper,
    title="Chatbot! 💬 Assistente Virtual 💬",
    multimodal=True
)


# Rota do chat
@app.route("/chat")
def chat_render():
    return redirect("http://127.0.0.1:7860")


def run_flask():
    app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    # app.run(debug=True)
    threading.Thread(target=run_flask, daemon=True).start()
    chat_interface.launch(
        server_name="127.0.0.1", server_port=7860
    )
