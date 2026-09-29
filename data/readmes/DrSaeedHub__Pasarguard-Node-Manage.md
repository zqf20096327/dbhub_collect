# PasarGuard Manager

One place to run all your **PasarGuard** panels and their nodes.

Add a panel once and the manager signs in for you, remembers the connection, and
keeps it alive. From then on you can add servers as nodes, watch them install
live, and take them down again — without touching a terminal or copying
certificates around by hand.

## Install

On a fresh Linux server, as root, run:

```bash
bash <(curl -Ls https://raw.githubusercontent.com/DrSaeedHub/Pasarguard-Node-Manage/master/scripts/install.sh)
```

It asks four things — a **username**, a **password**, a **port**, and a **web
path** — and does the rest: installs what it needs, sets itself up to start on
boot, creates your account, and prints the address to open. That's the whole
setup. There's no database to install and nothing to configure afterwards.

When it finishes you'll see something like:

```
==> The panel is running.

  URL:      http://203.0.113.7:8443/7f3a91c2b4e5/
  Login:    admin
  ...
```

Open that URL, sign in, and you're in.

### What the four questions mean

- **Username / password** — the account you'll sign in with. You can change
  both later, and add more accounts, from inside the panel.
- **Port** — which port the panel listens on. Pick anything free; the installer
  suggests a random one.
- **Web path** — a secret bit added to the address, like the `7f3a91c2b4e5` in
  the URL above. Anyone who doesn't know it just gets a blank "not found" page,
  which keeps the panel hidden from random scans of your server. Accept the
  suggested one, type your own, or answer **none** to serve it at the plain
  address.

## Using it

**Add a panel.** Give the manager your PasarGuard panel's address and admin
login. It connects, checks the credentials, and keeps the panel's session
fresh for you.

**Add a node two ways:**

- *Connect an existing node* — paste its certificate and API key, and the
  manager registers it on the panel.
- *Install a node for you* — give the manager a server's SSH details and it
  installs everything the node needs on that server and registers it, showing
  you the live progress as it goes.

**Remove a node** from the manager, from the panel, and — if you like — from the
server it's on, all in one step.

**When something goes wrong**, the manager helps you recover: retry a failed
install (it only redoes what's missing), cancel a job that's stuck, or force a
stubborn node to go away.

## Keeping it up to date

The version number in the top-right corner is a button. Click it and the panel
checks for a newer release and installs it for you with one more click, then
restarts. Your panels, nodes, and settings are all kept.

You can also update from the server with:

```bash
pgm update
```

## Settings

Everything about the panel itself lives under **Settings**:

- **Account** — change your own username or password.
- **Accounts** — add or remove the people who can sign in. Everyone who can sign
  in can see every panel, so treat adding an account like sharing the password.
- **Address** — change the port or the secret web path. The panel tells you the
  new address and applies it when you restart.
- **Updates** — check for and install new versions, or turn off the automatic
  check if your server has no internet access.
- **System** — what version you're on, and how the service is doing.

## If you get locked out

Everything you can do in the panel, you can also do from the server with the
`pgm` command — including the things you'd need when you *can't* get into the
panel:

```bash
pgm status      # is it running, and what's the address?
pgm password    # set a new password
pgm port 8443   # move it to a different port
pgm restart     # restart it
pgm logs -f     # watch what it's doing
```

Running the installer again on a server that already has the panel opens this
menu instead of reinstalling.

## Backing up

Everything the panel knows lives in one folder: `/var/lib/pasarguard-manager`.
Copy that folder and you've backed up the whole panel — accounts, connected
panels, saved node credentials, and settings. Put it back and installing again
brings it all back exactly as it was.

## Removing it

```bash
pgm uninstall
```

It asks whether to keep or delete your data. Keeping it means installing again
later picks up right where you left off. The nodes you installed on other
servers keep running either way — they're independent once they're up.

---