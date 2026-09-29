<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title></title>
</head>
<body>
ADO.NET SQLite Data Provider<br />
Version 1.0.95.0 - January XX, 2015 <font color="red">(release scheduled)</font><br />
Using <a href="http://www.sqlite.org/releaselog/3_8_7_4.html">SQLite 3.8.7.4</a><br />
Originally written by Robert Simpson<br />
Released to the public domain, use at your own risk!<br />
Official provider website:&nbsp;<a href="http://system.data.sqlite.org/">http://system.data.sqlite.org/</a><br />
Legacy versions:&nbsp;<a href="http://sqlite.phxsoftware.com/">http://sqlite.phxsoftware.com/</a><br />
<br />
The current development version can be downloaded from <a href="http://system.data.sqlite.org/index.html/timeline?y=ci">
http://system.data.sqlite.org/index.html/timeline?y=ci</a>
<br />
<br />

<h2><b>Features</b></h2>

<ul>
  <li>
    Written from scratch on Visual Studio 2008 specifically for ADO.NET,
    implementing all the base classes and features recently introduced in the
    framework, including automatic transaction enlistment.
  </li>

  <li>
    Supports the Full and Compact .NET Framework, and native C/C++ development.
    100% binary compatible with the original sqlite3.dll.
  </li>

  <li>
    Full support for Mono via a &quot;managed only&quot; provider that runs
    against the official SQLite 3.6.1 or higher library.
  </li>

  <li>Full Entity Framework support (ADO.NET 3.5 SP1).</li>

  <li>
    On the Compact Framework, it is faster than SQL Server Mobile.  SQLite's
    installed size is a fraction of SQL Mobile's.  It uses less memory at
    runtime, runs queries faster, and has a smaller database file size as well.
  </li>

  <li>
    Encrypted database support.  Encrypted databases are fully encrypted and
    support both binary and cleartext password types.
  </li>

  <li>
    Visual Studio design-time Support, works with all versions of Visual Studio
    2005/2008/2010/2012.  You can add a SQLite database to the Servers list,
    design queries with the Query Designer, drag-and-drop tables onto a Typed
    DataSet, etc.
    <br />
    <font color="red">
      Due to Visual Studio licensing restrictions, the Express Editions can no
      longer be supported.
    </font>
  </li>

  <li>
    Full SQLite schema editing inside Visual Studio.  You can create/edit tables,
    views, triggers, indexes, check constraints and foreign keys.
  </li>

  <li>
    Single file redistributable (except on Compact Framework).  The core SQLite
    native code and the ADO.NET managed wrapper are combined into one mixed-mode
    assembly.
  </li>

  <li>
    Binaries included for x86, x64, Itanium, and ARM processors.
    <br />
    <font color="red">
      Itanium processor support not currently included.
    </font>
  </li>

  <li>DbProviderFactory support.</li>

  <li>
    Full support for ATTACH'ed databases.  Exposed as <i>Catalogs</i> in the
    schema.  When cloning a connection, all attached databases are automatically
    re-attached to the new connection.
  </li>

  <li>
    DbConnection.GetSchema(...) support includes <i>ReservedWords</i>,
    <i>MetaDataCollections</i>, <i>DataSourceInformation</i>, <i>DataTypes</i>,
    <i>Columns</i>, <i>Tables</i>, <i>Views</i>, <i>ViewColumns</i>,
    <i>Catalogs</i>, <i>Indexes</i>, <i>IndexColumns</i>, <i>ForeignKeys</i> and
    <i>Triggers</i>.
  </li>

  <li>
    Enhanced DbDataReader.GetSchemaTable() functionality returns catalog,
    namespace and detailed schema information even for complex queries.
  </li>

  <li>Named and unnamed parameters.</li>

  <li>
    Full UTF-8 and UTF-16 support, each with optimized pipelines into the native
    database core.
  </li>

  <li>
    Multiple simultaneous DataReaders (one DataReader per Command however).
  </li>

  <li>
    Full support for user-defined scalar and aggregate functio

