# Cross-platform SQLite storage plugin for Cordova / PhoneGap - cordova-sqlite-storage plugin version

Native SQLite component with API based on HTML5/[Web SQL (DRAFT) API](http://www.w3.org/TR/webdatabase/) for the following platforms:

- browser
- Android
- iOS

and *deprecated* desktop platforms:

- macOS ("osx" platform)
- Windows 10 (UWP) DESKTOP ~~and MOBILE~~ (see below for major limitations)

The browser platform is now supported with the following options:
- This plugin now supports the browser platform using [`storesafe/sql.js`](https://github.com/storesafe/sql.js) (fork of [`sql-js/sql.js`](https://github.com/sql-js/sql.js)), with no persistence and other limitations described below.
- Other alternatives documented in the [**alternative browser platform usage notes**](#alternative-browser-platform-usage-notes) section below.

**LICENSE:** MIT, with Apache 2.0 option for Android and Windows platforms (see [`LICENSE.md`](./LICENSE.md) for details, including third-party components used by this plugin)

## WARNINGS

- [**Multiple SQLite corruption problem**](#warning-multiple-sqlite-problem-on-multiple-platforms) - see section below & [`storesafe/cordova-sqlite-storage#626`](https://github.com/storesafe/cordova-sqlite-storage/issues/626)
- [**Breaking changes coming soon**](#breaking-changes-coming-soon) - see section nearby & see [`storesafe/cordova-sqlite-storage#922`](https://github.com/storesafe/cordova-sqlite-storage/issues/922)

## Comparison of supported plugin versions

| | Free license terms | Commercial license & support |
| --- | --- | --- |
| [`cordova-sqlite-storage`](https://github.com/storesafe/cordova-sqlite-storage) - core plugin version | MIT (or Apache 2.0 on Android & Windows) | |
| [`cordova-sqlite-ext`](https://github.com/brodybits/cordova-sqlite-ext) - with extra features including BASE64 (SELECT BLOB in Base64 format), REGEXP, and pre-populated databases | MIT (or Apache 2.0 on Android & Windows) | |
| [`cordova-sqlite-evcore-extbuild-free`](https://github.com/storesafe/cordova-sqlite-evcore-extbuild-free) - plugin version with lighter resource usage in Android NDK | GPL v3 | available - see <https://storesafe.io/> or contact <sales@storesafe.io> |
| [`cordova-plugin-sqlite-evplus-ext-common-free`](https://github.com/storesafe/cordova-plugin-sqlite-evplus-ext-common-free) - includes workaround for extra-large result data on Android and lighter resource usage on iOS, macOS, and in Android NDK | GPL v3 | available - see <https://storesafe.io/> or contact <sales@storesafe.io> |
| [`cordova-sqlcipher-adapter`](https://github.com/storesafe/cordova-sqlcipher-adapter) - includes encryption functionality using [SQLCipher](https://www.zetetic.net/sqlcipher/) for Android/iOS/macOS | Permissive (see [`cordova-sqlcipher-adapter`](https://github.com/storesafe/cordova-sqlcipher-adapter) for details) | available - contact <sales@storesafe.io> |
| [`cordova-sqlite-express-build-support`](https://github.com/storesafe/cordova-sqlite-express-build-support) - using built-in SQLite libraries on Android, iOS, and macOS - may be missing some important SQLite updates | MIT (or Apache 2.0 on Android & Windows) | available - contact <sales@storesafe.io> |

### in progress

New SQLite plugin design with a simpler API with a working demo - see [`brodybits/ask-me-anything#3`](https://github.com/brodybits/ask-me-anything/issues/3)


## Breaking changes coming soon

in an upcoming major release - see [`storesafe/cordova-sqlite-storage#922`](https://github.com/storesafe/cordova-sqlite-storage/issues/922)

some highlights:

- error `code` will always be `0` (which is already the case on browser and Windows); actual SQLite3 error code will be part of the error `message` member whenever possible (see [`storesafe/cordova-sqlite-storage#821`](https://github.com/storesafe/cordova-sqlite-storage/issues/821))
- drop support for location: 0-2 values in openDatabase call (please use `location: 'default'` or `iosDatabaseLocation` setting 

[...截断...]

in openDatabase as documented below)
- throw an exception in case of `androidDatabaseImplementation: 2` setting which is now superseded by `androidDatabaseProvider: 'system'` setting

under consideration:

- remove `androidLockWorkaround: 1` option if not needed any longer - [`storesafe/cordova-sqlite-storage#925`](https://github.com/storesafe/cordova-sqlite-storage/issues/925)

## About this plugin version

This is a common plugin version branch which supports the most widely used features and serves as the basis for other plugin versions.

This version branch uses a `before_plugin_install` hook to install sqlite3 library dependencies from `cordova-sqlite-storage-dependencies` via npm.

<!-- XXX TBD WORKING CI WANTED in the future:
|Android Circle-CI (**full** suite)|iOS Travis-CI (partial suite)|
|-----------------------|----------------------|
| XXX TBD  ------------ | XXX TBD ------------ |
 -->

<!-- FUTURE TBD critical bug notices for this plugin version -->

<!-- END About this plugin version branch -->

## WARNING: Multiple SQLite problem on multiple platforms

### Multiple SQLite problem on Android

This plugin uses non-standard [`android-sqlite-native-ndk-connector`](https://github.com/brodybits/android-sqlite-native-ndk-connector) implementation with [`android-sqlite-ndk-native-driver`](https://github.com/brodybits/android-sqlite-ndk-native-driver) on Android. In case an application access the **same** database using multiple plugins there is a risk of data corruption ref: [`storesafe/cordova-sqlite-storage#626`](https://github.com/storesafe/cordova-sqlite-storage/issues/626)) as described in <http://ericsink.com/entries/multiple_sqlite_problem.html> and <https://www.sqlite.org/howtocorrupt.html>.

The workaround is to use the `androidDatabaseProvider: 'system'` setting as described in the [**Android database provider**](#android-database-provider) section below:

```js
var db = window.sqlitePlugin.openDatabase({
  name: 'my.db',
  location: 'default',
  androidDatabaseProvider: 'system'
});
```

### Multiple SQLite problem on other platforms

This plugin version also uses a fixed version of sqlite3 on iOS, macOS, and Windows. In case the application accesses the **same** database using multiple plugins there is a risk of data corruption as described in <https://www.sqlite.org/howtocorrupt.html> (similar to the multiple sqlite problem for Android as described in <http://ericsink.com/entries/multiple_sqlite_problem.html>).

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
    con