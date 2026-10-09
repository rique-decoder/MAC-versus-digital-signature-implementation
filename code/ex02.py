import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding, utils


class Usuario:
    def __init__(self):
        self.chave_publica = None
        self.chave_privada = None

    def gerar_chaves_assimetricas(self):
        """Gera o par de chaves deste usuário."""
        self.chave_privada = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        self.chave_publica = self.chave_privada.public_key()

    def assinar_mensagem(self, mensagem):
        """Calcula o hash e o assina com a chave privada deste usuário."""
        if self.chave_privada is None:
            raise ValueError("Gere as chaves antes de assinar uma mensagem.")

        # Calcular um hash não cifra a mensagem.
        hash_mensagem = hashlib.sha256(
            mensagem.encode('utf-8')
        ).digest()

        return self.chave_privada.sign(
            hash_mensagem,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            utils.Prehashed(hashes.SHA256())
        )

    def enviar_mensagem(self, mensagem):
        """Retorna a mensagem junto com sua assinatura digital."""
        assinatura = self.assinar_mensagem(mensagem)
        return mensagem, assinatura

    def verificar_mensagem(self, mensagem, assinatura, chave_publica_remetente):
        """Verifica a assinatura com a chave pública do suposto remetente."""
        hash_mensagem = hashlib.sha256(
            mensagem.encode('utf-8')
        ).digest()

        try:
            chave_publica_remetente.verify(
                assinatura,
                hash_mensagem,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                utils.Prehashed(hashes.SHA256())
            )

            return True

        except InvalidSignature:
            return False

    def alterar_mensagem(self, mensagem_interceptada, novo_conteudo):
        """Substitui todo o texto interceptado pelo conteúdo escolhido."""
        if novo_conteudo == mensagem_interceptada:
            raise ValueError("O novo conteúdo deve ser diferente do original.")

        return novo_conteudo


Alice = Usuario()
Bob = Usuario()
Eve = Usuario()

Alice.gerar_chaves_assimetricas()
chave_publica_alice = Alice.chave_publica


# Cenário 1: mensagem original e assinatura de Alice.
mensagem_alice, assinatura_alice = Alice.enviar_mensagem(
    "Oi Bob, podemos nos encontrar na biblioteca amanhã?"
)

print("\n--- Cenário 1: mensagem original de Alice ---")
print("Mensagem:", mensagem_alice)

print("Assinatura válida? Esperado: True")
print(Bob.verificar_mensagem(
    mensagem_alice,
    assinatura_alice,
    chave_publica_alice
))

# Cenário 2: Eve substitui todo o conteúdo, mantendo a assinatura de Alice.
Eve.gerar_chaves_assimetricas()

mensagem_eve = Eve.alterar_mensagem(
    mensagem_alice,
    "Bob, cancele o encontro e transfira R$ 500 para esta outra conta."
)

print("\n--- Cenário 2: conteúdo substituído e assinatura de Alice ---")
print("Mensagem original:", mensagem_alice)
print("Mensagem recebida por Bob:", mensagem_eve)

print("Assinatura válida? Esperado: False")
print(Bob.verificar_mensagem(
    mensagem_eve,
    assinatura_alice,
    chave_publica_alice
))


# Cenário 3: Eve assina o conteúdo substituído com sua própria chave.
mensagem_forjada, assinatura_eve = Eve.enviar_mensagem(mensagem_eve)

print("\n--- Cenário 3: conteúdo substituído e assinatura de Eve ---")
print("Mensagem recebida por Bob:", mensagem_forjada)

# A chave usada por Bob continua sendo a pública de Alice.
print("Assinatura válida com a pública de Alice? Esperado: False")
print(Bob.verificar_mensagem(
    mensagem_forjada,
    assinatura_eve,
    chave_publica_alice
))