[...截断...]

ns, encapsulated
    into an easy-to-use base class in which only a couple of overrides are
    necessary to implement new SQL functions.
  </li>

  <li>
    Full support for user-defined collating sequences, every bit as simple to
    implement as user-defined functions and uses the same base class.
  </li>

  <li>
    Full source for the entire engine and wrapper.  No copyrights.  Public
    Domain.  100% free for commercial and non-commercial use.
  </li>
</ul>

<h2><strong>Design-Time Support</strong></h2>
<p>
Download and run one of the setup packages and then select the
&quot;<b>Install the designer components for Visual Studio 20XX.</b>&quot;
option when prompted.
</p>
<h2>
<strong>DbFactory Support (Desktop Framework)</strong></h2>
In order to use the SQLiteFactory and have the SQLite data provider enumerated in
the DbProviderFactories methods, you must add the following segment into your application's
app.config file:<br />
<pre>
&lt;configuration&gt;
    &lt;system.data&gt;
        &lt;DbProviderFactories&gt;
            &lt;remove invariant="System.Data.SQLite" /&gt;
            &lt;add name="SQLite Data Provider" invariant="System.Data.SQLite" description=".NET Framework Data Provider for SQLite"
                 type="System.Data.SQLite.SQLiteFactory, System.Data.SQLite, Version=1.0.95.0, Culture=neutral, PublicKeyToken=db937bc2d44ff139" /&gt;
        &lt;/DbProviderFactories&gt;
    &lt;/system.data&gt;
&lt;/configuration&gt;
</pre>
<p>
See the help documentation for further details on implementing both version-specific
(GAC enabled) and version independent DBProviderFactories support.
</p>

<h2>Compiling for the .NET Compact Framework</h2>

<p>
Just change the target platform from Win32 to Compact Framework and recompile.&nbsp;
<strong>The Compact Framework has no support for enumerating attributes in an assembly,
therefore all user-defined collating sequences and functions must be explicitly
registered.</strong>&nbsp; See the <strong>testce</strong> sample application for
an example of how to explicitly register user-defined collating sequences and functions.</p>

<h2><b><a name="redist"></a>Distributing or Deploying System.Data.SQLite</b></h2>

<p>
On the desktop, when using the statically linked mixed-mode assembly, only the
<strong>System.Data.SQLite.dll</strong> file needs to be distributed with your
application(s).  This dynamic link library contains both the managed provider
and the SQLite native library.  For other build configurations, including those
for the .NET Compact Framework, you will need to distribute both the managed
provider <strong>System.Data.SQLite.dll</strong>, as well as the associated
native library <strong>SQLite.Interop.dll</strong> (or
<strong>SQLite.Interop.XXX.dll</strong> for the .NET Compact Framework).  For
the .NET Compact Framework edition, this is a breaking change as of 1.0.59.0.
The recent versions of the .NET Compact Framework do not appear to properly
support mixed-mode assemblies.  All builds of System.Data.SQLite, except those
explicitly marked as &quot;static&quot; in their package name, will also require
the associated <a href="https://support.microsoft.com/kb/2019667">Microsoft
Visual C++ Runtime Library</a> to be installed on the target machine.  For
further details on distributing and/or deploying System.Data.SQLite, please
refer to the
<a href="http://system.data.sqlite.org/index.html/doc/trunk/www/downloads.wiki">System.Data.SQLite Downloads</a>
web page.
</p>

<h2><b>Development Notes Regarding the SQLite Native Library Source Code</b></h2>

<p>
The included SQLite native library is compiled directly from the official source
code releases available from the <a href="http://www.sqlite.org/">sqlite.org</a>
website.
</p>

<p>
In addition, there are several relatively small extensions included within the
System.Data.SQLite &quot;interop assembly&quot; and some of these extensions ar