# dmlaravel
dmlaravel is a DM Database Driver package for Laravel. dmlaravel is an extension of Illuminate/Database that uses dmpdo extension to communicate with DM. Thanks to @yajra.

# Documentations
You will find user-friendly and updated documentation here: [laravel-Database](https://laravel.com/docs/master/database)  
Add dmphp to the php:[DMPHP](https://eco.dameng.com/document/dm/zh-cn/pm/php-rogramming-guide)

## Laravel Version Compatibility

 Laravel  | Package
:---------|:----------
 11.x     | 11.x
 master   | master

## Quick Installation

```bash
composer require dmmars/dmlaravel:^11
```

## Configuration (OPTIONAL)

Finally you can optionally publish a configuration file by running the following Artisan command.
If config file is not publish, the package will automatically use what is declared on your `.env` file database configuration.

```bash
php artisan vendor:publish --tag=dm
```

This will copy the configuration file to `config/dm.php`.

> Note: For [Laravel Lumen configuration](http://lumen.laravel.com/docs/configuration#configuration-files), make sure you have a `config/database.php` file on your project and append the configuration below:

```php
'dm' => [
    'driver'         => 'dm',
    'host'           => env('DB_HOST', 'localhost'),
    'port'           => env('DB_PORT', '5236'),
    'database'       => env('DB_DATABASE', ''),
    'schema'         => env('DB_SCHEMA', ''),
    'username'       => env('DB_USERNAME', ''),
    'password'       => env('DB_PASSWORD', ''),
    'charset'        => env('DB_CHARSET', 'UTF8'),
    'prefix'         => env('DB_PREFIX', ''),
],
```

> Then, you can set connection data in your `.env` files:

```ini
DB_CONNECTION=dm
DB_HOST=localhost
DB_PORT=5236
DB_SCHEMA=SYSDBA
DB_USERNAME=SYSDBA
DB_PASSWORD=SYSDBA
```

Then run your laravel installation...

## License

The MIT License (MIT). Please see [License File](https://github.com/dmmars/dmlaravel/blob/11.x/LICENSE) for more information.
