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
