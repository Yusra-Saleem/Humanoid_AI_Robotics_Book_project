---
id: 4
title: Update Agent Instructions for Conversational Flow
stage: implement
date: 2025-12-03
surface: agent
model: gemini
feature: general-chatbot-behavior
branch: main
user: user
command: agent ko aesi instruction do k wo ye kren but english me instructions do ek detailed instruction : @backend\** 
mujhe smjh nhi aya ye sb ye kia flow me chahtii hun chatbot ka kaam he normal conversation kren user se chatbot speciffic is book k liye bnaya aya he jis ka kaam he is book se related user queries ka response krna unke pochne pr explain krna unki helpkrna chahe kisi bhi zuban me ho
labels: [chatbot, agent-instructions, rag-service]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/src/services/rag_service.py
tests:
 - none
---

## Prompt

agent ko aesi instruction do k wo ye kren but english me instructions do ek detailed instruction : @backend\** 
mujhe smjh nhi aya ye sb ye kia flow me chahtii hun chatbot ka kaam he normal conversation kren user se chatbot speciffic is book k liye bnaya aya he jis ka kaam he is book se related user queries ka response krna unke pochne pr explain krna unki helpkrna chahe kisi bhi zuban me ho

## Response snapshot

I have updated the agent's instructions as you requested. The chatbot should now behave more closely to the conversational tutor you described. Is there anything else I can help you with?

## Outcome

- ✅ Impact: The agent's instructions were updated to provide a more detailed persona and set of behaviors, aligning with the user's request for a conversational, multi-lingual, book-focused tutor.
- 🧪 Tests: No tests were run as this was a change to a configuration string (the agent's instructions).
- 📁 Files: Modified `backend/src/services/rag_service.py` to replace the existing agent instructions with a more detailed set.
- 🔁 Next prompts: None
- 🧠 Reflection: The user was confused by the technical documentation and wanted a clear, high-level instruction set for the agent. Directly updating the agent's prompt was the most effective way to address this. The new instructions are more robust and better define the desired chatbot behavior.

## Evaluation notes (flywheel)

- Failure modes observed: None observed.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
