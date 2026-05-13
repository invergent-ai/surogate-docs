---
title: AWS
sidebar_position: 1
slug: /compute-providers/aws
description: Connect AWS as a Surogate Ops compute backend. IAM setup, supported instance types, troubleshooting.
---

# AWS

AWS is one of the eight cloud backends Surogate Ops can schedule workloads on. The credential setup is the heaviest of the eight — an IAM user with the right policy attached — but it pays off in the breadth of GPU types you can reach.

## Credentials Surogate needs

Two values, both from the same IAM user:

- **Access Key ID**
- **Secret Access Key**

## Set up the IAM user

The five-step path from a fresh AWS account to a working credential:

1. **AWS Console → IAM → Users → Create user.**
2. **Name** — something like `surogate-ops-scheduler`. The name has no operational meaning; it's for your records.
3. **Console access** — leave unchecked. This user is for programmatic access only.
4. **Permissions → Attach policies directly →** attach **AmazonEC2FullAccess**.  This is the easiest path; a least-privilege custom policy is possible but more setup.
5. **Create user.**

Once the user exists, generate the access key:

1. Open the user's detail page.
2. **Security credentials → Create access key.**
3. **Use case → Application running outside AWS.**
4. **Create access key.**
5. **Copy both values.**

:::warning Secret is shown once
The Secret Access Key is displayed exactly once during creation. If you miss it, delete the access key and create a new one — there's no "show me again" path.
:::

## Connect in Surogate

Compute → Cloud → **AWS** tile. Paste the Access Key ID and the Secret Access Key. Submit. The tile flips to **Connected**.

The form has a deep-link to the AWS Console for finding the values — use it if you've forgotten the path.

## Supported instance types

Surogate schedules workloads against AWS's GPU instance families:

| Family | Typical GPUs | Best for |
|---|---|---|
| **P4d** | A100 40GB / 80GB | Training and serving large models. |
| **P5** | H100 80GB | The current top-end. Training 70B+ and serving large models with headroom. |
| **G5** | A10G 24GB | Smaller serving, cheaper evals, GRPO at modest scale. |
| **G6** | L4 24GB | Cheapest serving for 7B–13B class models. |

The scheduler reads the offers list from AWS's `DescribeInstanceTypes` API. Instance types your account doesn't have quota for don't appear in the offers — request the quota in AWS Service Quotas before expecting offers.

## Verify the backend works

After connecting, open the AWS backend's detail page. The **Offers** panel should list every GPU type you have quota for, with current spot and on-demand prices.

If the offers list is empty, three things to check, in order:

1. **Quota.** GPU quotas in AWS are off by default. Request them via AWS Service Quotas — separately for each region you care about. Approval takes hours to days.
2. **Regions.** The backend defaults to a small set of regions. Broaden under the backend's settings if you need more.
3. **IAM scope.** `AmazonEC2FullAccess` includes the metadata reads Surogate needs. If you went with a least-privilege custom policy, make sure `ec2:DescribeInstanceTypes` and `ec2:DescribeRegions` are granted.

## Cost shape

Surogate doesn't add a margin to AWS prices; you pay AWS at the rate they show in their billing console.

Practical pointers:

- **Spot is cheaper.** Surogate's scheduler can be configured to prefer spot offers in Compute Policies. Spot saves 30–70% but workloads can be interrupted; serving containers handle this poorly, training handles it well with checkpointing.
- **Reservations apply if you have them.** Reserved Instances and Savings Plans on the AWS side affect the bill but aren't visible in Surogate's offers list.
- **Data transfer matters at scale.** Models pulled from `s3.studio.internal:9000` to AWS GPUs cost data transfer. Mirror frequently-used models into an S3 bucket in the same region as your AWS backend.

## When something fails

- **Offers list empty.** Usually quota. Open AWS Service Quotas → search "running on-demand" → confirm you have non-zero quota for the GPU family in the relevant regions.
- **Workload stays Provisioning forever.** Region capacity is exhausted, or your AZ ran out of the requested instance type. Cancel and retry; the scheduler picks a different AZ.
- **Workload provisions but the container immediately crashes.** Usually the GPU driver mismatch with the model's CUDA version. Surogate ships pre-built images that match recent CUDA; for very new model architectures you may need to bump the image. Open the workload's logs to see the exact failure.
- **`401 invalid_credentials` shortly after connecting.** The IAM user's secret was reset on the AWS side. Generate a new access key and update the credential in Surogate.
- **`AccessDenied` on `DescribeInstanceTypes`.** Custom policy too tight. Add the required permissions or swap to `AmazonEC2FullAccess` while you debug.

## Where to go next

- **[Compute](../features/compute.mdx)** — the backend-agnostic overview.
- **[Compute Providers → Azure](./azure.md)**, **[GCP](./gcp.md)**, **[RunPod](./runpod.md)**, **[Modal](./modal.md)**, **[Nebius](./nebius.md)**, **[OCI](./oci.md)**, **[Vast.ai](./vast-ai.md)** — the other seven backends.
