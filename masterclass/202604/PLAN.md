# Africa Free Routing - Lightning Payment Integration Masterclass

## Day 2: Blink API Integration with AI Coding Tools

**Date:** April 2, 2026, 18:00-20:00 UTC  
**Format:** 2-hour live technical presentation (recorded, no live audience interaction expected)  
**Audience:** 100+ African developers, entrepreneurs, and educators  
**Series:** 3-day Lightning Payment Integration Masterclass  
- Day 1: MavaPay / V2Pay  
- **Day 2: Blink (this session)**  
- Day 3: BTCPay Server  

### Instructors

| Role | Person | Focus |
|------|--------|-------|
| Lead presenter | @pretyflaco | Live demo, prompting, tool setup |
| Blink dev / API expert | @k9ert | API docs, dev.blink.sv, closing the loop |
| Support / co-host | @openoms | Technical backup, audience coordination |

### Goal

Move participants from curiosity to real implementation. By the end of the session, viewers should understand how to:
1. Set up an AI-assisted development environment (terminal + OpenCode + cheap LLM)
2. Use the Blink API's unauthenticated endpoints to generate Lightning invoices
3. Build and deploy a static donation page on GitHub Pages
4. Understand the frontend vs. backend distinction and when a VPS is needed

---

## Pre-Session Setup (for participants)

### Environment
- **OS:** Linux recommended. If on Windows, install WSL (Windows Subsystem for Linux) to get a proper terminal
- **Accounts needed:**
  - GitHub account (free) -- this is where code lives, gets version-controlled, and gets published
  - Blink account with a username (free at blink.sv)
  - PPQ.ai account (optional, for cheap AI model access -- can top up with Lightning)

### Tooling Stack
- **Terminal** (Linux/macOS native, or WSL on Windows)
- **GitHub CLI** (`gh`) -- gives superpowers to the coding agent (repo creation, pages setup, etc.)
- **OpenCode** -- AI coding agent that runs in the terminal
- **LLM Model:** MiniMax M2.5 via PPQ.ai (~$0.30 per session vs ~$25 for Claude Opus)
  - Proven to successfully implement all instructions in pre-session testing
  - Other cheap options: Kimi K2.5, Codex
  - PPQ.ai can be topped up with Lightning -- no subscription needed
- **Chrome DevTools MCP** -- allows the agent to drive the browser for testing (spectacular for demos)

---

## Session Outline

### Part 1: Foundation (0:00 - 0:20)

**Topics:**
- Welcome and context: what is this masterclass about, why Bitcoin Lightning payments matter for African developers and entrepreneurs
- Philosophy: why we teach AI-assisted development -- "the times of live coding with Apollo Playground are gone"
- OS and terminal setup: brief recommendation for Linux/WSL, why Windows PowerShell causes friction
- Show existing example: reference Electro Badour's website as a real-world Lightning-enabled site
- **GitHub account and CLI:** explain that GitHub is where your code lives, gets version-controlled, gets published. Setting up `gh` CLI gives the AI agent the ability to create repos, enable pages, push code
- **OpenCode setup:** install, configure with PPQ.ai API key and MiniMax M2.5 model
  - Show how to add a custom provider in OpenCode config
  - Explain what models are, why cheap models are viable for many tasks
  - Mention: if configuration gets broken (as happened in brainstorming), use a SOTA model briefly to fix it

**Key teaching moment:** Installing GitHub CLI and logging in gives "superpowers" to OpenCode -- it can create repos, push code, enable pages, all from the terminal.

### Part 2: Build the Donation Page (0:20 - 1:00)

**Approach:** Start from scratch. No cloning a repo. Use smaller, sequential prompts (not one mega-prompt) -- both for pedagogy and to reduce hallucination/derailing.

**Live demo flow:**

1. **First prompt:** Create a GitHub repository and static HTML page with a Lightning donation button
   - Agent creates repo via `gh repo create`
   - Agent scaffolds `index.html` with basic structure
   - Agent enables GitHub Pages via `gh api`

2. **Second prompt:** Integrate the Blink API for invoice generation
   - Point the agent to `dev.blink.sv` and the **AI Agent API Playbook** at `dev.blink.sv/api/agent-playbook`
   - Key resource: **No API Key Operations** page at `dev.blink.sv/api/no-api-key-operations`
   - The agent should discover the 2-step flow:
     1. `accountDefaultWallet(username, walletCurrency: BTC)` -- get wallet ID (no auth)
     2. `lnInvoiceCreateOnBehalfOfRecipient(recipientWalletId, amount)` -- create invoice (no auth)

