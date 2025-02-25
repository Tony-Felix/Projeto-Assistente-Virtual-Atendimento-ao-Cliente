import gradio as gr
from gemini_config import gradio_wrapper, ia_decision

ia_decision()

# Crie e lance a interface do chat com suporte a arquivos
chat_interface = gr.ChatInterface(
    fn=gradio_wrapper, 
    title="Chatbot! ☎️ Assistente Virtual 💬",
    multimodal=True
)
# Inicie a interface
chat_interface.launch(server_name="127.0.0.1", server_port=7860)
