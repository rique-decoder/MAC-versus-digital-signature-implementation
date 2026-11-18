
# MAC versus Digital Signature

This repository presents a practical Python implementation comparing two message authentication and integrity mechanisms:

- **MAC (Message Authentication Code)**, using HMAC-SHA256
- **Digital Signature**, using RSA public-key and private-key cryptography

The examples simulate communication between Alice, Bob, and Eve, where Eve attempts to intercept or tamper with messages.

## Contents

- `code/ex01.py`: demonstrates symmetric authentication with HMAC-SHA256.
- `code/ex02.py`: demonstrates asymmetric authentication with RSA and PSS.
- `code/enunciado.md`: contains the proposed instructions for the activity.
- `img/`: explanatory diagrams of the concepts and implemented scenarios.

## HMAC-SHA256

In the first example, Alice and Bob share the same secret key. Alice generates an HMAC tag from the message and the key. Next, Bob recalculates the tag and compares the results.

HMAC allows verifying:

- Message integrity
- That it was created by someone who knows the shared key

If Eve modifies a single character of the message and sends the original tag, validation will fail.

## RSA Digital Signature

In the second example:

- Alice generates an RSA key pair
- The private key is used to sign the SHA-256 hash of the message
- Bob verifies the signature using Alice's public key
- Eve cannot generate a valid signature without Alice's private key

The scenarios demonstrate:

1. An original message with a valid signature
2. A replaced message keeping the original signature
3. A message signed by Eve herself

## Key Differences

| MAC/HMAC | Digital Signature |
|---|---|
| Uses a shared secret key | Uses a public and private key pair |
| Alice and Bob hold the same key | Only the sender holds the private key |
| Ensures integrity and authenticity among trusted parties | Proves authorship/origin |
| Does not provide full non-repudiation | Can provide non-repudiation |

## Dependencies

The MAC example uses only features from the Python standard library.

The digital signature example requires the `cryptography` package:

```bash
pip install cryptography
```

## Running the Examples

```bash
python code/ex01.py
python code/ex02.py
```

Each script outputs to the terminal the results of creating and verifying messages across different communication and tampering scenarios.

## License

This project is available under the MIT License.

