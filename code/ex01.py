import hmac


class Usuario:
    def __init__(self, chave_secreta=None):
        self.chave_secreta = chave_secreta

    def calcular_tag(self, mensagem):
        """Calcula o HMAC-SHA256 usando a chave secreta deste usuário."""
        if self.chave_secreta is None:
            raise ValueError("Este usuário não possui a chave secreta.")

        return hmac.new(
            self.chave_secreta.encode('utf-8'),
            mensagem.encode('utf-8'),
            'sha256'
        ).hexdigest()

    def enviar_mensagem(self, mensagem):
        """Retorna a mensagem original junto com sua tag HMAC."""
        tag_mac = self.calcular_tag(mensagem)
        return mensagem, tag_mac

    def verificar_mensagem(self, mensagem, tag_mac):
        """Recalcula a tag e compara com a recebida."""
        tag_mac_calculada = self.calcular_tag(mensagem)
        return hmac.compare_digest(tag_mac_calculada, tag_mac)

    def alterar_mensagem(self, mensagem):
        """Altera um caractere para simular uma adulteração."""
        return mensagem.replace('!', '?', 1)


CHAVE_SECRETA_SIMETRICA = "ULTRASECRETO"

Alice = Usuario(CHAVE_SECRETA_SIMETRICA)
Bob = Usuario(CHAVE_SECRETA_SIMETRICA)
Eve = Usuario()


# Cenário 1: mensagem original e tag de Alice.
mensagem_alice, tag_hmac = Alice.enviar_mensagem(
    "Oi Bob, Alice aqui! Como você está?"
)

print("\n--- Cenário 1: mensagem original de Alice ---")

print("\nChave secreta usada na simulação:")
print(CHAVE_SECRETA_SIMETRICA)

print("\nMensagem:")
print(mensagem_alice)

print("\nTag HMAC:")
print(tag_hmac)

print("\nA verificação passou? Esperado: True")
print(Bob.verificar_mensagem(mensagem_alice, tag_hmac))


# Cenário 2: Eve altera a mensagem e mantém a tag original.
mensagem_eve = Eve.alterar_mensagem(mensagem_alice)
tag_interceptada = tag_hmac

print("\n--- Cenário 2: mensagem alterada e tag original ---")

print("\nMensagem original:")
print(mensagem_alice)

print("\nMensagem recebida por Bob:")
print(mensagem_eve)

print("\nA verificação passou? Esperado: False")
print(Bob.verificar_mensagem(mensagem_eve, tag_interceptada))