3. **Third prompt:** Add QR code display and copy button
   - QR library: `qrcodejs` from cdnjs.cloudflare.com (note: jsdelivr CDN for `qrcode` npm package was blocked by CORB in testing)

4. **Fourth prompt:** Add payment status checking
   - `lnInvoicePaymentStatusByPaymentRequest` query (no auth required)
   - Polling every 3 seconds
   - Show success animation when PAID, handle EXPIRED state
   - **Note:** WebSocket subscription (`lnInvoicePaymentStatus`) exists but requires authentication -- polling is the no-auth alternative

5. **Deploy and test:** Push to GitHub, verify on GitHub Pages, generate an invoice, pay it live

**Reference implementation:** https://pretyflaco.github.io/africafreerouting/  
**Source code:** https://github.com/pretyflaco/africafreerouting

**Teaching moments during Part 2:**
- Show what happens when the agent hallucates (e.g., tries authenticated endpoints) -- explain how to correct course with follow-up prompts
- Demonstrate Chrome DevTools MCP: the agent can open a browser, click buttons, take snapshots to verify its own work
- Explain what "closing the loop" means: don't just accept "it's done" from the agent -- make it test itself with curl or the browser
- When the agent goes wrong, use it as a learning opportunity: "this is not something they realize out of the box"
- **Skills and context:** explain how OpenCode skills help direct the agent, reducing generic web searches when you have specific documentation

### Part 3: Frontend vs. Backend & Advanced Concepts (1:00 - 1:30)

**Frontend vs. Backend distinction:**
- Everything built so far runs entirely on the frontend (static HTML/JS on GitHub Pages)
- No API key exposed, no server needed -- because Blink provides unauthenticated endpoints
- **When you need a backend:**
  - Checking account balance (requires API key)
  - Fundraising thermometer (needs to query balance -- requires auth)
  - Any feature that needs to store state or protect secrets
