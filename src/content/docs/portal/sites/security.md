---
title: RSA keys and DKIM checks
description: Make an RSA key pair, with the DKIM record that publishes it, and check that a domain publishes the DKIM record it should.
---

The portal's **Security** extension makes keys and checks DNS records. Both run for jobs and administrators only: a form anyone may send, or an endpoint anyone may call, cannot use them. As with every extension, it is open to every tenant of the portal.

## Make an RSA key pair

**Make an RSA key pair** keeps a new public key and private key, in PEM, and the DKIM record that publishes the public one (`v=DKIM1; k=rsa; p=…`). Keys are 2048 bits unless you ask for 3072 or 4096.

- Keep the private key where only it is needed, such as a connector's secret or a record only administrators read. The portal never writes it in a log.
- A DKIM record is longer than 255 characters: your DNS host splits it into several strings, or asks you to.
- Larger keys take longer to make; a portal makes two at a time.

## Check a DKIM record

**Check a DKIM record** reads the record a domain publishes for a selector, at `<selector>._domainkey.<domain>`, and keeps:

- **found**: whether there is a DKIM record;
- **revoked**: whether its key was taken back (an empty `p=`);
- **matches**: whether it holds the public key you expected, compared as a key, however it is written (PEM, or the base64 a DKIM record holds). With no key given, it is empty;
- **record**: the record as published, at most 1,000 characters.

RSA and Ed25519 keys are read. When DNS fails or does not answer in time, the step fails, rather than say there is no record. Names that are not public DNS names (`localhost`, `.local`, `.internal`) are refused.
