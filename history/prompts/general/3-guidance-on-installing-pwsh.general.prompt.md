---
id: 3
title: Guidance on Installing pwsh
stage: general
date: 2025-11-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: what should i do?
labels: [troubleshooting, powershell, installation]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:

tests:

---

## Prompt

what should i do?

## Response snapshot

The `/sp.clarify` command requires PowerShell Core (`pwsh`) to execute its scripts. It appears that `pwsh` is not installed or not in your system's PATH.

To resolve this, please follow these steps:

1.  **Install PowerShell Core**:
    *   **Windows**: You can install it via MSI package, winget, or the Microsoft Store. Refer to the official Microsoft documentation: [https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.5](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.5)
    *   **macOS**: Use Homebrew: `brew install powershell/powershell/powershell`. Refer to: [https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-macos?view=powershell-7.5](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-macos?view=powershell-7.5)
    *   **Linux**: Installation methods vary by distribution. Refer to: [https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-linux?view=powershell-7.5](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-linux?view=powershell-7.5)

2.  **Verify Installation**: After installation, open a new terminal and type `pwsh`. If it starts a PowerShell session, the installation was successful.

3.  **Re-run the command**: Once `pwsh` is correctly installed, please re-run your previous command:
    `/sp.clarify Outline Refinement`

## Outcome

- ✅ Impact: User provided with clear instructions to resolve a dependency issue.
- 🧪 Tests: N/A
- 📁 Files: None
- 🔁 Next prompts: User to install pwsh and re-run /sp.clarify.
- 🧠 Reflection: Provided detailed steps and official documentation links for installing PowerShell Core, which was blocking the /sp.clarify command. This addresses the immediate user need.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
