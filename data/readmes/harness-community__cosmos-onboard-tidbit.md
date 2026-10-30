# Your first Cosmos loop

This walkthrough gets you from a brand-new Cosmos account to two merged pull
requests. You will fork a small storefront that has two reported defects, point
Cosmos at your fork, and then work the way the Software Factory is meant to be
worked: you describe the problem, Cosmos writes and reviews the change, and you
make the final call before anything merges.

The app is a one-page storefront for Cool Professor Clothiers, a shop that sells
tweed, corduroy, and merino and has not opened yet. Two customers have written
in to complain. Neither complaint tells you what is wrong with the code, only
what they saw — which is exactly the shape of the work in a real backlog.

## What you will learn

- Create a Cosmos account and connect a GitHub repository as a source.
- Start a loop from a plain-language problem description rather than a patch.
- Read what Cosmos produces: the pull request, the reviewers' findings, and the
  reasoning behind the change.
- Act as the human checkpoint — review, request a change, and merge.
- Recognize when a defect report is specific enough for an agent to act on.

## How a loop works

A **loop** is one workflow run end to end, with human checkpoints in it. For
code, the loop you will use here is Ticket → PR:

```
  you describe the defect
          │
          ▼
    PR Author ──────► writes the change and opens a pull request
          │
          ▼
    Reviewers ──────► read the diff, flag risk, push fixes back onto the branch
          │
          ▼
        you  ────────► final review and merge
```

You are not in the middle of that chain typing code. You are at the two ends:
you set the problem, and you decide whether the answer ships.

## Repository structure

```
.
├── index.html              Page markup: masthead, hero, gallery, notify form
├── package.json
├── vite.config.js
├── public/
│   ├── favicon.svg
│   └── garments/           Garment images, at their original proportions
│       ├── tweed-jacket.png
│       ├── corduroy-pants.png
│       └── turtleneck.png
├── src/
│   ├── styles.css          All styling for the page
│   └── main.js             Behaviour for the notify form
└── readme-assets/          Screenshots used by this README
```

That is the whole app. There is no backend, no framework, and no test suite —
small enough that you can judge Cosmos's work by reading it.

## Prerequisites

- A GitHub account.
- An email address you can receive mail at, to create your Cosmos account. This 
  should be a **personal email address** not associated with an existing Cosmos
  tenant.
- Permission to install a GitHub App on your own account. If you are using a
  work GitHub account with restrictions, **fork to a personal GitHub account**
  instead.
- Optional, for Step 4 only: Node 20.19 or later and npm.

A new Cosmos account starts with $20 in credits. The two loops in this
walkthrough use about half of that, so you can run them more than once if
you want to try a different prompt.

## Step 1 — Fork this repository

Fork this repository to your own GitHub account. Everything after this point
happens on your fork, not in the `harness-community` repository. 

Leave the fork public and keep the default name.

## Step 2 — Create your Cosmos account

