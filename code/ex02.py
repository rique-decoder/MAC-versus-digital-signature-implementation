import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Ainda usaremos hmac para fazer a assinatura?
# Ou por estarmos usando RSA/ECDSA ja conseguimos fazer o quesito de autenticacao?



class Remetente:
    def __init__(self):
        self.chave_publica = None
        self.chave_privada = None

    def gerar_chaves_assimetricas(self):
        self.chave_privada = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        self.chave_publica = self.chave_privada.public_key()

    def assinar_mensagem(self, mensagem):
        

        assinatura = self.chave_privada.sign(
            mensagem,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return assinatura

    def enviar_mensagem(self, mensagem):
        """Gera uma tag HMAC para autenticar a mensagem e verificar sua integridade."""
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

Alice = Remetente()
Alice.gerar_chaves_assimetricas()
