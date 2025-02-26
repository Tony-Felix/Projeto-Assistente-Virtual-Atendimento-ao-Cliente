import datetime
import secrets
import string


def atualizar_status_pedido() -> dict:
    """
    Atualiza o status do pedido
    """
    status_opcoes = [
        "Pedido entregue",
        "Pedido na transportadora",
        "Pedido a caminho"
    ]
    status_atual = secrets.choice(status_opcoes)

    print(f"Status atualizado: {status_atual}")
    return {"status": status_atual}


def registrar_reclamacao() -> str:
    """
    registra a reclamação
    """
    print("reclamação registrada")
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # Gera um código aleatório de 4 dígitos
    codigo_aleatorio = secrets.randbelow(10000)  # Número entre 0 e 9999
    protocolo = f"{timestamp}-{codigo_aleatorio:04d}"
    return protocolo


def gerar_cupom_desconto() -> str:
    """
    Gera cupom de desconto
    """
    caracteres = string.ascii_uppercase + string.digits
    codigo = ''.join(secrets.choice(caracteres) for _ in range(8))
    print("cupom de desconto gerado")
    return f"{codigo}-DESC30%"
