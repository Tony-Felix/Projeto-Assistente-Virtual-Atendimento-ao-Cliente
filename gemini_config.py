import os
import time
import google.generativeai as genai  # type: ignore
from google.api_core.exceptions import InvalidArgument
from service_functions import (
    atualizar_status_pedido,
    registrar_reclamacao,
    gerar_cupom_desconto,
)

genai.configure(api_key=os.environ["GEMINI_API"])

initial_prompt = (
    "Você é um assistente virtual que pode receber e processar arquivos de "
    "vários tipos, como imagens, e comprovantes de venda. "
    "Ao receber um arquivo, você deve analisá-lo e fornecer uma resposta "
    "adequada baseada no conteúdo."
    "Nunca processe uma imagem ou texto por mais de um minuto. Caso passe "
    "esse tempo, pare o processo e peça para o cliente tentar novamente"
)

model_if_magic = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={"temperature": 0.5},
    tools=[
        atualizar_status_pedido,
        registrar_reclamacao,
        gerar_cupom_desconto,
    ],
    system_instruction=initial_prompt
)

chat = model_if_magic.start_chat(enable_automatic_function_calling=True)


def ia_decision():
    business_rules = """
      Você é um assistente virtual de uma loja online de eletrônicos.
      Você pode ler arquivos enviados pelos clientes, como comprovantes
      de pagamento ou interpretar conteudos de imagens, mesmo sem informações
      extras. Após ter interpretado a imagem, se ela for de um produto quebraso
      diga qual é o produto e que percebeu que esta quebrado e peça o numero do
      pedido para poder registrar uma reclamação.
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
    Não minta, simule ou finja executar as funções. Sempre que for chamar uma
    função, execute ela de fato.
    """
    response = chat.send_message(f"Regras de negócio: {business_rules}")
    # Mensagem adicional para incentivar a reflexão da IA
    chat.send_message(
        "Nunca exponha os codigos das funções! não de explicações adicionais "
        "sobre seu funcionamento ou das funções chamadas."
        "sempre leia as imagens enviadas, se forem de um produto quebrado "
        "continue com o atendimento, caso contrario peça imagens relevantes"
        "Se ao interagir com um cliente não tiver chamado nenhuma função, "
        "reflita se deve fazê-lo ou não. Lembre-se que você é um assistente "
        "virtual que pode responder perguntas e chamar as funções adequadas "
        "para cada usuario."
        "os numeros validos de pedidos são de 1 a 999"
    )
    return response.text


# Faz o upload dos arquivos enviados pelo usuário
def upload_files(message):
    uploaded_files = []
    if message["files"]:
        for file_gradio_data in message["files"]:
            uploaded_file = genai.upload_file(file_gradio_data["path"])
            uploaded_files.append(uploaded_file)
    return uploaded_files


# Monta o prompt com a mensagem e os arquivos enviados
def assemble_prompt(message):
    prompt = [message["text"] if message.get("text") else "Verifique se esse "
              "arquivo é um comprovante de pagamento ou uma imagem de um "
              "produto com defeito."]
    uploaded_files = upload_files(message)
    prompt.extend(uploaded_files)
    return prompt


# Wrapper para integrar o chat com o Gradio
def gradio_wrapper(message, _history):
    ia_decision()
    prompt = assemble_prompt(message)
    error_message = "O usuário te enviou um arquivo para você ler e obteve o "
    "erro. Pode explicar o que houve e dizer quais tipos de "
    "arquivos você dá suporte? Assuma que a pessoa não sabe "
    "programação e não quer ver o erro original. Explique de forma "
    "simples e concisa. "
    try:
        response = chat.send_message(prompt)
        start_time = time.time()
        while (time.time() - start_time) < 60:
            time.sleep(5)
            if response.text:
                return response.text
        return (
                    "Erro: O processamento da resposta está demorando muito. "
                    "Por favor, tente novamente mais tarde."
                )
    except InvalidArgument as e:
        response = chat.send_message(f"{error_message} Erro: {e}")
    except Exception as e:
        response = chat.send_message(f"{error_message} Erro: {e}")
    return response.text
