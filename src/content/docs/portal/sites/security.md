---
title: RSA keys and DKIM checks
description: Make an RSA key pair, with the DKIM record that publishes it, and check that a domain publishes the DKIM record it should.
---

The portal's **Security** extension makes keys and checks DNS records. Both run for jobs and administrators only: a form anyone may send, or an endpoint anyone may call, cannot use them. As with every extension, it is open to every tenant of the portal.

## Make an RSA key pair

**Make an RSA key pair** makes a new key pair. The private key is kept sealed in a **secret connector** you name, made for it on **Connectors**: it never appears in the run, its log or its answer. The step keeps the public key, in PEM, and the DKIM record that publishes it (`v=DKIM1; k=rsa; p=…`). Keys are 2048 bits unless you ask for 3072 or 4096.

- Making a key again replaces the one kept in that connector.
- A DKIM record is longer than 255 characters: your DNS host splits it into several strings, or asks you to.
- Larger keys take longer to make: a portal makes one at a time for a site, and at most 20 an hour.

## Check a DKIM record

**Check a DKIM record** reads the record a domain publishes for a selector, at `<selector>._domainkey.<domain>`, and keeps:

- **found**: whether there is a DKIM record;
- **revoked**: whether its key was taken back (an empty `p=`);
- **records**: how many DKIM records the selector has;
- **matches**: whether its one record holds the public key you expected, compared as a key, however it is written (PEM, or the base64 a DKIM record holds). With no key given, it is empty; with several records, it is false, as a verifier may read any of them;
- **record**: the record as published, at most 1,000 characters.

RSA and Ed25519 keys are read. When DNS fails or does not answer in time, the step fails, rather than say there is no record. Names that are not public DNS names (`localhost`, `.local`, `.internal`) are refused.

## Encrypt and decrypt with AES and RSA

Four actions under **Security** keep what must not be read in the clear. Their keys are only ever **secret connectors**: an action names the connector, and the key never appears in a form, an expression, a run's log or an answer.

- **Encrypt with AES** and **Decrypt with AES** use AES-256-GCM. The key is a secret connector holding 32 random bytes written in base64 (the **Set credentials** form of a secret connector takes it). The text to encrypt is an expression (text, or base64 for bytes); **Associated data** is optional text that must be the same to decrypt. The answer is base64 of the 12-byte IV (new at every encryption), the encrypted text and the 16-byte tag, one after the other, so another system can read it. Decrypt gives the text as text or as base64.
- **Encrypt with RSA** and **Decrypt with RSA** use RSA-OAEP with SHA-256, with keys of 2048, 3072 or 4096 bits. The text is encrypted for the key pair a secret connector holds (made by **Make an RSA key pair**), or for a public key you paste (a public key is not secret). Decrypting takes the private key of a secret connector, and nowhere else. The text to encrypt is at most the key's bytes less 66, 190 bytes with a 2048-bit key: longer fails with "The text is too long for RSA; use AES."

Plain texts are at most 1 MB. A text decrypted with a wrong key, a changed byte or other associated data only says "The data cannot be decrypted." and nothing more. A key of the wrong length makes the action fail when it runs.

- **Who may:** encryption works in any form, flow, endpoint or job. Decryption works in jobs, in flows, and in forms and endpoints people sign in to; it is refused when a form anyone may send or a public endpoint holds it, as soon as the file is saved.
- **Who may read it:** the decrypting actions take an optional **Who may read the text**, a list of up to 20 principals such as `group:HR` or `user:ana@example.ro`. Only a person who is one of them reads it (a job reads as the person it runs as); anyone else fails with "You are not allowed to read this text." Without the list, anyone who may run decryption, as above, reads it.
- **The text decrypted is sensitive:** a **Write in the log** step that reads it writes `[sensibil]`, as does an error that names it. A message or an answer that shows it shows it to the person it is for, but the copy kept in the history of the run has `[sensibil]` instead. The value is still there for the steps that follow.
