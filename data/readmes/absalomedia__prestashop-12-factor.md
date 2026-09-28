# Twelve-Factor Prestashop

Prestashop, the [Twelve-Factor](http://12factor.net/) way: fully managed using Composer and configured using environment variables. This has been heavily inspired by [Wordpress 12 Factor](https://github.com/dzuelke/wordpress-12factor)

[![Code Climate](https://codeclimate.com/github/absalomedia/prestashop-12-factor/badges/gpa.svg)](https://codeclimate.com/github/absalomedia/prestashop-12-factor) [![StyleCI](https://styleci.io/repos/54073612/shield)](https://styleci.io/repos/54073612) [![Codacy Badge](https://api.codacy.com/project/badge/grade/fad89d57d8474c579c8159ed8ea503b3)](https://www.codacy.com/app/media/prestashop-12-factor) ![Prestashop 1.7.1](https://img.shields.io/badge/Prestashop-1.7.1-yellow.svg) [![Patreon](https://img.shields.io/badge/patreon-donate-green.svg)](https://www.patreon.com/bePatron?u=14641360)




## General Concepts and Considerations

The Prestashop installation is fully contained in a `shop1` subfolder upon Heroku deployment. A `settings.inc.php` resides in the root of the project, and uses several different environment variables to control behavior.

The configuration file is kept as generic as possible; on Heroku, add-ons [JawsDB](https://elements.heroku.com/addons/jawsdb) (for MySQL) and [SendGrid](https://elements.heroku.com/addons/sendgrid) (for E-Mails) are used.

The assumption is that this installation runs behind a load balancer whose `X-Forwarded-Proto` header value can be trusted; it is used to determine whether the request protocol is HTTPS or not.

## Quick Deploy

If you have a [Heroku](http://heroku.com) account, you may simply use the following button to deploy this application:

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

After the deploy, in [Heroku's Dashboard](https://dasboard.heroku.com) under "Settings" for your deployed application, **remove the `PRESTASHOP_ADMIN_*` environment variables**.

## Manual Deploy

### Clone

Clone this repo:

```
$ git clone https://github.com/absalomedia/prestashop-12-factor
$ cd prestashop-12-factor
```

If you like, you can locally install dependencies with [Composer](https://getcomposer.org):

```
$ composer install
```

### Create Application and Add-Ons

Create a new app and add add-ons for MySQL and E-Mail:

```
$ heroku create
$ heroku addons:create jawsdb
$ heroku addons:create sendgrid
```

### Deploy

```
$ git push heroku master
```

### Finalize Installation

This will create tables and set up an admin user:

```
$ heroku run 'composer prestashop-db-core --name='Prestashop on Heroku' --domain=example.herokuapp.com --db_server=localhost --db_name=prestashop --db_user=admin --db_password=admin --email=admin@example.com '
```

### Visit ecommerce store

Navigate to the application's URL, or open your browser the lazy way:

```
$ heroku open
```

## Updating Prestashop and Plugins

To update all dependencies:

```
$ composer update
```


## Environment Variables

`settings.inc.php` will use the following environment variables (if multiple are listed, in order of precedence):

### Database Connection

`DATABASE_URL` or `JAWSDB_URL` or `CLEARDB_DATABASE_URL` (format `mysql://user:pass@host:port/dbname`) for database connections.

### SendGrid

`SENDGRID_USERNAME` and `SENDGRID_PASSWORD` for SendGrid credentials.
