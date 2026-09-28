![version](https://raw.githubusercontent.com/Saka7/sqlibri/master/src/com/sqlibri/resources/image/version.png)
[![Code Climate](https://codeclimate.com/github/Saka7/sqlibri/badges/gpa.svg)](https://codeclimate.com/github/Saka7/sqlibri)
[![Issue Count](https://codeclimate.com/github/Saka7/sqlibri/badges/issue_count.svg)](https://codeclimate.com/github/Saka7/sqlibri)

![sqlibri-logo](https://raw.githubusercontent.com/Saka7/sqlibri/master/SQLibri.png)

# SQLibri - the lightweight sqlite GUI client
SQLibry is a platform independent SQLite GUI client.

# Build and run
- Navigate to project parent folder and run `gradle build` to build the project 
- Then `gradle run` or `java -jar build/libs/sqlibri-[version].jar` to run it

> Note: To run this application you need [Java SE 1.8.0_40+](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html) and [Gradle 2+](https://gradle.org/install)

# Getting started
It this section we collect all information which is essential to figure out how to use the application. You can find this tutorial inside the application by pressing `CTRL/COMMAND+SHIFT+H` or find it in HELP -> USER GUIDE menu.

## Working with database
### Creating database
First of all we need to figure out how to create a database. And it's simple as pie. Just click on **DATABASE** menu -> then on **CREATE** menu item / or press `CTRL/COMMAND+N`, enter database path and name and click OK.

![Creating database](https://raw.githubusercontent.com/Saka7/sqlibri/master/src/com/sqlibri/resources/image/Database-Create.png)

### Opening database
To open database click on **DATABASE** menu -> **OPEN** menu item / or press `CTRL/COMMAND+O`, enter database path and name and click ok.

![Opening database](https://raw.githubusercontent.com/Saka7/sqlibri/master/src/com/sqlibri/resources/image/Database-Open.png)

### Droping database
TO drop database click on **DATABASE** menu -> **DROP** menu item -> and press ok. It will drop currently opened database.

![Droping database](https://raw.githubusercontent.com/Saka7/sqlibri/master/src/com/sqlibri/resources/image/Database-Drop.png)

### Copying database
To copy database click on **DATABASE** menu -> **COPY** menu item / or press 	`CTRL/COMMAND+SHIFT+C`, enter file path and name and press ok. It will copy currently opened database to new one(which is located by entered filepath).

![Copying database](https://raw.githubusercontent.com/Saka7/sqlibri/master/src/com/sqlibri/resources/image/Database-Copy.png)

## Working with SQL editor
### Writing and executing SQL queries
You can write SQL queries in the SQL Editor, which provides some advanced code editor features like syntax highlighting, intellisence and snippets. To run the query click on **EXECUTE** button or press **F9**. Query execution info will be displayed in the status bar. If query returns any data it will be displayed in the table view.

![Working with SQL editor](https://raw.githubusercontent.com/Saka7/sqlibri/master/src/com/sqlibri/resources/image/SQLEditor.png)

### Navigating through previously executed queries
When query has been executed, it saves to history. You can search and select previously executed queries using history combobox.

![Queries History](https://raw.githubusercontent.com/Saka7/sqlibri/master/src/com/sqlibri/resources/image/History.png)


## Working with query files
### Saving Queries
To save written before query you need to click on **FILE** menu -> **SAVE QUERY** menu item / or pres `CTRL/COMMAND+S` and enter file path and name.

![Saving queries](https://raw.githubusercontent.com/Saka7/sqlibri/master/src/com/sqlibri/resources/image/File-SaveQuery.png)

### Opening Queries
To open saved before query you need to click on **FILE** -> **LOAD QUERY** menu item / or press `CTRL/COMMAND+SHIFT+O` and enter file path and name.

![Opening Queries](https://raw.githubusercontent.com/Saka7/sqlibri/master/src/com/sqlibri/resources/image/File-LoadQuery.png)

## Exporting as CSV
### Exporting data to CSV file
to Export data from table view to CSV file you need to click on  **FILE** menu -> **EXPORT AS CSV** menu item / or press `CTRL/COMMAND+E`, enter file name and press ok.

![Exporting as CSV](https://raw.githubusercontent.com/Saka7/sqlibri/master/src/com/sqlibri/resources/image/File-ExportAsCSV.png)

# Shortcuts

|Key|Command|
|:--	|:--	|
| CTRL/COMMAND+S | Save Query |
| CTRL/COMMAND+Shift+O | Open Query |
| CTRL/COMMAND+E | Export As CSV|
| CTRL/COMMAND+X | Exit |
| CTRL/COMMAND+N | Create Database |
| CTRL/COMMAND+O | Open Database |
| CTRL/COMMAND+Shift+C | Copy Database|
| CTRL/COMMAND+Shift+H | Open User Guide|

# Snippets

|keyword|expanded|
|:--	|:--	|
| tbl | Create table |
| col | Create column |
| ccol | Create column (varchar type) |
| ncol | Create column (number type) |
| dcol | Create column (date type) |
| ind | Create index on column |
| uind | Create unique index on column |
| s* | Select all from table |
| addcol | Add column to the table |
| seq | Create sequence |
| tblcom | Create comment on table |
| colcom | Create comment on column |
| ins | Insert row(s) to table |
| upt | Update row(s) |
| dt | Drop table |
| dl | Delete row(s) from table |

# License
SQLibri is released under the [BSD-3 License](https://opensource.org/licenses/BSD-3-Clause).
