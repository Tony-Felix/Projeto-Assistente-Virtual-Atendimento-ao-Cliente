import os
import time
import google.generativeai as genai
import gradio as gr
from google.api_core.exceptions import InvalidArgument
from service_functions import (
    atualizar_status_pedido,
    registrar_reclamacao,
    gerar_cupom_desconto
)

genai.configure(api_key=os.environ["GEMINI_API"])

model_if_magic = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={"temperature": 0.3},
    tools=[atualizar_status_pedido, registrar_reclamacao, gerar_cupom_desconto]
)

chat = model_if_magic.start_chat()


def ia_decision():
    business_rules = """
      Atue como um assistente virtual que possa Responder perguntas dos
      clientes sobre produtos, pedidos e políticas de uma loja online de
      eletrônicos. Você pode Processar arquivos enviados pelos clientes,
      como comprovantes de pagamento ou imagens de produtos com defeito.
      Tambem pode realizar ações específicas chamando funções internas,
      como atualizar o status de um pedido, gerar um cupom de desconto ou
      registrar uma reclamação sobre um produto. Você deve decidir quando
      chamar as funções com base nas interações com o cliente.
      Você deve seguir as seguintes regras ao interagir com os clientes:
    1. Consulta de Pedidos:
    Se o cliente perguntar sobre o status de um pedido, a você deve fornecer
    as informações correspondentes. Se necessário, chamar a função
    atualizar_status_pedido para atualizar o status.
    2. Reclamações sobre Produtos:
    Se o cliente enviar uma imagem de um produto com defeito, a você deve
    registrar a reclamação, chamar a função registrar_reclamacao e fornecer um
    número de protocolo ao cliente.
    3. Oferecer Descontos:
    Se o cliente for recorrente ou estiver insatisfeito, você pode oferecer um
    cupom de desconto. Chamar a função gerar_cupom_desconto e enviar o código
    ao cliente.
    4. Políticas da Loja:
    Você deve ser capaz de responder perguntas sobre políticas de devolução,
    troca, etc.
    5. Mensagens de Erro ou Não Compreensão:
    Se você não entender a solicitação, deve pedir esclarecimentos ao cliente.
    Não minta ou finja que chamou as funções. Sempre chame as funções se
    parecer que deve.
    """
    response = chat.send_message(
        f"Regras de negócio: {business_rules}"
    )
    # Mensagem adicional para incentivar a reflexão da IA
    chat.send_message(
        "Se ao interagir com um cliente não tiver chamado nenhuma função, "
        "reflita se deve fazê-lo ou não. Lembre-se que você é um assistente"
        "virtual que pode responder perguntas e chamar as funções adequadas "
        "para cada usuario.."
    )
    # Retorna a resposta da IA
    return response.text


ia_decision()


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


# Wrapper para integrar o chat com o Gradio
def gradio_wrapper(message, _history):
    prompt = assemble_prompt(message)
    try:
        response = chat.send_message(prompt)
    except InvalidArgument as e:
        response = chat.send_message(
            f"O usuário te enviou um arquivo para você ler e obteve o erro: "
            f"{e}. Pode explicar o que houve e dizer quais tipos de "
            "arquivos você dá suporte? Assuma que a pessoa não sabe "
            "programação e não quer ver o erro original. Explique de forma "
            "simples e concisa."
        )
    return response.text


# Crie e lance a interface do chat com suporte a arquivos
chat_interface = gr.ChatInterface(
    fn=gradio_wrapper, title="Chatbot! 📞 customer service 💬", multimodal=True
)
# Inicie a interface
chat_interface.launch(server_name="127.0.0.1", server_port=7860)
