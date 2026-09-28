# APEX Off Grid

APEX Offline for everyone thanks to a Low Code API with Plug-Ins

<img src="https://raw.githubusercontent.com/phartenfeller/apex-off-grid/main/assets/apex-off-grid-logo.png" width="400" >

[Watch this tutorial video](https://youtu.be/D9aTzsYK7MQ)

## Features

- Low Code API thanks to APEX Plug-Ins
- Data Synchronization
  - Input SQL Query -> Data gets downloaded and synced back
  - Changes get saved to local storage
  - Changes get synced back to server
  - Conflict detection and resolution possible with your own logic
- Super fast and able to handle lots of data amounts thanks to SQLite
## How to get started

### Prerequisites

- APEX >= 23.2
- Following HTTP Response Headers are required

```
Cross-Origin-Embedder-Policy: require-corp
Cross-Origin-Opener-Policy: same-origin
```
<details>
  <summary>Current APEX Bug: setting headers in shared components does not work!</summary>

There is a setting in APEX to set these headers. [There currently is a bug](https://twitter.com/chrisneumueller/status/1649367365342093313?s=20) that results in these headers not being set on Plug-In files. So this solution **currently does not work**.

![App > Shared Components > Security > Browser Security > HTTP Response Headers](./assets/http-headers-apex.png)

</details>

**So you need to set these headers in your Webserver or Proxy.**

- [Here is an example](https://docs.oracle.com/en/database/oracle/oracle-rest-data-services/23.4/ordig/miscellaneous-configuration-options-of-ORDS.html#GUID-A3798C5A-C6C6-40A2-826F-CE1CF0B8DDE2)  on how to it with ORDS standalone (Example 5-3).

[More info on the header requirement](https://sqlite.org/wasm/doc/trunk/persistence.md#:~:text=COOP%20and%20COEP%20HTTP%20Headers).

### Installation

Go to the latest release and download the installation zip file. For the base installation you run the tables and package scripts. Afterwards import the plug-ins.

### Install sample app

Read the [Installation Guide](./sample-apps/recipes/readme.md)

### How to build your own app

1. Import Plug-Ins from release download into your app
2. [Watch this tutorial video](https://youtu.be/D9aTzsYK7MQ)

x. After you defined your storage, you have to define the DML logic in the package `offline_data_sync_api.sync_row`:

```sql
case 
  when pi_sync_storage_id = 'ingredients' and pi_sync_storage_version = 1 then

	  recipe_offline_sync_api.sync_ingredients_v1 (
			pi_json                 => l_json
		, pi_change_type          => l_change_type
		, pi_change_date          => l_change_date
		, pi_updated_by           => v('APP_USER')
		, po_success              => po_success
		, po_sync_fail_reason     => po_sync_fail_reason
		, po_sync_device_pk       => po_sync_device_pk
		, po_snyc_db_pk           => po_snyc_db_pk
	  );
```

## Caution

- This is a proof of concept
- There is no warranty or support garantee
- I am working on this in my free time 
- I am not responsible for any data loss or damage
- Only a small fraction of APEX features are supported
- You can't just make your existing APEX app offline capable with this. You have to build your app with this in mind.
- The users could download the Database and get control over all offline available data
- The users could manipulate the data in the local database with malicious intent

## Resources

Download SQLite WASM buidl from [here](https://sqlite.org//download.html#:~:text=WebAssembly%20%26%20JavaScript)
