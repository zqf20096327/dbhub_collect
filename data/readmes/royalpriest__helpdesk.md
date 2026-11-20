# Helpdesk

An open source, self-hosted helpdesk built with Rails 8. Customers email your support address, the
emails become tickets, and your team answers them from one shared inbox.

**[Try the live demo](https://helpdesk-demo-zga1.onrender.com)** (sign in as `agent@example.com` / `password`; it resets every night and may take a minute to wake up).

![A ticket with a canned reply inserted](docs/ticket.png)

## Features

- **Shared inbox.** Email sent to your support address arrives through Action Mailbox and opens a
  ticket. When the customer replies, the reply joins the same ticket (matched by the `[#42]` tag in
  the subject or the email's `References` header).
- **Assignment.** Agents filter tickets by *Mine*, *Unassigned*, *Open* or *All*, and assign a ticket
  to themselves or a teammate. Tickets move between `open`, `pending` and `closed`.
- **Multiple inboxes.** Run support@, billing@ and more from one helpdesk. Each ticket remembers
  which address it came in on, and replies go out from that same address.
- **Canned replies.** Save common answers and drop them into a reply from a menu.
- **Satisfaction ratings.** When an agent closes a ticket, the customer gets a one-click
  "how did we do?" email. The inbox shows the share of good ratings over the last 30 days.
- **Customer portal.** Every reply email links to a private page where the customer can read the
  whole conversation and answer from the browser. No customer accounts or passwords needed.

## Getting started

You need Ruby 3.3 or newer and SQLite.

```sh
git clone https://github.com/royalpriest/helpdesk.git
cd helpdesk
bin/setup          # installs gems, creates the database, loads demo data, starts the server
```

Open http://localhost:3000 and sign in as `agent@example.com` / `password`.

### Try it in your browser

No Ruby needed: on GitHub, click **Code → Codespaces → Create codespace on main**. It installs
everything, loads the demo data and opens the app. Sign in as `agent@example.com` / `password`.

### Try the online demo

The live demo runs at **https://helpdesk-demo-zga1.onrender.com**. Sign in as `agent@example.com` / `password`.
It sends no email and resets every night.

To run your own copy:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/royalpriest/helpdesk)

The button sets up a free demo that resets every night. See [Free demo on Render](docs/deploy.md#free-demo-on-render).

### Try the inbox locally

Rails ships a page for sending fake inbound email. With the server running, open
http://localhost:3000/rails/conductor/action_mailbox/inbound_emails/new, write an email to
`support@example.com`, and it shows up as a new ticket.

Agent replies are delivered by Active Job. In development you can see them in the log.

## Configuration

| Variable | What it does | Default |
| --- | --- | --- |
| `SUPPORT_EMAIL` | The default inbox's address. Add more addresses (billing@, sales@) on the **Inboxes** page | `support@example.com` |
| `APP_HOST` | Host used in links inside emails (production) | `example.com` |
| `SMTP_ADDRESS`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD` | Outgoing mail server (production) | none |
| `ACTION_MAILBOX_INGRESS` | How inbound mail reaches the app: `relay`, `postmark`, `sendgrid`, `mailgun`, `mandrill` (production) | `relay` |
| `AUTO_CLOSE_AFTER_DAYS` | Close tickets waiting on the customer after this many days (`0` turns it off) | `7` |
| `SATISFACTION_SURVEYS` | Email customers a rating request when an agent closes their ticket (`false` turns it off) | `true` |
| `DEMO_MODE` | Run as a public demo: loads demo data, sends no email and resets nightly. Never for real use | `false` |
| `FORCE_SSL`, `ASSUME_SSL` | Set to `false` to run without HTTPS, e.g. trying the Docker image locally (production) | `true` |

To run it on your own server, follow the [deploy guide](docs/deploy.md). It covers a plain server install, the Docker image and a free demo on Render.

See the [Action Mailbox guide](https://guides.rubyonrails.org/action_mailbox_basics.html) for setting
up your mail provider's ingress.

Create your first agent from the console:

```ruby
User.create!(name: "Your Name", email_address: "you@example.com", password: "a-long-password", admin: true)
```

After that, invite teammates from the **Agents** page (only admins can see it). They get an email with a link to choose
their password.

## How it fits together

| Piece | File |
| --- | --- |
| Incoming email to tickets | `app/mailboxes/support_mailbox.rb` |
| Ticket rules (status changes, replies) | `app/models/ticket.rb` |
| Reply email to the customer | `app/mailers/ticket_mailer.rb` |
| Agent screens | `app/controllers/tickets_controller.rb`, `app/views/tickets/` |
| Customer portal | `app/controllers/portal/` |
| Canned reply picker | `app/javascript/controllers/canned_reply_controller.js` |

## Contributing

Contributions are welcome, and first-timers especially. Issues labeled
[good first issue](https://github.com/royalpriest/helpdesk/labels/good%20first%20issue) are a good
place to start. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [roadmap](ROADMAP.md).

## License

MIT. See [LICENSE](LICENSE).
