# Enunciado Direcional

## Implementando Autenticação de Mensagem (MAC vs. Assinatura Digital)

**Objetivo Prático:** Desenvolva um script (em Python ou C++) que demonstre o ciclo de envio, proteção e verificação de uma mensagem utilizando tanto um Código de Autenticação de Mensagem quanto uma Assinatura Digital.

### 1) Implementação de MAC (Simétrico)

* Simule uma chave secreta compartilhada ($K$) entre Alice e Bob.
* Alice deve pegar uma mensagem de texto ($M$), aplicar uma função de MAC baseada em chave (como HMAC-SHA256) para gerar uma tag de autenticação.
* Alice envia a mensagem $M$ junto com a tag para Bob.
* Bob recebe a mensagem, recalcula o HMAC usando a mesma chave secreta $K$ e valida se a tag bate, garantindo que a mensagem não foi adulterada e veio de alguém que conhece a chave.

### 2) Implementação de Assinatura Digital (Assimétrica)

* Gere um par de chaves assimétricas (ex: RSA ou ECDSA) representando a chave privada e a chave pública de Alice.
* Alice calcula o hash da mensagem $M$ e, em seguida, cifra o hash usando a sua chave privada para gerar a assinatura digital.
* Alice envia a mensagem $M$ e a assinatura para Bob.
* Bob recebe os dados, calcula o hash da mensagem recebida e utiliza a chave pública de Alice para decifrar/verificar a assinatura, comprovando a integridade, a autoria e o não-repúdio.

### 3) Desafio Extra

* Tente alterar um único caractere da mensagem em trânsito em ambos os cenários e observe o comportamento da validação em cada caso.