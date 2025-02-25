import time
from flask import Flask, render_template
import os
import google.generativeai as genai
from service_functions import (
    atualizar_status_pedido,
    registrar_reclamacao,
    gerar_cupom_desconto
)

app = Flask(__name__)

genai.configure(api_key=os.environ["GEMINI_API"])

model_if_magic = genai.GenerativeModel(
    "gemini-1.5-flash",
    tools=[atualizar_status_pedido, registrar_reclamacao, gerar_cupom_desconto]
)

chat = model_if_magic.start_chat()


# Faz o upload dos arquivos enviados pelo usuário
def upload_files(message):
    uploaded_files = []
    if message["files"]:
        for file_gradio_data in message["files"]:
            uploaded_file = genai.upload_file(file_gradio_data["path"])
            while uploaded_file.state.name == "PROCESSING":
                time.sleep(5)
                uploaded_file = genai.get_file(uploaded_file.name)
            uploaded_files.append(uploaded_file)
    return uploaded_files


# Monta o prompt com a mensagem e os arquivos enviados
def assemble_prompt(message):
    prompt = [message["text"]]
    uploaded_files = upload_files(message)
    prompt.extend(uploaded_files)
    return prompt


# Rotas básicas
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
