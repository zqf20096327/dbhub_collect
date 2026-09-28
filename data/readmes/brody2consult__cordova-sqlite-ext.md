# Cordova/PhoneGap sqlite storage adapter with extra features

Native SQLite component with API based on HTML5/[Web SQL (DRAFT) API](http://www.w3.org/TR/webdatabase/) for the following platforms:
- Android
- iOS
- macOS ("osx" platform)
- Windows 10 (UWP) DESKTOP ~~and MOBILE~~ (see below for major limitations)

<!-- [TBD] HIDE browser usage notes for now (at least):
Browser platform is currently supported with some limitations as described in [browser platform usage notes](#browser-platform-usage-notes) section below, will be supported with more features such as numbered parameters and SQL batch API in the near future.
- -->

**LICENSE:** MIT, with Apache 2.0 option for Android and Windows platforms (see [LICENSE.md](./LICENSE.md) for details, including third-party components used by this plugin)

## WARNINGS

- **Multiple SQLite corruption problem** - see section below & [`xpbrew/cordova-sqlite-storage#626`](https://github.com/xpbrew/cordova-sqlite-storage/issues/626)
- **Breaking changes coming soon** - see section nearby & see [`xpbrew/cordova-sqlite-storage#922`](https://github.com/xpbrew/cordova-sqlite-storage/issues/922)

## Comparison of supported plugin versions

| | Free license terms | Commercial license & support |
| --- | --- | --- |
| [`cordova-sqlite-storage`](https://github.com/xpbrew/cordova-sqlite-storage) - core plugin version | MIT (or Apache 2.0 on Android & Windows) | |
| [`cordova-sqlite-express-build-support`](https://github.com/xpbrew/cordova-sqlite-express-build-support) - using built-in SQLite libraries on Android, iOS, and macOS | MIT (or Apache 2.0 on Android & Windows) | |
| [`cordova-sqlite-ext`](https://github.com/brodybits/cordova-sqlite-ext) - with extra features including BASE64, REGEXP, and pre-populated databases | MIT (or Apache 2.0 on Android & Windows) | |
| [`cordova-sqlite-evcore-extbuild-free`](https://github.com/brodysoft/cordova-sqlite-evcore-extbuild-free) - plugin version with lighter resource usage in Android NDK | GPL v3 | available, see <https://xpbrew.consulting/> |
| [`cordova-plugin-sqlite-evplus-ext-common-free`](https://github.com/brodysoft/cordova-plugin-sqlite-evplus-ext-common-free) - includes workaround for extra-large result data on Android and lighter resource usage on iOS, macOS, and in Android NDK | GPL v3 | available, see <https://xpbrew.consulting/> |

### COMING SOON

New SQLite plugin design with a simpler API is in progress with a working demo - see [`brodybits/ask-me-anything#3`](https://github.com/brodybits/ask-me-anything/issues/3)


## Breaking changes coming soon

in an upcoming major release - see [`xpbrew/cordova-sqlite-storage#922`](https://github.com/xpbrew/cordova-sqlite-storage/issues/922)

some highlights:

- error `code` will always be `0` (which is already the case on Windows); actual SQLite3 error code will be part of the error `message` member whenever possible (see [`xpbrew/cordova-sqlite-storage#821`](https://github.com/xpbrew/cordova-sqlite-storage/issues/821))
- drop support for location: 0-2 values in openDatabase call (please use `location: 'default'` or `iosDatabaseLocation` setting in openDatabase as documented below)
- throw an exception in case of `androidDatabaseImplementation: 2` setting which is now superseded by `androidDatabaseProvider: 'system'` setting

under consideration:

- remove `androidLockWorkaround: 1` option if not needed any longer - [`xpbrew/cordova-sqlite-storage#925`](https://github.com/xpbrew/cordova-sqlite-storage/issues/925)

## About this plugin version

_Version with extra features: REGEXP (Android/iOS/macOS), BASE64, BLOBFROMBASE64, and pre-populated databases_

This plugin version uses a `before_plugin_install` hook to install sqlite3 library dependencies from `cordova-sqlite-ext-deps` via npm.

<!-- XXX TBD WORKING CI WANTED in the future:
|Android Circle-CI (**full** suite)|iOS Travis-CI (partial suite)|
|-----------------------|----------------------|
| XXX TBD  ------------ | XXX TBD ------------ |
 -->

[...截断...]



<!-- FUTURE TBD critical bug notices for this plugin version -->

<!-- END About this plugin version branch -->

## WARNING: Multiple SQLite problem on multiple platforms

### Multiple SQLite problem on Android

This plugin uses non-standard [`android-sqlite-native-ndk-connector`](https://github.com/brodybits/android-sqlite-native-ndk-connector) implementation with [`android-sqlite-ndk-native-driver`](https://github.com/brodybits/android-sqlite-ndk-native-driver) on Android. In case an application access the **same** database using multiple plugins there is a risk of data corruption ref: [`storesafe/cordova-sqlite-storage#626`](https://github.com/storesafe/cordova-sqlite-storage/issues/626)) as described in <http://ericsink.com/entries/multiple_sqlite_problem.html> and <https://www.sqlite.org/howtocorrupt.html>.

The workaround is to use the `androidDatabaseProvider: 'system'` setting as described in the [Android database provider](#android-database-provider) section below:

```js
var db = window.sqlitePlugin.openDatabase({
  name: 'my.db',
  location: 'default',
  androidDatabaseProvider: 'system'
});
```

### Multiple SQLite problem on other platforms

This plugin version also uses a fixed version of sqlite3 on iOS, macOS, and Windows. In case the application accesses the SAME database using multiple plugins there is a risk of data corruption as described in <https://www.sqlite.org/howtocorrupt.html> (similar to the multiple sqlite problem for Android as described in <http://ericsink.com/entries/multiple_sqlite_problem.html>).

<!-- END WARNING: Multiple SQLite problem -->

## A quick tour

To open a database:

```Javascript
var db = null;

document.addEventListener('deviceready', function() {
  db = window.sqlitePlugin.openDatabase({
    name: 'my.db',
    location: 'default',
  });
});
```

**IMPORTANT:** Like with the other Cordova plugins your application must wait for the `deviceready` event. This is especially tricky in Angular/ngCordova/Ionic controller/factory/service callbacks which may be triggered before the `deviceready` event is fired.

### Using DRAFT standard transaction API

To populate a database using the DRAFT standard transaction API:

```Javascript
  db.transaction(function(tx) {
    tx.executeSql('CREATE TABLE IF NOT EXISTS DemoTable (name, score)');
    tx.executeSql('INSERT INTO DemoTable VALUES (?,?)', ['Alice', 101]);
    tx.executeSql('INSERT INTO DemoTable VALUES (?,?)', ['Betty', 202]);
  }, function(error) {
    console.log('Transaction ERROR: ' + error.message);
  }, function() {
    console.log('Populated database OK');
  });
```

or using numbered parameters as documented in <https://www.sqlite.org/c3ref/bind_blob.html>:

```Javascript
  db.transaction(function(tx) {
    tx.executeSql('CREATE TABLE IF NOT EXISTS DemoTable (name, score)');
    tx.executeSql('INSERT INTO DemoTable VALUES (?1,?2)', ['Alice', 101]);
    tx.executeSql('INSERT INTO DemoTable VALUES (?1,?2)', ['Betty', 202]);
  }, function(error) {
    console.log('Transaction ERROR: ' + error.message);
  }, function() {
    console.log('Populated database OK');
  });
```

To check the data using the DRAFT standard transaction API:

```Javascript
  db.transaction(function(tx) {
    tx.executeSql('SELECT count(*) AS mycount FROM DemoTable', [], function(tx, rs) {
      console.log('Record count (expected to be 2): ' + rs.rows.item(0).mycount);
    }, function(tx, error) {
      console.log('SELECT error: ' + error.message);
    });
  });
```

### Using plugin-specific API calls

<!-- [TBD] HIDE browser usage notes for now (at least):
NOTE: These samples will *not* work with alternative 3 for browser platform support discussed in [browser platform usage notes](#browser-platform-usage-notes).
- -->

To populate a database using the SQL batch API:

```Javascript
  db.sqlBatch([
    'CREATE TABLE IF NOT EXISTS DemoTable (name, score)',
    [ 'INSERT INTO DemoTable VALUES (?,?)', ['Alice', 101] ],
    [ 'INSERT INTO DemoTable VALUES (?,