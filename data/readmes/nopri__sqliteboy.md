
::

    SQLiteBoy
    Simple web-based management tool for SQLite database
    (with form, report, website, and many other features)
    (c) Noprianto <nopri.anto@icloud.com>
    2012-2019
    License: GPL
    Version: 1.83

    SQLiteBoy is an independent product, developed separately from the
    SQLite core library, which is maintained by SQLite.org.
    Neither noprianto.com nor SQLite.org take any responsibility for the
    work of the other.




.. contents::



What Is SQLiteBoy
========================================================================

- Easy to use, python and web.py based, simple web-based management tool 
  for SQLite database with user-defined functions and many extended features 
  (Free/open source)

- User-defined functions: number to words (multi language), number format,
  table lookup, hash, base64, random, additional date/time, additional
  string, regular expression, utility

- If Extended feature is enabled:

  Multi user, simple (yet flexible) form (data entry) and reporting can
  be created by admin (simple JSON syntax), and can be run by
  admin/user (configurable). Very simple subform is also supported.

  Form field supports predefined values (options) from SQL Query or
  Python list. Also, default value can be result of function call,
  static value or SQL Query. Constraint is also supported, to check before
  save, to prevent saving invalid value (it's possible to call
  function before comparison). Onsave event is also supported, to
  execute SQL Query (and use the result) just before the data is saved.

  Reporting wizard also supports form field predefined values, default
  value and constraint (checking before reporting query is executed).
  Supported report format: PDF, HTML, HTML (printer friendly) and CSV.

  Form and Report support python handler, which will be automatically called, if
  provided. Python handler eases the integration with external system
  (for example: ERP system). Python handler also could be useful in,
  for example, complex database operation, reading from/writing to
  external devices, etc.

  User accounts, Notes, Files (with file sharing support), Page (home page),
  calculator, configurable hosts allowed, database backup, system configuration,
  Scripts, profile (with user-defined profile support)
  and others are available as extended features

  SQLiteBoy script (simple JSON syntax, single file) can be used to automate
  the creation of tables (including addition of columns, for existing table),
  forms, reports or user-defined profiles
  
  It is also possible to use SQLiteBoy to serve a website with custom URLs.
  URL can be handled by a python function, redirect, Files, template, or HTML.
  POST method is also supported and can be handled by python function.


Links
========================================================================

- screenshot, probably not up-to-date:
  https://github.com/nopri/sqliteboy/wiki

- Free Book: Form dan Report sederhana dengan SQLiteBoy
  (Bahasa Indonesia, available as PDF/ODT, 250+ pages, revision 2):
  https://github.com/nopri/publication/raw/master/form-dan-report-sederhana-dengan-sqliteboy.pdf

- Tutorial: simple medical record:
  https://github.com/nopri/sqliteboy/wiki/Tutorial-simple-medical-record

- Tutorial: install sqliteboy on ACRyan Playon!HD Mini2 ACRPV73800:
  https://github.com/nopri/sqliteboy/wiki/Tutorial-install-sqliteboy-on-ACRyan-Playon!HD-Mini2-ACRPV73800

- Tutorial: Using sqliteboy udf in python handler:
  https://github.com/nopri/sqliteboy/wiki/Tutorial-using-sqliteboy-udf-in-python-handler

- Tutorial: Create a new partner in OpenERP:
  https://github.com/nopri/sqliteboy/wiki/Tutorial-create-a-new-partner-in-openerp

- Tutorial: Search partners in OpenERP:
  https://github.com/nopri/sqliteboy/wiki/Tutorial-search-partners-in-openerp

- Tutorial: Hyperlink and Javascript in label:
  https://github.com/nopri/sqliteboy/wiki/Tutorial-hyperlink-and-javascript-in-label

- More: https://git

[...截断...]

hub.com/nopri/sqliteboy/wiki/_pages


Development Notes
========================================================================

- Standalone version is no longer provided, but codes for this
  are still in the source code

- Version 1.51 was released as a bug fix (reported in issue #1). In this
  commit, many lines (both in this file and the source code) had been
  added/deleted (due to text reformatting). Please, let me know if
  something was accidentally added or deleted.

- As of v1.64, index URL was changed to /index because / is used for 
  public home page (new in v1.64, please read WEBSITE AND CUSTOM URL REFERENCE)  


Features
========================================================================

- Works with single SQLite database per instance

- Single python file

- Configurable port (default 11738 because it looks like sqliteboy).
  As of v1.75, it is possible to run SQLiteBoy as WSGI application,
  please read HOW TO RUN. 

- SSL Support

- Basic/Extended Feature

  - Basic: Database management + User-defined function

  - Extended: Form, Report, User/Login, etc

    - Completely optional

    - Can be enabled in menu

    - If enabled, one table::

        _sqliteboy_

      will be created. You can delete this table
      and extended feature will be disabled

- Form Support (Extended feature, new in v0.12)

  - Simple data entry

  - Simple syntax (JSON)

  - Please read FORM CODE REFERENCE section (below)

  - Readonly field

  - Required field

  - Predefined values (field options) from SQL Query
    or Python list

  - Default value: function call or static value or SQL Query

  - Constraint: check before save,
    prevent saving invalid value
    (possible to call function before comparison)

  - Simple security setting

  - As of v0.21, onsave event is also supported, to execute SQL Query
    (and use the result) just before the data is saved. The SQL Query
    can be very complex and involves nested function calls.

  - As of v0.26, very simple subform is also supported. Subform can be
    used in one to many relationship. However, field in subform is
    limited, compared to form.

  - As of v0.27, custom result message (based on SQL query result),
    is also supported.

  - As of v0.27, optional, additional SQL query statement(s) can be
    provided, and each of them will be executed in order, if you need
    to perform additional task(s), after the form data is saved (for
    example, write to another table). Previously, one might use report
    if need to write to several tables. Last insert rowid value is
    provided.

  - As of v0.75, insert into table can be disabled by setting insert key
    to zero/negative value. This is useful if you need to update/delete data in
    table(s), using additional SQL query statement(s). By default,
    form/subform save will insert new row(s) into table(s).

  - As of v0.98, form supports python handler, which will be automatically
    called, if provided. Python handler eases the integration with external
    system (for example: ERP system). Please read PYTHON HANDLER REFERENCE
    section.

  - As of v1.33, optional, (run before) additional SQL query statement(s)
    can be provided.

  - As of v1.72, links can be added to form

  - As of v1.73, form supports extended result message. This extends 
    custom result message introduced in v0.27. Using extended result, 
    it is possible to perform operations on form fields, and use the result.
    Like custom result message, it is based on SQL query result.
    But unlike custom result message, the result is not limited to integer
    (can be string or another types; probably returned from function call). 

- Report Support (Extended feature, new in v0.16)

  - Simple reporting (and data entry)

  - Simple syntax (JSON)

  - Please read REPORT CODE REFERENCE section (below)

  - Readonly field

  - Predefined values (field options) from SQL Query
    or Python list

  - Default value: function call or st