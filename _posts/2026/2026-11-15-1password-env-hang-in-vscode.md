---
layout: post
title: "Why a 1Password `.env` Mount Made VS Code Hang"
description: "How a Python extension's default .env lookup clashed with a 1Password mount, and how to fix it."
seo_title: "Why a 1Password `.env` Mount Made VS Code Hang"
seo_description: "How a Python extension's default .env lookup clashed with a 1Password mount, and how to fix it."
date: 2026-11-15 23:00
type: blog
syndicate:
    - mastodon
    - bluesky
    - rss
    - devnull

---

I use 1Password Environments to provide project secrets through a locally mounted `.env`
file. In one repository, enabling the mount made VS Code's Copilot Chat and Source Control
views very slow or appear to hang resulting in the inability to push code.
The same setup worked fine in other repositories.

The problem was not the secret values. An empty 1Password-mounted `.env` caused the same
behaviour, and disabling the mount for this repository made VS Code responsive again.

## What the Logs Showed

VS Code reported an error reading the mounted file:

> Unable to read file `.../.env` (Unavailable (FileSystemError): An unknown error occurred.)

Around the same time, VS Code reported that its extension host was briefly unresponsive.
An extension-host profile showed the Python extensions responding to an environment-file
change: `ms-python.vscode-python-envs` was handling a file event, while `ms-python.python`
called `getEnvFile` and `getEnvironmentVariablesSync`.

The Python extension's default `python.envFile` is `${workspaceFolder}/.env`. It was
therefore trying to use the mounted path as a source of Python environment variables.
1Password's local `.env` mounts use a Unix named pipe rather than an ordinary file. The
failed VS Code read and the Python extension activity pointed to an interaction between
that default lookup and the mounted path.

The profile was only a short CPU sample, so it did not prove what caused every delay in
Copilot or Source Control. The practical confirmation came from changing the Python
extension's env-file path: VS Code stopped hanging with the 1Password mount enabled.

## The Fix

I configured the Python extension to use a separate, ordinary empty file instead of the
mounted `.env`.

In the workspace's `.vscode/settings.json`, add this setting inside the existing JSON
object. Keep any settings already in the file, separating entries with commas:

```json
{
  "python.envFile": "${workspaceFolder}/.vscode/python.env"
}
```

Then, from the repository root, create the empty file:

```sh
touch .vscode/python.env
```

After reloading VS Code and enabling the 1Password mount again, the hangs stopped. The
mounted `.env` remained available to the repository; this change stopped the Python
extension from using that path as its environment-variable file.

## The Trade-Off

Python processes launched by the VS Code Python extension no longer automatically receive
variables from the mounted `.env` through the `python.envFile` setting. Scripts that load
`.env` themselves are unaffected by this setting, as are Git, Copilot and shell sessions.
If a debug or test configuration depends on VS Code injecting values from `.env`, provide
those values another way for that launch. I didn't have any such configurations and
`python.env` remains empty.

In this repository, `.vscode/` is Git-ignored, so the setting and helper file are local to
the checkout and do not need to be committed. Other repositories may have a different
trigger; this fix addresses the Python extension's default `.env` lookup in this workspace.

## Links

- [1Password: Access secrets through local `.env` files](https://www.1password.dev/environments/local-env-file)
- [VS Code: Python environments](https://code.visualstudio.com/docs/python/environments)
