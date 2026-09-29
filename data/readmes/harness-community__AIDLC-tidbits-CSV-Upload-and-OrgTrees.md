# AI DLC Insights Tidbit: Upload Developer CSV & Build Org Trees

## What this Tidbit covers

This Tidbit walks through the CSV upload and Org Tree creation steps of AI DLC Insights onboarding! This tidbit covers the following:

- Uploading a developer dataset via CSV
- Mapping CSV columns to AI DLC Insights fields (Display Name, Email, Manager Email, Role)
- Building an Org Tree from that data so reporting hierarchy and teams are derived automatically

No integrations or profiles setup in this video — just developer records in, Org Tree out.

## Repo contents

- `example-developers.csv` — a real 14-developer dataset (Dev1–Dev14, harness.io test emails) used as the upload example in the walkthrough

## CSV requirements

AI DLC Insights expects one row per developer. Only three columns are truly required:

- `full_name`
- `email`
- `manager_email`

These are supported but optional — include them if you have the data, since they're what let AI DLC Insights map developers to teams and metrics:

- `role`
- `sub_role`
- `team`
- `department`
- `site`


Standards your source data needs to meet before upload:

| Requirement | Why it matters |
|---|---|
| Managers must also exist as developers | Every `manager_email` must also appear as its own developer row, so AI DLC Insights can build an accurate reporting hierarchy |
| No cyclic relationships | Circular manager chains (A → B → A) break hierarchy creation |
| Unique developer emails | Duplicate emails cause ingestion errors or incorrect identity attribution |
| No missing values | Whatever columns you include, populate them for every record — gaps cause failure |
| Email correctness | Use the same emails developers use in GitHub, Jira, etc., or AI DLC Insights can't link identities correctly |
| No blank column headers | Every column needs a valid header, or validation fails |
| Top Manager has Manager Email Field blank | The top manager user of your org tree will not need to have the manager email field filled out. This is the only user who can have a blank field in this column.



**The CSV has to describe one complete tree.** Every `manager_email` value must point to a row that exists in the same file — no manager referenced who isn't also a developer record. There can only be one root (one row with no manager), and every other row has to connect back to that root through the chain of managers. A dangling manager reference or a second disconnected root breaks the hierarchy build, even if every individual row looks valid on its own.

## example-developers.csv structure

14 developers, 3 levels deep:

- Dev3 — root, no manager
- Dev11 and Dev14 — report to Dev3, 7 and 4 direct reports respectively
- The remaining 11 developers report to either Dev11 or Dev14


## Walkthrough steps

1. **Upload the CSV**
   Account Management → Developers → Upload New CSV → select `example-developers.csv`

2. **Map columns**
   Developer Preview screen — map `name` → Display Name, `email` → Email, `manager email` → Manager Email, `Role` → Role

3. **Review the hierarchy**
   Check Developer Data and Developer Mappings tabs to confirm all 14 records processed without errors

4. **Create the Org Tree**
   Org Trees → + Create Org Tree → name it → choose `Manager Email` as the grouping level → review the Tree View preview to confirm it matches the 3-level structure above


## Notes
- If you re-upload an updated CSV later, AI DLC Insights detects changes (new hires, reporting line moves) and rebuilds the Org Tree
