---
title: Troubleshooting
sidebar_position: 90
---

_Last updated: 2026-05-11 · App snapshot: surogate-ops-main (2026-05-10)_

# Troubleshooting

Symptom → likely cause → fix. For the underlying error vocabulary see [Reference → Error messages](./reference/errors).

## Sign-in

**I can sign in but I'm sent straight to /onboarding every time.**
The `agentOnboardingDone` flag is missing in this browser's localStorage. Walk through the 2-step welcome once; the next sign-in will land on `/work` or `/studio` directly. Clearing site storage will reset the flag.

**My password works but I'm asked to change it.**
Your admin set you up with a temporary password (`must_change_password=true`). Finish the change-password flow first; the access token can only reach `/change-password` until you do.

**My provider (Google/GitHub) sign-in lands on "Complete signup".**
This is your **first** Firebase sign-in. Pick a Surogate username and a fallback password. The username can't be changed later.

**"Wrong password" but I'm certain the password is correct.**
Some accounts are **Firebase-only** even when they have a local email — try the Forgot password link (only Firebase accounts can reset). For local-only accounts the admin must reset it.

## Work mode

**The Work pages keep redirecting to /onboarding.**
Two causes: (a) you haven't completed the 2-step welcome on this browser, or (b) you cleared localStorage. Walk through the welcome — it's a once-per-browser, instant flow.

**"Find Templates" is greyed out.**
Type something into the **Describe what you need** textarea — the button is disabled until at least one character is entered.

**My agent isn't appearing under /work.**
- Confirm the agent is in **Running** state (check **/studio/agents** under Develop mode).
- Confirm you have read access to the agent's project.
- Refresh — the dashboard updates live but transient errors can drop the stream.

## Studio

**/studio redirects to /onboarding for new users.**
The Studio index has a built-in onboarding gate when you have zero agents. Direct sub-routes (`/studio/agents`, `/studio/models`, etc.) load anyway.

**The Settings sidebar shows only Profile and Data Hub.**
Projects / Integrations / Notifications are hidden from the sidebar for non-admin accounts. They are still reachable by URL with limited actions.

**Studio Dashboard counters all show 0 but other pages have data.**
The dashboard sums **this project** only. Switch project in the top bar.

## Models & Agents

**Deploy stuck in "Deploying".**
Check **/studio/compute/workload-queue** for the related `serving` job. If it's stuck in **Provisioning**, the cloud backend has no capacity or the credentials drifted. If it's **Failed**, open the job logs from the row menu.

**Agent crashes with "Model unhealthy".**
The Model is in **Error** or **Stopped**. Re-deploy the model first, then redeploy the agent.

**Skill calls fail silently.**
The Skill version pinned by the agent might no longer exist. Reattach a current Skill version in agent settings and redeploy.

## Hub & Knowledge Bases

**Hub home shows 0 repos but I expect content.**
Your Hub credentials (`hub_key` / `hub_secret`) are missing or wrong. Re-enter under **Settings → Data Hub**.

**KB stuck in Compiling forever.**
Large sources can take a while. Check **/studio/compute/workload-queue** for the related job. If there's no related job, the indexer queue is stalled — file an issue.

**KB shows Error.**
Open the KB and read per-document errors. Most common cause: a source URL returns 401/403 because the credential expired.

## Compute

**Connected a backend but offers are empty.**
- Credentials may be valid but missing the quota / IAM permissions needed to list instance types.
- The account may have no GPU quota in the regions Surogate queries.
- The provider may be rate-limiting — wait and click **Refresh** on the Hub page (you're looking at Hub here, not Compute — the refresh affordance is similar).

## Monitoring

**Counters frozen after a while.**
The live WebSocket disconnected. Refresh the page.

## Performance

**Slow page loads.**
Check the [Hub](./features/hub) for very large repos — opening a repo with thousands of files loads the file tree client-side and can be slow on cold caches.

## Still stuck?

- Open the browser console; many server errors show structured detail there.
- File an issue against the docs repo with the URL, the time, your username (not real-name), and a short reproduction.
