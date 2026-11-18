# MAC versus Digital Signature

Este repositório apresenta uma implementação prática em Python para comparar dois mecanismos de autenticação e integridade de mensagens:

- **MAC (Message Authentication Code)**, utilizando HMAC-SHA256
- **Assinatura digital**, utilizando criptografia RSA com chave pública e privada

Os exemplos simulam a comunicação entre Alice, Bob e Eve, onde Eve tenta interceptar ou modificar mensagens.

## Conteúdo

- `code/ex01.py`: demonstra autenticação simétrica com HMAC-SHA256.
- `code/ex02.py`: demonstra autenticação assimétrica com RSA e PSS.
- `code/enunciado.md`: contém as instruções propostas para a atividade.
- `img/`: diagramas explicativos dos conceitos e dos cenários implementados.

## HMAC-SHA256

No primeiro exemplo, Alice e Bob compartilham uma mesma chave secreta. Alice gera uma tag HMAC a partir da mensagem e da chave. Em seguida, Bob recalcula a tag e compara os resultados.

O HMAC permite verificar:

- A integridade da mensagem
- Que ela foi criada por alguém que conhece a chave compartilhada

Caso Eve modifique um caractere da mensagem e envie a tag original, a validação falhará.

## Assinatura digital RSA

No segundo exemplo:

- Alice gera um par de chaves RSA
- A chave privada é usada para assinar o hash SHA-256 da mensagem
- Bob verifica a assinatura com a chave pública de Alice
- Eve não consegue gerar uma assinatura válida sem a chave privada de Alice

Os cenários demonstram:

1. Uma mensagem original com assinatura válida
2. Uma mensagem substituída mantendo-se a assinatura original
3. Uma mensagem assinada pela própria Eve

## Diferenças principais

| MAC/HMAC | Assinatura digital |
|---|---|
| Usa uma chave compartilhada | Usa um par de chaves pública e privada |
| Alice e Bob possuem a mesma chave | Somente o remetente possui a chave privada |
| Indica integridade e autenticidade entre participantes confiáveis | Permite comprovar autoria |
| Não oferece não-repúdio completo | Pode oferecer não-repúdio |

## Dependências

O exemplo de MAC utiliza apenas recursos da biblioteca padrão do Python.

O exemplo de assinatura digital requer o pacote `cryptography`:

```bash
pip install cryptography
```

## Executando os exemplos

```bash
python code/ex01.py
python code/ex02.py
```

Cada script mostra no terminal o resultado da criação e da verificação das mensagens em diferentes cenários de comunicação e tentativa de adulteração.

## Licença

Este projeto está disponível sob a licença MIT.