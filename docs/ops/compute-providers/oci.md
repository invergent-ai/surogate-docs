---
title: Oracle Cloud (OCI)
sidebar_position: 7
slug: /compute-providers/oci
description: Connect Oracle Cloud Infrastructure as a Surogate Ops compute backend. Five-field credential, bare-metal GPU shapes.
---

# Oracle Cloud (OCI)

Oracle Cloud Infrastructure is the heaviest credential setup of the eight backends — five fields, including a `.pem` upload — but pays off in OCI's GPU bare-metal shapes, which are often cheaper-per-hour than the equivalent AWS / GCP options.

## Credentials Surogate needs

Five values:

- **User OCID**
- **Tenancy OCID**
- **Fingerprint**
- **Home Region**
- **Private Key** (uploaded as `.pem`)

## Set up the credential

OCI's authentication uses API signing keys. Three places in the OCI Console:

### 1. Find your User OCID

OCI Console → **Identity & Security → Users**. Pick the user that Surogate will act as (or create a new one for the purpose). The user's overview page has the **OCID** field — copy it.

### 2. Find your Tenancy OCID and Home Region

Top-right user menu → **Tenancy**. Two fields are visible:

- **OCID** — your Tenancy OCID.
- **Home Region** — copy the region identifier (e.g., `us-ashburn-1`).

### 3. Add an API signing key

User overview → **API Keys → Add API Key**.

Either:

- **Generate API key pair** — OCI generates a pair; download both. Note the **Fingerprint** displayed after upload.
- **Choose public key file** — upload your own public key (PEM format). Note the **Fingerprint**.

You also need the **private key** corresponding to the public key. If OCI generated the pair, this was downloaded; if you uploaded your own public key, the private key is on your machine.

### 4. Grant compute permissions

The user needs to provision compute instances. Add to a group that has the right policies, or create a dedicated group:

- **Identity & Security → Groups → Create Group → Surogate-Scheduler**.
- Add your user.
- **Policies → Create Policy**:

```
allow group Surogate-Scheduler to manage instance-family in tenancy
allow group Surogate-Scheduler to use virtual-network-family in tenancy
allow group Surogate-Scheduler to manage compute-management-family in tenancy
```

## Connect in Surogate

Compute → Cloud → **OCI** tile. Provide:

- User OCID
- Tenancy OCID
- Fingerprint
- Home Region (e.g., `us-ashburn-1`)
- Private Key (`.pem` upload)

Submit. The tile flips to **Connected**.

## Supported instance shapes

OCI offers a mix of bare-metal and virtual GPU shapes:

| Shape | GPUs | Notes |
|---|---|---|
| **BM.GPU.H100.8** | 8× H100 80GB | Bare metal. Top-end for training. |
| **BM.GPU.A100-v2.8** | 8× A100 80GB | Bare metal. Bread-and-butter training. |
| **BM.GPU4.8** | 8× A100 40GB | Older A100 generation. |
| **VM.GPU.A10.1 / .2** | 1 or 2× A10 24GB | Cheaper VM option for smaller serving. |
| **VM.GPU3.1 / .2 / .4** | 1, 2, or 4× V100 16GB | Legacy. |

OCI's bare-metal pricing is unusually competitive for what you get. The scheduler reads availability from the Compute API.

## Verify the backend works

After connecting, the Offers panel populates within a minute. If empty:

1. **Policy.** Without the *manage instance-family* policy, the offers query returns empty. Add the policy to the user's group.
2. **Region.** OCI GPU availability varies sharply by region; Ashburn (us-ashburn-1), Frankfurt (eu-frankfurt-1), and Tokyo (ap-tokyo-1) tend to have the most stock. Broaden the region set.
3. **Service limits.** OCI gates GPU shapes on per-tenant service limits. Open **Governance & Administration → Limits, Quotas and Usage** → request limit increases for the GPU shapes you want.

## Cost shape

OCI publishes per-hour rates that are often the lowest among the hyperscalers for bare-metal GPU.

Practical pointers:

- **Reservations save more on OCI than on most clouds** — multi-year commits can drop bare-metal rates substantially.
- **Bare metal vs VM.** Bare-metal shapes are dedicated and faster; VMs are cheaper for smaller workloads but rare for GPU above A10.
- **Egress is cheap.** OCI's egress pricing is below the hyperscaler average. If you need to move data between Surogate and other clouds, OCI can serve as the egress-friendly tier.

## When something fails

- **`401 NotAuthenticated`.** Private key and fingerprint don't match. Re-confirm the fingerprint matches the key in OCI's API Keys panel.
- **`401 NotAuthorizedOrNotFound` on a region.** The user lacks policy in the compartment for that region. Add policy or use a region the user already has access to.
- **Offers list empty after a working connection.** Service limit for the requested GPU shape went to zero, or quota was revoked. Check Limits, Quotas and Usage.
- **Bare metal provisioning takes much longer than a VM.** Expected. Bare-metal shapes take five to ten minutes to provision; VMs take under a minute.
- **`.pem` upload rejected as malformed.** Make sure the file is the *private* key (begins with `-----BEGIN RSA PRIVATE KEY-----` or `-----BEGIN PRIVATE KEY-----`). Public keys are rejected.

## When this is the right backend

- **Cost-bound bare-metal training.** OCI's BM shapes are often the cheapest H100 / A100 per hour.
- **Data-residency in specific OCI regions** that aren't well-served by the other hyperscalers.

## When this isn't the right backend

- **Quick experimentation.** The credential setup is heavy; RunPod or Modal are faster to get going.
- **Region requirements OCI doesn't cover.** OCI's region footprint is smaller than AWS / Azure / GCP.

## Where to go next

- **[Compute](../features/compute.mdx)** — the backend-agnostic overview.
- **[AWS](./aws.md)**, **[Azure](./azure.md)**, **[GCP](./gcp.md)**, **[RunPod](./runpod.md)**, **[Modal](./modal.md)**, **[Nebius](./nebius.md)**, **[Vast.ai](./vast-ai.md)** — the other seven backends.
