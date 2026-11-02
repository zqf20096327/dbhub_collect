<p align="center">
  <img src="public/icons/icon.svg" width="80" alt="ShareTab logo" />
</p>

<h1 align="center">ShareTab</h1>

<p align="center">
  A self-hosted, open-source alternative to Splitwise with AI-powered receipt scanning.
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#features">Features</a> &bull;
  <a href="#screenshots">Screenshots</a> &bull;
  <a href="#configuration">Configuration</a> &bull;
  <a href="#development">Development</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT" /></a>
  <img src="https://img.shields.io/github/stars/sw-carlos-cristobal/sharetab" alt="GitHub stars" />
  <img src="https://img.shields.io/github/last-commit/sw-carlos-cristobal/sharetab" alt="Last commit" />
</p>

---

ShareTab is a free, self-hosted alternative to Splitwise for tracking shared expenses with roommates, friends, and travel groups. Snap a photo of a receipt, let AI extract the line items, and assign them to group members. Taxes and tips split proportionally. Deploy on your own server with Docker Compose.

## Screenshots

### Dashboard -- see all your balances at a glance

<p align="center">
  <img src="demo/dashboard.gif" width="100%" alt="Dashboard showing balance summary, who owes you, and group cards" />
</p>

### AI receipt scanning -- snap a photo, assign items to people

<p align="center">
  <img src="demo/receipt-scan.gif" width="320" alt="Receipt scan: upload photo, AI extracts items, assign to group members" />
</p>

### Split modes -- equal, exact, percentage, or shares

<p align="center">
  <img src="demo/split-modes.gif" width="320" alt="Switching between equal, exact, percentage, and shares split modes" />
</p>

### Add expense -- quick and simple

<p align="center">
  <img src="demo/add-expense.gif" width="320" alt="Adding an expense with equal split" />
</p>

### Multi-currency -- spend in any currency, settle in the group's currency

<p align="center">
  <img src="demo/multi-currency.gif" width="320" alt="Adding an expense in EUR for a USD group, with automatic exchange-rate conversion" />
</p>

### Create a group -- emoji, currency, and description

<p align="center">
  <img src="demo/create-group.gif" width="320" alt="Creating a new group with emoji picker and currency selector" />
</p>

### Settle up -- click a debt to record payment

<p align="center">
  <img src="demo/settle-up.gif" width="320" alt="Settlement dialog with From, To, and Amount" />
</p>

### Venmo payments -- one tap to pay your share

<p align="center">
  <img src="demo/venmo-pay.gif" width="320" alt="Guest split with one-tap Venmo deep-link pay buttons for each person" />
</p>

### Invite members -- share a link

<p align="center">
  <img src="demo/invite-members.gif" width="320" alt="Generating and copying an invite link" />
</p>

### Guest bill splitting -- no account needed

<p align="center">
  <img src="demo/guest-split.gif" width="320" alt="Guest split: upload receipt, add people, assign items, share results" />
</p>

### Group settings

<p align="center">
  <img src="demo/group-settings.gif" width="320" alt="Group settings page with member management" />
</p>

### Dark mode -- toggle with one click

<p align="center">
  <img src="demo/dark-mode.gif" width="320" alt="Dark mode toggle" />
</p>

### 9 languages -- switch the entire UI in one click

<p align="center">
  <img src="demo/language-switcher.gif" width="100%" alt="Switching the interface language between English, Spanish, and Japanese with locale-aware formatting" />
</p>

### Admin dashboard -- manage users, AI providers, and system settings

<p align="center">
  <img src="demo/admin-dashboard.gif" width="100%" alt="Admin dashboard with system health, OAuth management, audit log, and tools" />
</p>

## Features

- **Group expense tracking** with multiple split modes (equal, percentage, shares, exact, item-level)
- **AI receipt scanning** -- photograph

[...截断...]

 a receipt, AI extracts line items, assign items to group members with proportional tax/tip; zoomable/pannable receipt viewer; rescan with correction prompts
- **Multi-currency** -- record an expense in any currency and ShareTab converts it to the group's currency at the exchange rate for the expense date (ECB rates from [frankfurter.app](https://frankfurter.app), no API key; the server needs outbound internet access). For a currency without an ECB rate, or when the lookup fails, enter the rate yourself (expenses created from a scanned receipt can't take a manual rate)
- **Claim sessions** -- share a scanned receipt as a link so everyone picks their own items: split an item between people, join as a couple or group that pays a proportional share, and finalize once every item is claimed. Each person gets a personal link for continuing as themselves on another device (send it only to yourself: anyone who has it can act as you in that split until the split expires, 7 days after it's created or earlier if its signed-in creator ends it, or until you're removed from it); rejoining under a name someone already took needs that person's link. Works for guest splits and group receipt scans, and signed-in users find their guest splits under **My Splits**
- **Venmo payments** -- one-tap Venmo pay links on guest split results, claim sessions, and group balances; paying a group debt records the settlement after you confirm. USD only, and off by default: an admin enables it, users add their Venmo handle in Settings, and a guest split's creator (signed in) adds theirs on the split
- **9 languages** -- English, Spanish, Swedish, French, German, Brazilian Portuguese, Japanese, Simplified Chinese, and Korean, with locale-aware money formatting; each user's choice is saved to their account
- **Guest bill splitting** -- no account needed, shareable summary links; admins can turn off guest receipt uploads (admin toggle or `DISABLE_GUEST_UPLOADS`) so anonymous visitors can't upload receipt images or run AI scans (signed-in users with an active account keep access, so also limit who can create an account: Registration Control covers password and Google sign-up, while magic link and OIDC auto-registration still create accounts; see [Security notes](#oidc-security-notes))
- **Pluggable AI providers** -- OpenAI (GPT-4o), OpenAI-Codex (ChatGPT OAuth), Claude (API key), Meridian (Claude Max subscription), local Ollama
- **Group archiving** -- archive settled-up groups to declutter your dashboard; toggle archived view on groups page. A group with an open balance can't be archived, and an archived group where you still owe or are owed money (for example, one archived before this rule) stays on the dashboard
- **Cross-group dashboard** -- see all your balances at a glance, with per-person debt breakdown
- **Debt simplification** -- minimize the number of payments needed
- **Settle up** -- record payments between any two group members with explicit From/To fields
- **Placeholder members** -- add people without accounts and rename them from group settings; when someone joins, send them a link that hands over their placeholder, or merge the placeholder into the account they joined with, and its expenses and payments move to them. Once someone has settled up, remove them: their past expenses stay under their name, and a balance that comes back can still be settled with them
- **Dark mode** -- system-aware with manual toggle
- **Invite links** -- share a link to add friends to your groups
- **Magic link auth** -- passwordless email sign-in
- **Password reset** -- "Forgot password?" emails a single-use reset link when email is configured; an admin can also make one from the admin dashboard, the way back in without email; a new password ends every session signed in under the old one (see [Forgotten passwords](#forgotten-passwords))
- **Single sign-on (OIDC)** -- sign in with Authentik, Authelia, Keycloak, or other OpenID Connect providers; optional auto-registratio