- **Backend options:**
  - LNVPS: ~5 EUR/month for a VPS
  - **Cloudflare Workers:** serverless option worth exploring (Kemal's suggestion from pre-session testing)
  - Explain the cost/complexity tradeoff

**POC vs. MVP Discussion (Kim's topic):**
- What we built today is a **Spike/POC** (Proof of Concept) -- it proves the technology works
- The difference between a Spike, POC, Prototype, and MVP:
  - **Spike:** Quick experiment to answer a technical question ("can we generate invoices without auth?")
  - **POC:** Demonstrates that a concept is feasible (our donation page)
  - **Prototype:** A more complete version for user feedback
  - **MVP:** Minimum Viable Product -- the smallest thing you can ship to real users
- Reference: Medium article on "Spikes, POCs, Prototypes, MVP"
- For participants building businesses: don't over-engineer at the start. Use AI tools to quickly validate ideas, then iterate

**Push Notifications with ntfy.sh (Kim's topic):**
- **ntfy.sh** -- free, open-source push notification service
  - No signup required, no API key needed
  - Can be used as a building block for payment notifications
  - Example: when a payment is detected, send a push notification to the merchant's phone
  - Works on any device via the ntfy app or browser
  - Perfect for lightweight integrations without building a full backend
- This is the kind of "building block" thinking that makes the difference between a POC and something people actually use

### Part 4: Interactive / Live Building (1:30 - 2:00)

**Format:** More open-ended. Options depending on audience energy:

**Option A: Audience Q&A + Live Improvisation**
- Take questions from the chat/audience
- Kim instructs Kemal on what to build, Kemal translates instructions into OpenCode prompts
- Audience watches real-time problem-solving: how to interpret requirements, formulate prompts, handle agent errors
- Show the dynamic between "product owner" (Kim) and "AI-assisted developer" (Kemal)

**Option B: Enhance the Donation Page**
- Add BOLT11 invoice generation (replace LNURL approach if the initial demo used LNURL)
- Improve the UI/design with a follow-up prompt
- Add multiple donation amount options
- Style the page to match a specific brand/project

**Option C: Explore a New Use Case**
- Discount codes sold for sats (Kim's idea -- simple frontend, manual backend process)
- Point-of-sale concept for local merchants
- Personal website with integrated payments

**Key principles for Part 4:**
- Show failure as much as success -- it's more educational
- When the agent derails, demonstrate course correction techniques
- Keep a steady flow; instructors coordinate via back-channel (Blink Slack channel)
- If someone suggests a complex business case, acknowledge it but scope it down to what's achievable in the remaining time

---

## Key Resources

| Resource | URL |
|----------|-----|
| Blink API (GraphQL) | `https://api.blink.sv/graphql` |
| Blink WebSocket | `wss://ws.blink.sv/graphql` (requires auth) |
| AI Agent API Playbook | https://dev.blink.sv/api/agent-playbook |
| No API Key Operations | https://dev.blink.sv/api/no-api-key-operations |
| Donation Page (live) | https://pretyflaco.github.io/africafreerouting/ |
| Source Code | https://github.com/pretyflaco/africafreerouting |
| PPQ.ai (cheap LLM access) | https://ppq.ai |
| OpenCode (AI coding agent) | https://opencode.ai |
| ntfy.sh (push notifications) | https://ntfy.sh |
| Blink Dashboard | https://dashboard.blink.sv |

## Technical Discoveries from Pre-Session Testing

These are gotchas and insights that came up during the brainstorming session and prototype building:

1. **No-auth invoice flow is 2-step:** Must first call `accountDefaultWallet(username)` to get `walletId`, then use that ID in `lnInvoiceCreateOnBehalfOfRecipient`. The mutation does NOT accept `receiverUsername` directly.

2. **QR code library CDN matters:** `qrcodejs` from cdnjs.cloudflare.com works. The jsdelivr CDN for the `qrcode` npm package gets blocked by CORB (Cross-Origin Read Blocking).

3. **Payment status polling works without auth:** `lnInvoicePaymentStatusByPaymentRequest` takes a `paymentRequest` (BOLT11 string) and returns the status. Poll every ~3 seconds.

4. **WebSocket requires auth:** The `lnInvoicePaymentStatus` subscription on `wss://ws.blink.sv/graphql` requires an API key. For frontend-only solutions, use polling instead.

5. **MiniMax M2.5 was the winning cheap model:** Successfully completed the full task. NemoTron (free) struggled with hallucinations and ignored the dev.blink.sv documentation. Cost comparison: ~$0.30 for MiniMax vs ~$25 for Claude Opus for the same session.

6. **Agent behavior issues to demonstrate:**
   - Free models may do web searches instead of reading provided documentation
   - Models may execute actions even in "plan mode" without permission
   - Models may try authenticated endpoints even when told to use public ones
   - All of these are valuable teaching moments about AI-assisted development

7. **GitHub Pages deployment:** Can be enabled via `gh api -X POST repos/{owner}/{repo}/pages` with source branch main, path `/`.

8. **Username bug:** The Blink username may differ from the GitHub username. The wallet lookup for "pretyflaco" returned "Could not find wallet" -- need to verify the correct Blink username before the live demo.

## Action Items

- [ ] Verify correct Blink username for the live demo (pretyflaco wallet lookup fails)
- [ ] Finalize and test the sequential prompts end-to-end with MiniMax M2.5
- [ ] Set up back-channel coordination (Blink Slack channel: #blink-claw-bot)
- [ ] Schedule 30-minute coordination call before presentation day
- [ ] Find out what V2Pay/MavaPay plans for Day 1 to avoid overlap
- [ ] Test if dev.blink.sv serves `llms.txt` or similar for AI agent auto-discovery
- [ ] Investigate Cloudflare Workers as a lightweight backend option for the advanced demo
- [ ] Prepare fallback: have the working donation page repo ready in case the live demo fails

## Open Questions

1. What is the ideal second-hour feature beyond the donation page? (Fundraising thermometer requires backend; discount codes are complex; audience Q&A is safest)
2. Should Replit be shown briefly as an alternative to local dev, or skip it entirely?
3. Can the dev.blink.sv site signal to AI agents where to find relevant docs (llms.txt, HTTP headers)?
4. What exactly is V2Pay covering on Day 1, and is there content overlap?

---

*This plan was compiled from the brainstorming session on March 26, 2026 (@pretyflaco, @k9ert, @openoms) and the prototype building session that produced the donation page at https://pretyflaco.github.io/africafreerouting/*
