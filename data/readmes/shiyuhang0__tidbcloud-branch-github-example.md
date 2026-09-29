# tidbcloud-branch-github-example

> **Warning:** TiDB Cloud Branch and the corresponding GitHub App are still in beta. You can't get the GitHub integration in the TiDB Cloud website if you are not the PingCAP staff.


This repo has been connected to a TiDB Cloud cluster using the TiDB Cloud GitHub integration. This brings database branches to your GitHub workflows, the TiDB Cloud App will automatically manage database branches for you when PR, commits are created.

You can open a PR in this repo to have a try. You can also use this step-by-step tutorial to build your example.

- [Before you start](#before-you-start)
- [Connect TiDB Cloud to your GitHub repository](#connect-tidb-cloud-to-your-github-repository)
- [GitHub App](#github-app)
  * [Open a PR](#open-a-pr)
  * [New commit in a PR](#new-commit-in-a-pr)
  * [Close a PR](#close-a-pr)
  * [Reopen a PR](#reopen-a-pr)
- [Configuring GitHub App](#configuring-for-github-app)
  * [branch.blackList](#branchblacklist)
  * [branch.whiteList](#branchwhitelist)
  * [branch.level](#branchlevel)
  * [branch.autoReserved](#branchautoreserved)
  * [branch.autoDestroy](#branchautodestroy)
- [Use the Branch in GitOps Workflow](#use-the-branch-in-gitops-workflow)

## Before you start

Before you start, make sure you have:

- A TiDB Cloud account
- A GitHub account
- Create a TiDB Cloud cluster
- Create A GitHub repository


## Connect TiDB Cloud to your GitHub repository

1. Go to the integrations page under the admin, then you can find the GitHub integration

<img width="1417" alt="image" src="https://user-images.githubusercontent.com/52435083/233818397-96e2c8d6-5971-4f2b-b9a6-e278293cf9f4.png">

2. Go to the GitHub integration and click the `connect` button. 
    - If you have not login the GitHub, you will be asked to login in the GitHub account in a pop-up. 
    - If it is the first time you use the integration, you will be asked to authorize the GitHub app in a pop-up.
    
<img width="793" alt="image" src="https://user-images.githubusercontent.com/52435083/233824789-37c55dfb-939f-48bd-8773-9e47aa3bdd7a.png">


3. Select A TiDB Cloud 

You will enter the connect page after clicking the connect button. Select the cluster under the project first.

<img width="1063" alt="image" src="https://user-images.githubusercontent.com/52435083/233825019-a85b306a-52c8-415b-bbb1-907cc5792ad4.png">

4. Install and select an account

If it is the first time you use the integration. you need to install the GitHub app for your account. Click the `GitHub account` and choose the `install other account`, you will be redirected to an install page.

<img width="780" alt="image" src="https://user-images.githubusercontent.com/52435083/233826052-cc63d74b-c12d-4c44-ac5a-5173633737c5.png">

After you have installed your account, it will be shown under the `GitHub account` drop-down. Select the account you need.

5. Select a repository under the account

Choose a repository under the account you selected.

<img width="1107" alt="image" src="https://user-images.githubusercontent.com/52435083/233826252-1469f6d5-a6e2-4a6c-8d77-1dc1dc30f4ee.png">


6. Connect

Click the `Connect` button to connect between the TiDB Cloud cluster and The GitHub repository. 

<img width="1117" alt="image" src="https://user-images.githubusercontent.com/52435083/233826403-b9480b8d-9c95-47b6-a4b3-6c76885c1341.png">


## GitHub App

After you connect a TiDB Cloud cluster to a GitHub repository. A GitHub App will work in this repository, trying to manage TiDB Cloud Branch in every PR.

### Open a PR

GitHub App will create a TiDB Cloud Branch every time you open a PR under the repository. The branch name is `${github_branch_name}_${pr_id}_${commit_sha}`

<img width="823" alt="image" src="https://user-images.githubusercontent.com/52435083/233826740-9cdf13a2-b8cf-4a59-b7b4-5c2756440a79.png">

### New commit in a PR

GitHub App will delete the previous branch and create a new TiDB Cloud Branch for the lasted commit.

<img width="821" alt="image" src="https://user-images.githubusercontent.com/52435083/233826906-dd792d46-eb3d-457c-b22e-4134ffcc0ed7.png">

### Close or merge a PR

GitHub App will delete all the branches in this PR.

### Reopen a PR

GitHub App will create a branch for the lasted commit.

## Configuring GitHub App

The following configuration options can be used through a tidbcloud.yml file in the root of your repository.

### branch.blackList

**type:** Array of string. **Default:** `[]`.

Specify the branches that forbid the GitHub App, even if it is in the whiteList.

```
github:
    branch:
       blackList:
           - ".*_doc"
           - ".*_blackList"
```

### branch.whiteList

**type:** Array of string. **Default:** `[.*]`.

Specify the branches that allow the GitHub App.

```
github:
    branch:
       whiteList: 
           - ".*_db"
```

### branch.autoReserved

**type:** boolean. **Default:** `false`.

If set to true, TiDB Cloud App will not delete the TiDB Cloud branch which created in the previous commit.

```
github:
    branch:
       autoReserved: false
```

### branch.autoDestroy

**type:** boolean. **Default:** `true`.

If set to false, TiDB Cloud App will not delete the TiDB Cloud branch when the pull request is closed.

```
github:
    branch:
       autoDestroy: true
```

## Use the Branch in GitOps Workflow

It is highly recommended running your CI with the TiDB Cloud branch rather than the production cluster before merging the pull request.

Use [wait-for-tidbcloud-branch]() action to wait for the ready of the TiDB Cloud branch and get the connection information.

Here is an example:

```
steps:
  - name: Wait for TiDB Cloud branch ready
    uses: tidbcloud/wait-for-tidbcloud-branch@v0
    id: wait-for-branch
    with:
      token: ${{ secrets.GITHUB_TOKEN }}
      publicKey: ${{ secrets.TIDB_CLOUD_API_PUBLIC_KEY }}
      privateKey: ${{ secrets.TIDB_CLOUD_API_PRIVATE_KEY }}

  - name: Test with TiDB Cloud branch
     run: |
        echo "The host is ${{ steps.wait-for-branch.outputs.host }}"
        echo "The user is ${{ steps.wait-for-branch.outputs.user }}"
        echo "The password is ${{ steps.wait-for-branch.outputs.password }}"
```