Go to [cosmos.augmentcode.com](https://cosmos.augmentcode.com) and sign up with a personal email address that you have not yet used with the Augment Code platform.

<!-- TODO(verify): confirm the signup flow — email + verification, Google SSO, GitHub SSO? Capture the first screen after login. -->

Once you are in, you will be asked to connect a source of work. This walkthrough will use GitHub, and you'll set it up in the next step.

## Step 3 — Connect your fork to Cosmos

Cosmos reads and writes your repository through the Cosmos GitHub App, not
through your personal GitHub login. Installing the app is what lets it clone the
code, push a branch, and open a pull request on your behalf.

1. When Cosmos asks you to connect GitHub, choose to install the GitHub App.
1. On GitHub's installation screen, select **Only select repositories** and
   choose your fork of this repository.
1. Approve the installation and return to Cosmos.
1. Confirm your fork now appears in Cosmos as an available repository.

<!-- TODO(verify): exact button labels and screen order for the GitHub App install; whether the repository picker lives in Cosmos or only on GitHub; what the post-install confirmation looks like. -->

> [!NOTE]
> Scoping the install to one repository is deliberate. You can widen it later
> from your GitHub settings, and you can remove it entirely when you are done —
> see [Cleanup](#cleanup).

Cosmos will spend a few moments indexing the repository. That index is what
lets it answer questions about code it has never been shown directly.

## Step 4 - Prompt Cosmos Advisor

After the Augment Code GitHub app is installed to your GitHub account with access
to your fork of `cosmos-onboard-tidbit`, you will be provided a prompt for your first 
Session with Cosmos Advisor. Review the prompt and submit it to 
Cosmos Advisor, and it will create several Experts for you.

Once your experts are created you, you'll continue the session with loops to address the defects
in the Cool Professor Clothiers app.

## Step 5 — Optional: see the defects for yourself

You do not need to run the app. Both defects are visible in the screenshots
below, and Cosmos works from the repository rather than from your machine. Run
it only if you would rather see the behaviour first-hand.

1. Clone your fork and install dependencies:

   ```
   npm install
   ```

1. Start the dev server:

   ```
   npm run dev
   ```

1. Open the address it prints, scroll to **The collection**, and then try the
   **Notify me** form with any email address.

## Step 6 — First loop: the gallery

Here is the first complaint, from a customer browsing on a laptop:

> Something is off with your product photos. Every garment looks squashed — the
> trousers could pass for shorts. On my phone it is worse: the gallery runs off
> the right edge and the whole page slides sideways.

That is what the gallery looks like now:

![Gallery with every garment squashed out of proportion](readme-assets/gallery-stretched.jpg)

And on a narrow screen:

![Gallery overflowing past the right edge of a phone viewport, with a horizontal scrollbar](readme-assets/gallery-overflow.jpg)

Start a loop and give Cosmos the problem. Use the complaint, not a diagnosis:

```
The garment images in the gallery are distorted. Each garment is squashed out
of its true proportions — the corduroy trousers read as shorts. On a narrow
screen the gallery also overflows past the right edge of the viewport and the
page scrolls sideways.

Fix it so every garment keeps its original proportions and the gallery fits any
screen width, from a phone to a wide desktop. Do not change the image files.
```

<!-- TODO(verify): where the student starts a loop and what the entry point is called — Advisor chat, a "new session", a loop template? Confirm whether the PR Author runs automatically once the loop is described, or whether the student picks the expert. Capture a screenshot of the loop in progress. -->

While the loop runs, watch what it does rather than waiting for the result. You
should see it locate the relevant files, propose a change, and then hand the
change to reviewers before it reaches you.

When the pull request is ready, review it on GitHub:

1. Read the diff. The change should be small, and you should be able to say in
   one sentence what it does.
1. Read what the reviewers flagged, and whether the author addressed it.
1. Confirm the fix does what the complaint asked, and nothing else. A fix that
   also restyles the headings is doing too much.
1. Merge it.

Here is what a correct result looks like — three garments, each in its own
proportions, in a gallery that reflows instead of overflowing:

![Gallery with each garment at its true proportions, fitting the page](readme-assets/gallery-fixed.jpg)

> [!NOTE]
> There is more than one defensible way to fix this. Cosmos may crop the images
> to a shared shape or fit each one whole inside its frame. Either satisfies the
> complaint. Judge the change by the result and by whether you would be willing
> to own the code, not by whether it matches the screenshot pixel for pixel.

## Step 7 — Second loop: the notify form

Now the second complaint. This one is functional, and it is the kind of bug that
only shows up when someone actually uses the thing:

> I tried to sign up to hear when you open. I typed my address, pressed
> **Notify me**, and the page just reloaded with an empty box. No confirmation,
> no thank you, nothing. Did it work? I have no idea, so I tried four more
> times.

Start a second loop with that problem:

```
The "Notify me" form on the storefront does not confirm anything. After
entering an email address and submitting, the page reloads, the field is
cleared, and no confirmation message is ever shown, so there is no way to tell
whether the address was accepted.

Fix it so submitting the form keeps the visitor on the page and shows the
confirmation message the page already contains.
```

Review and merge it the same way you did the first. Two details worth checking
before you approve:

1. The page already has a confirmation message of its own. A fix that bolts on
   a second one instead of using what is there is a sign the author misread the
   problem.
1. Submitting the same address twice should still behave sensibly.

<!-- TODO(verify): capture the Cosmos review/checkpoint screens for this loop too, for the second half of the video. -->

## What to notice

Two merged pull requests is the small part. The things worth taking away:

- **You described symptoms, not solutions.** Neither prompt named a file, a
  property, or a function. The loop found them. That is the Augment Context
  Engine doing the reading you would otherwise have done.
- **The review happened before you saw it.** The pull request you opened was
  already reviewed once. Your job was the last check, not the only one.
- **The checkpoint is the point.** Nothing merged without you. A loop is not an
  agent left alone with your main branch; it is a workflow with you in it.
- **Small, specific reports get good results.** The second complaint worked
  because it said what the visitor did and what they saw. "The form is broken"
  would have produced a worse pull request.

## Exercise: Improve the factory

The Cosmos Experts did a lot of work for you, but you still had to run the app
locally to verify their work. If you skipped that step, you had to take the
Experts' word that the defects were fixed. 

Cosmos Advisor can do more than orchestrate your Experts. As you saw in the
initial prompt, it can also create experts. Ask Cosmos Advisor to create an
Expert that can verify fixes to the application. Make your own prompt,
or use the following:

> Create a new Expert that can verify the work done in each loop. To save
> me the trouble of running the app locally to see the results, have it
> take screenshots for me.

When Cosmos Advisor is done, make some other change to the application. 
It doesn't have to be a bug fix, it can be a new feature.

## Explore

You likely still have credits available. Continue exploring Cosmos
by either extending the demo application, or creating a new one. You
can update the Augment GitHub app to access other repositories in your
GitHub account and work on those. 

If you have any questions along the way, ask the Cosmos Advisor for guidance.

## Cleanup

Nothing in this walkthrough costs money after you stop, but if you would like to
leave no trace:

1. Remove the Cosmos GitHub App from your account under **Settings →
   Applications → Installed GitHub Apps** on GitHub.
1. Delete your fork.

Your Cosmos account and any remaining credits stay as they are.

## Troubleshooting

**I did not get $20 in credits**
If the domain portion of your email already has users in Cosmos, you
will be considered part of that tenant for the domain. Sign up using
a personal email address instead.

**The onboarding flow did not detect the Augment GitHub App installation**
Make sure you don't already have the app installed in your GitHub account.
If you do, remove it using the [Cleanup](#cleanup) instructions, and 
try again.

**Cosmos cannot see my repository.**
The GitHub App is probably installed on a different account, or scoped to
different repositories. Check **Settings → Applications** on GitHub, open the
Cosmos app's configuration, and confirm your fork is in the selected list.

**The GitHub App install was blocked.**
Organization accounts can require an owner to approve third-party apps. Fork to
a personal account instead.

**The change did not fix the problem.**
Say so in the loop and give it the symptom again, more precisely. Describing
what is still wrong is a legitimate move — that is what the human checkpoint is
for. Your credits cover several attempts.

**`npm run dev` fails (Step 4 only).**
Check your Node version with `node --version`. Vite 7 needs Node 20.19 or later,
or 22.12 or later.
