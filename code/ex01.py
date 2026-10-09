import hmac


class Remetente:
    def __init__(self, chave_secreta):
        self.chave_secreta = chave_secreta

    def enviar_mensagem(self, mensagem):
        """Gera uma tag HMAC para autenticar a mensagem"""
        tag_mac = hmac.new(
            self.chave_secreta.encode(),
            mensagem.encode(),
            'sha256'
        ).hexdigest()

        return mensagem, tag_mac


class Destinatario:
    def __init__(self, chave_secreta):
        self.chave_secreta = chave_secreta

    def verificar_mensagem(self, mensagem, tag_mac):
        """Verifica a integridade e a autenticidade perante quem conhece a chave."""
        tag_mac_calculada = hmac.new(
            self.chave_secreta.encode(),
            mensagem.encode(),
            'sha256'
        ).hexdigest()

        return hmac.compare_digest(tag_mac_calculada, tag_mac)


class Invasor:
    def __init__(self, mensagem_interceptada, tag_interceptada):
        self.mensagem_interceptada = mensagem_interceptada
        self.tag_mac_interceptada = tag_interceptada

    def alterar_mensagem(self):
        """Altera um caractere da mensagem e mantém a tag original interceptada."""
        mensagem_alterada = self.mensagem_interceptada.replace('!', '?', 1) 
        return mensagem_alterada, self.tag_mac_interceptada


CHAVE_SECRETA_SIMETRICA = "ULTRASECRETO"

Alice = Remetente(CHAVE_SECRETA_SIMETRICA)
Bob = Destinatario(CHAVE_SECRETA_SIMETRICA)

mensagem_alice, tag_hmac = Alice.enviar_mensagem(
    "Oi Bob, Alice aqui! Como você está?"
)

print("\nChave secreta usada na simulação:")
print(Alice.chave_secreta)

print("\nMensagem de Alice:")
print(mensagem_alice)

print("\nTag HMAC gerada:")
print(tag_hmac)

print("\nA mensagem original passou na verificação de Bob?")
print(Bob.verificar_mensagem(mensagem_alice, tag_hmac))

print("\nO que acontece se um invasor mudar a mensagem?")

# Cenario de invasao

Eve = Invasor(mensagem_alice, tag_hmac)
mensagem_eve, tag_interceptada = Eve.alterar_mensagem()

print("\nMensagem alterada por Eve:")
print(mensagem_eve)

print("\nA mensagem alterada passou na verificação de Bob?")
print(Bob.verificar_mensagem(mensagem_eve, tag_interceptada))