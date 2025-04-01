# Chatbot! 💬 Assistente Virtual 💬

Este projeto implementa um chatbot interativo utilizando o poder do Google Gemini para fornecer respostas inteligentes e suporte multimodal (texto e arquivos). A interface do chatbot é construída com Gradio, e a aplicação web principal é gerenciada com Flask.

## Visão Geral

A aplicação oferece duas formas de interação:

1.  **Interface Web Principal (Flask):** Uma página inicial informativa (rota `/`) que apresenta uma simulação de loja de eletrônicos e fornece um link para a interface de chat com o assistente virtual.
2.  **Interface de Chat (Gradio):** Uma interface de chat rica e interativa (rota `/chat`, que redireciona para `http://127.0.0.1:7860`) onde os usuários podem conversar com o assistente virtual, enviando tanto texto quanto arquivos (imagens e comprovantes). O Google Gemini, configurado através do módulo `gemini_config.py`, processa as entradas e gera as respostas, além de ter acesso a ferramentas para atualizar status de pedidos, registrar reclamações e gerar cupons de desconto.

## Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **Flask:** Framework web micro para construir a aplicação web principal e gerenciar a rota inicial, além de servir arquivos estáticos.
* **Gradio:** Biblioteca para criar a interface de usuário interativa para o chatbot, permitindo interação multimodal.
* **Google Gemini:** Modelo de linguagem grande para geração de texto, compreensão de arquivos e chamada de funções (`gemini-1.5-flash`).
* **`google-generativeai`:** Biblioteca do Google para interagir com os modelos Gemini.
* **`python-dotenv`:** Utilizado para carregar a chave de API do Gemini a partir de um arquivo `.env`.
* **Threading:** Utilizado para executar o servidor Flask e a interface Gradio simultaneamente.

## Pré-requisitos

* Python 3.x instalado.
* Pip (gerenciador de pacotes do Python) instalado.
* [Opcional] Um ambiente virtual Python (recomendado para isolar dependências).
* Uma chave de API do Google Gemini. Você pode obter uma em [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey).

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio](https://www.google.com/search?q=https://github.com/seu-usuario/seu-repositorio) # Substitua pelo link do seu repositório
    cd [nome do seu repositório]
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Linux/macOS
    venv\Scripts\activate  # No Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure a chave de API do Google Gemini:**
    * Crie um arquivo chamado `.env` na raiz do seu projeto.
    * Adicione a sua chave de API do Gemini neste arquivo, conforme o exemplo em `.env.example`:
        ```
        GEMINI_API=SUA_CHAVE_DE_API_DO_GEMINI_AQUI
        ```
        *(Substitua `SUA_CHAVE_DE_API_DO_GEMINI_AQUI` pela sua chave real.)*

5.  **[Opcional] Crie um diretório para arquivos estáticos:**
    * Se você tiver arquivos CSS ou outras assets estáticas para a página inicial, crie um diretório chamado `static` na raiz do seu projeto.
    * Coloque seus arquivos estáticos (como `style.css` mencionado no `index.html`) dentro deste diretório.

## Configuração Adicional

* O arquivo `gemini_config.py` contém a configuração para interagir com o modelo Gemini, incluindo o prompt inicial, a seleção do modelo (`gemini-1.5-flash`), a temperatura e a definição das ferramentas (funções) que o modelo pode utilizar (`atualizar_status_pedido`, `registrar_reclamacao`, `gerar_cupom_desconto` definidas em `service_functions.py`).
* O arquivo `service_functions.py` implementa as funções que o Gemini pode chamar. Estas funções simulam operações como atualizar o status de um pedido, registrar uma reclamação e gerar um cupom de desconto.
* O diretório `templates` contém os arquivos HTML para a aplicação Flask. Atualmente, inclui o `index.html` que simula a página inicial de uma loja de eletrônicos com um link para o chatbot.

## Execução

1.  **Execute a aplicação:**
    ```bash
    python app.py
    ```
    Isso iniciará dois servidores:
    * Um servidor Flask rodando em `http://127.0.0.1:5000`.
    * Uma interface Gradio rodando em `http://127.0.0.1:7860`.

2.  **Acesse a aplicação:**
    * Abra seu navegador web e acesse `http://127.0.0.1:5000` para ver a página inicial da loja de eletrônicos com um link para falar com o assistente virtual.
    * Clique no link "Fale com nosso assistente virtual" ou acesse diretamente `http://127.0.0.1:7860` no seu navegador para interagir com o chatbot.

## Utilização

* Ao acessar `http://127.0.0.1:5000`, você verá uma página inicial simulando uma loja de eletrônicos. O link "Fale com nosso assistente virtual" redirecionará você para a interface de chat do Gradio.
* Na interface Gradio (`http://127.0.0.1:7860`), você poderá interagir com o assistente virtual conforme descrito anteriormente (enviando texto e arquivos para consultar pedidos, registrar reclamações, etc.).
