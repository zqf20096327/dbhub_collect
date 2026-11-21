# MOKI Taskboard for DSH

[English](README.md) · [简体中文](README.zh-CN.md) · [Releases](https://github.com/JKZeng-cell/moki-taskboard-for-dsh/releases)

**Windows · DSH plugin v0.1.12 · MIT**

[DSH community showcase](https://github.com/deepseek-ai/deepseek-harness/discussions/13890) · [DSH launch covers and carousel](media/dsh-launch/README.md)

MOKI adds a project taskboard to DeepSeek Harness Desktop. Track requests from chats, dispatch tasks to DSH sessions, and open versioned files beside the board while reviewing a delivery.

[Install](#install) · [Projects](#projects) · [Chat capture](#capture) · [Quick submission](#quick) · [Files](#files) · [Review](#review)

Open the field notes in DSH. The asset list stays on the left and the selected revision opens in a tab on the right.

[![DSH workspace showing the asset list on the left and the v2 Markdown table on the right](media/walkthrough/en/13-side-preview.webp)](media/walkthrough/en/13-side-preview.webp)

<a id="projects"></a>

## Find the project, then choose a task view

Open **Project overview** in the sidebar. The spring issue has work awaiting review. Select its project row to see what needs attention.

[![Project portfolio with two projects, status counts and progress](media/walkthrough/en/01-portfolio.webp)](media/walkthrough/en/01-portfolio.webp)

The project overview shows its task progress and latest release. In **Task activity**, select a day, week or month to see which tasks changed in that period.

[![Inside the spring issue project, with progress, project information, activity and releases](media/walkthrough/en/02-dashboard.webp)](media/walkthrough/en/02-dashboard.webp)

<details>
<summary>Weekly activity in the running panel</summary>

[![Weekly activity with a selected week and its list of tasks](media/walkthrough/en/03-activity.webp)](media/walkthrough/en/03-activity.webp)

</details>

Switch to **Tasks** to see work arranged in status columns.

[![Task board with status columns and the quick composer at the bottom](media/walkthrough/en/04-board.webp)](media/walkthrough/en/04-board.webp)

On **Tasks**, switch from the board to the table. Each row shows the task status and input count. Open a row to see its instructions and files.

[![The same tasks in the table, with status and input counts per row](media/walkthrough/en/05-table.webp)](media/walkthrough/en/05-table.webp)

<a id="capture"></a>

## Turn a chat request into a project task

In **Chats → Capture settings**, enable semantic capture and select the directory scope. The example is limited to the project and its additional directories. The chosen host and model process conversations within that scope.

[![Capture settings with semantic matching enabled for project directories](media/walkthrough/en/06-scope.webp)](media/walkthrough/en/06-scope.webp)

The editor asks for a water-stop card naming two stops on the north route. Expand the matched chat. The match reason points to the spring issue, and the record contains the original request and a linked task.

[![Expanded captured chat with the match reason, linked task and source quote](media/walkthrough/en/07-session.webp)](media/walkthrough/en/07-session.webp)

Click the task title inside that record. It opens the to-do card. Its **Source chat** links the instructions back to the editor’s words.

[![Task detail opened from the chat, with a source link and the original request](media/walkthrough/en/08-source-task.webp)](media/walkthrough/en/08-source-task.webp)

<a id="quick"></a>

## Submit a task with an attachment

Use the composer at the bottom of the panel. Put the title on the first line, add instructions on the next line and attach the route card. Select the spring issue and the to-do option, then press **Ctrl+Enter**. The card appears in the to-do column. Open it and expand its inputs to find the Markdown file pinned at **v1**.

[![Three frames showing the filled composer, the created card and the pinned input ](media/walkthrough/en/quick-submission.gif)](media/walkthrough/en/quick-submission.gif)

Still frames: [Compose](media/walkthrough/en/09-quick-draft.webp) · [Creation receipt](media/walkthrough/en/10-quick-created.webp) · [Pinned input](media/walkthrough/en/11-quick-input.webp)

<a id="files"></a>

## Open the version you need

In **Assets**, expand the version control next to the field notes. This file has a first draft and a second revision. Preview a specific revision to inspect the text used at that point.

[![Expanded version history for the field notes, showing v2 and v1](media/walkthrough/en/12-versions.webp)](media/walkthrough/en/12-versions.webp)

Open a second file to keep both previews in tabs. Closing the active tab returns to the other open file.

<a id="review"></a>

## Check the delivery and record the decision

Open the proof task in **Review** and choose **Review this run**. The delivery contains a PNG card and a Markdown proof. Inspect the thumbnail, the text and the checks. All six automatic checks passed in this example, and the editor still has to sign off.

[![Delivery review dialog with an image proof, Markdown proof and six passed checks](media/walkthrough/en/14-review.webp)](media/walkthrough/en/14-review.webp)

<details>
<summary>Enlarged proof and decision controls</summary>

[![Enlarged image proof with the two station names and their positions](media/walkthrough/en/14b-proof.webp)](media/walkthrough/en/14b-proof.webp)

[![Review note and controls to approve or send the task back to the backlog](media/walkthrough/en/14c-decision.webp)](media/walkthrough/en/14c-decision.webp)

</details>

Enter the review note and choose **Approve**. The task changes to **Done**, with its proof and review still attached. Returning it to the backlog is also available from the review form.

[![Completed task with its accepted review and original delivery](media/walkthrough/en/15-accepted.webp)](media/walkthrough/en/15-accepted.webp)

If the proof needs another pass, open **Continue refining**, enter the change, attach the markup, and choose the execution session. Submitting starts a new round with the follow-up and previous delivery. The screenshot shows the draft before submission.

[![Refinement dialog with a follow-up request, an attached editorial note and a session selector](media/walkthrough/en/16-refine.webp)](media/walkthrough/en/16-refine.webp)

<a id="install"></a>

## Install


Tested with DeepSeek Harness Desktop 0.2.2-rc.1 on Windows. Download the [0.1.12 package](https://github.com/JKZeng-cell/moki-taskboard-for-dsh/releases/download/v0.1.12/dsh-moki-taskboard-0.1.12.tgz), select the local tgz in the desktop plugin manager, or run the following from its download folder with the CLI for your desktop installation.

```powershell
$archive = (Resolve-Path '.\dsh-moki-taskboard-0.1.12.tgz').Path.Replace('\', '/')
dsh plugin --profile desktop add "dsh-moki-taskboard@file:$archive"
dsh plugin --profile desktop list dsh-moki-taskboard --depth 0
```
Reopen DSH and select MOKI Taskboard for DSH in the sidebar. Files open in the right-hand preview. Approval notifications take you to the originating DSH session. Scheduling and session capture require the host to be running.

[Adapter and buildable source for this release](https://github.com/JKZeng-cell/moki-taskboard/tree/v0.2.23/ports/dsh) · [Build instructions](https://github.com/JKZeng-cell/moki-taskboard/tree/v0.2.23)

The project database and managed files are stored locally. Starting an agent or using semantic capture sends the relevant content to the selected host and model and uses that account’s model allowance.

[Chinese carousel and publication copy](https://github.com/JKZeng-cell/moki-taskboard/tree/main/media/launch/field-guide) · [Download media kit](https://github.com/JKZeng-cell/moki-taskboard-for-dsh/releases/download/v0.1.12/moki-taskboard-visual-guide-zh-v2.zip)

Screenshots show the released plugin panel running against an isolated sample project. The sample names and editorial files are in Chinese.
