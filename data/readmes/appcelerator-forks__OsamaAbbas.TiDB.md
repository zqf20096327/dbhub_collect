# TiDB
 Embedded datastore for Titanium Appcelerator. Based on [nedb].

### What is TiDB?

NeDB, is an Embedded persistent database for Node.js, written in Javascript,
with no dependency (except npm modules of course). You can think of it as
a SQLite for Node.js projects, which can be used with a simple require
statement. The API is a subset of MongoDB's. You can use it as a persistent or
an in-memory only datastore.

TiDB, is Titanium Appcelerator version of NeDB. NeDB uses some native Node.js
modules (mainly fs, path, util ... etc). So I have re-written the required
functions from these modules to make it compatible with Titanium API.

### How to use?

* Copy ```./TiDB.js``` and ```./lib``` to your project Resources.
* Require it:
```javascript
var TiDB = require('path/to/TiDB');
```
* Creating/loading a database:
```javascript
var myDB = new TiDB({
	filename : Ti.Filesystem.externalStorageDirectory + '/myDB.db',
	autoload : true
});
```
* Note that ```filename``` will be passed to ```Ti.Filesystem``` functions. It
should start with ```file://```. You can also use
```Ti.Filesystem.File.nativePath``` property.
* For more information, check [nedb].

### TODO:

* benchmark against [TiTaffyDb].
* benchmark against native sqlite.
* benchmark against ```Ti.App.Properties.getObject``` and similar functions.

[nedb]:https://github.com/louischatriot/nedb
[TiTaffyDb]:https://github.com/benbahrenburg/TiTaffyDb
