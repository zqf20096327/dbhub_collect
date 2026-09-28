# Cordova/PhoneGap sqlite storage - free enterprise version with performance improvements for Android and extra features for PhoneGap Build

Native SQLite component with API based on HTML5/[Web SQL (DRAFT) API](http://www.w3.org/TR/webdatabase/) for the following platforms:
- Android
- iOS
- macOS ("osx" platform)
- Windows 10 (UWP) _DESKTOP ONLY, with ARM CPU support removed again from this plugin version_ (see below for major limitations)

<!-- [TBD] HIDE browser usage notes for now (at least):
Browser platform is currently supported with some limitations as described in [browser platform usage notes](#browser-platform-usage-notes) section below, will be supported with more features such as numbered parameters and SQL batch API in the near future.
- -->

This plugin version uses a special, non-standard Android NDK sqlite database access library (C-language implementation), with some premium improvements to the internal JSON interface between the Javascript and native Android implementation, to provide significant performance and memory usage improvements on the Android platform.

This plugin version is available under GPL v3 (<https://www.gnu.org/licenses/gpl-3.0.txt>) or commercial license options and includes components available under the MIT and Apache 2.0 licenses listed in [LICENSE.md](./LICENSE.md). Contact for commercial license: <sales@litehelpers.net>

NOTE: Commercial licenses for [litehelpers / Cordova-sqlite-enterprise-free](https://github.com/litehelpers/Cordova-sqlite-enterprise-free) are valid for this plugin version as well.

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
- throw an exception in case of `androidDatabaseImplementation: 2` settin

[...截断...]

g which is now superseded by `androidDatabaseProvider: 'system'` setting

under consideration:

- remove `androidLockWorkaround: 1` option if not needed any longer - [`xpbrew/cordova-sqlite-storage#925`](https://github.com/xpbrew/cordova-sqlite-storage/issues/925)

## About this plugin version

Free enterprise version with Android performance improvements and other features with sqlite3 dependencies included, working with PhoneGap Build.

<!-- FUTURE TBD critical bug notices for this plugin version -->

<!-- END About this plugin version branch -->

## WARNING: Multiple SQLite problem on multiple platforms

### Multiple SQLite problem on Android

__This plugin uses non-standard [android-sqlite-evcore-ndk-driver-free](https://github.com/storesafe/android-sqlite-evcore-ndk-driver-free) sqlite database access implementation on Android. In case an application access the SAME database using multiple plugins there is a risk of data corruption ref: [storesafe/cordova-sqlite-storage#626](https://github.com/storesafe/cordova-sqlite-storage/issues/626) as described in <http://ericsink.com/entries/multiple_sqlite_problem.html> and <https://www.sqlite.org/howtocorrupt.html>.__

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
NOTE: These samples will *not* work with altern