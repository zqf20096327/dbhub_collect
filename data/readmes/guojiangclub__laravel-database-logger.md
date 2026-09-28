# Laravel Database Logger

A simple database logger for Laravel application, support Guard,Auth to multiple file record.

[![Build Status](https://travis-ci.org/ibrandcc/laravel-database-logger.svg?branch=master)](https://travis-ci.org/ibrandcc/laravel-database-logger)
[![Build Status](https://scrutinizer-ci.com/g/ibrandcc/laravel-database-logger/badges/build.png?b=master)](https://scrutinizer-ci.com/g/ibrandcc/laravel-database-logger/build-status/master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/ibrandcc/laravel-database-logger/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ibrandcc/laravel-database-logger/?branch=master)
[![Latest Stable Version](https://poser.pugx.org/ibrand/laravel-database-logger/v/stable)](https://packagist.org/packages/ibrand/laravel-database-logger)
[![Latest Unstable Version](https://poser.pugx.org/ibrand/laravel-database-logger/v/unstable)](https://packagist.org/packages/ibrand/laravel-database-logger)
[![License](https://poser.pugx.org/ibrand/laravel-database-logger/license)](https://packagist.org/packages/ibrand/laravel-database-logger)

- [Chinese Documentation](./README.cn.md)

## Feature

1. Log files support anonymous or guard types.
2. Record auth uesrs.
3. Record request url
4. Support record specifying SQL statement(SELECT,INSET INTO,UPDATE,DELETE,ALTER TABLE etc.)
5. Record slow logs separately.

## Installation

```
composer require ibrand/laravel-database-logger:~1.0 -vvv
```

**Below Laravel5.5 version**

In `config/app.php`  'providers' region add 

```
iBrand\DatabaseLogger\ServiceProvider::class
```

Publish config file.

```
php artisan vendor:publish --provider="iBrand\DatabaseLogger\ServiceProvider" 
```

## Usage

### Enable in .env or config file.

Set `log_queries=>true` in `config/ibrand/dblogger.php` file. or set  `DB_LOG_QUERIES = true` in `.env` file.

### use `databaselogger` middleware 

```
Route::get('test', 'Controller@index')->middleware('databaselogger');
```
For more middleware users see the document.

[laravel-routing](https://laravel.com/docs/5.5/routing#route-group-middleware)

## Preview

![snapshot_1515552729718.png](https://note.youdao.com/yws/public/resource/59a59be278b1e0604684ed422875099c/xmlnote/E8B042EEF01446589326A7A4FF016C65/9459)
![snapshot_1515552729719.png](https://note.youdao.com/yws/public/resource/59a59be278b1e0604684ed422875099c/xmlnote/46ABB7598DAB429BBB4C2A722298B0FC/9462)
![snapshot_1515552729720.png](https://note.youdao.com/yws/public/resource/59a59be278b1e0604684ed422875099c/xmlnote/3F4BA3E7B2B4481BA8E5AA0AA702DDF6/9465)

## Contributing

If you find any bug or problem please raise the [issue here](https://github.com/ibrandcc/laravel-database-logger/issues).
