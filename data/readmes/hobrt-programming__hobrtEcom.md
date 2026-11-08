# hobrtEcom
hobrt eCommerce script

## Requirements

- PHP 8.1 or newer with the `pdo_mysql`, `gd`, `intl`, `curl` and `mbstring` extensions
- MySQL 5.7+ or MariaDB 10.2+
- Apache with `mod_rewrite` (the `.htaccess` files also protect private files), or nginx with the rules from `nginx.conf.example`

## Install a new store

1. Create an empty database and a database user in your hosting panel.
2. Download the ZIP of the [latest release](https://github.com/hobrt-programming/hobrtEcom/releases/latest): it already contains `application/vendor`. From a git clone instead, run `composer install` inside the `application` folder.
3. Upload all files to your web root or to a sub folder.
4. Open `yourdomain.com/install/install.php` (any page of the store redirects there until it is installed).
5. Fix anything the requirements list shows in red. The folders `application/config`, `application/cache`, `application/logs`, `uploads` and `images` must be writable by PHP (755 is usually enough, never use 777).
6. Choose **New store**, fill in the database, store and admin account, then click install.

The installer writes `application/config/local.php` (database and store URL) and `application/config/secrets.php`. Keep them private and back them up. Once they exist the installer locks itself; you can delete the `install` folder for extra safety.

### Template editor and AI assistant (optional)

Admin > Themes > Template editor and its AI assistant save changes to the store theme files, so PHP needs write access to **`themes/front` only**. Leave everything else (`application`, `system`, `themes/enAdmin`) read-only. Theme `.php` files can't be opened by URL (`themes/.htaccess`, or the `themes` rule in `nginx.conf.example`), so a writable theme file is still only run by the store itself.

- **Shared hosting** (PHP runs as your hosting user): usually nothing to do.
- **Your own server** (PHP runs as `nginx`, `apache` or `www-data`): give that user write access to the folder, for example on Fedora/RHEL with SELinux:

  ```bash
  sudo setfacl -R -m u:nginx:rwX -m d:u:nginx:rwX themes/front
  sudo semanage fcontext -a -t httpd_sys_rw_content_t "$PWD/themes/front(/.*)?"
  sudo restorecon -Rv themes/front
  ```

If you don't use the editor, skip this: the store works with read-only themes.

### AI agents: MCP server (optional)

The store has an [MCP](https://modelcontextprotocol.io) server at `yourdomain.com/mcp`, so an AI agent such as Claude Code, Codex or Cursor can manage it from a simple request: add products (with images from a URL or a local file), write landing pages, follow and update orders, and manage categories, collections, coupons, pages and reviews.

1. Admin > Plugins > AI agents (MCP): create a key. Choose **read only** for an agent that only needs to look, **full access** for one that adds and changes things. The key is shown once.
2. Connect the agent with the command shown on that page, for example:

   ```bash
   claude mcp add --transport http hobrtecom https://yourdomain.com/mcp --header "Authorization: Bearer hbm_..."
   ```

3. Ask, for example: *"Add a product from ~/photos/bag.jpg: leather bag, 349 MAD, sizes S, M and L"* or *"Which orders are waiting for confirmation?"*

A full access key can do what an admin can (except settings, admins and HTML codes), so keep keys private and revoke the ones you no longer use on the same page. The agent sends the key in the `Authorization` header; the included `.htaccess` passes it to PHP. If your host still removes it, the agent can send it as `X-Hobrt-Key` instead.

### Ad tracking and Conversion API (optional)

Admin > Plugins > Tracking & Conversion API: Facebook and TikTok pixels, Google Tag Manager and GA4. Each pixel runs in the browser and, when you add its access token, is also sent from the server (Facebook Conversions API, TikTok Events API), with the same event id so it is counted once. Server events still arrive when an ad blocker or the browser blocks the pixel, and carry the customer's phone (hashed) for better matching.

- Events: ViewContent (product and landing pages), AddToCart, InitiateCheckout (cart page) and Purchase (every order, store and landing pages).
- Google: Tag Manager gets `view_item`, `add_to_cart`, `begin_checkout` and `purchase` in the `dataLayer` (GA4 ecommerce format). With a GA4 measurement id and Measurement Protocol API secret, every order is also sent to GA4 from the server; GA4 counts it once by its transaction id.
- To check the setup, fill in the test event codes and press *Save and send a test event*: the answers of Facebook, TikTok and GA4 are shown on the page. Empty the test codes afterwards.

### Hidden admin login (optional)

In Admin > Store Settings > Admin login address you can choose a secret address for the login page (for example `yourdomain.com/office-3f9a2c71`). Once set, the login form is only there: `user/admin_login` and every admin page answer "page not found" to anyone not logged in. After signing in, the admin works as usual with its normal `/admin/...` links. Bookmark the address.

**Lost it?** Open your database (phpMyAdmin) and run `DELETE FROM hb_meta WHERE k = 'admin_path';`. `/admin` works again right away.

### Errors and development mode

Live stores never show PHP errors to visitors; errors are written to `application/logs` instead. To see errors while developing, set the `CI_ENV` environment variable to `development`: `SetEnv CI_ENV development` in `.htaccess` (Apache) or `fastcgi_param CI_ENV development;` in the PHP location (nginx).

## Upgrade an existing store

**Back up your database and your `uploads`/`images` folders first.**

### From the 2019 or 2023 release

1. Upload the files of the new release over the old ones.
2. Open `yourdomain.com/install/install.php` and choose **Upgrade an existing store**.
3. Enter the database details of your store and your current admin username and password.

The upgrade keeps all your data: it adds the missing tables and columns, converts old orders, dates and reviews, creates the URL slugs for products and categories, and your old admin password keeps working.

After the upgrade:
- SMS notifications need your own Hbsms token and device id in **Admin > Settings**.
- Check the store URL in **Admin > Settings** and your theme.

### Future releases

**Admin > Update** installs the latest release in one click, without FTP or cPanel. The admin panel shows when a new version is out.

- It downloads the release ZIP from GitHub, checks it against the release checksum, writes the store's program files and then updates the database.
- It never deletes anything and never writes `uploads`, `images`, `reviews`, `logo`, `application/config/local.php`, `secrets.php` or the logs.
- Theme files you changed (template editor), `.htaccess` and `application/config` files you changed keep your changes when the new version doesn't change them. When it changes one of them too, the update stops first and lists them with a warning: they stay as they are unless you tick them, and a ticked file gets the new version and loses your changes (your version stays in the backup). A store installed before this feature can't tell which files you changed yet, so on its first update every such file that differs is listed this way.
- Every replaced file is saved first in `application/backups` (the last 3 updates). If writing fails halfway the old files are put back at once, and **Restore** puts back any backup later.
- PHP needs write access to the store folder (usual on shared hosting). If it doesn't have it, nothing is changed and the page lists the files it can't write.

You can still update by hand: upload the new files over the old ones (never delete the `uploads` and `images` folders), then click **Update now** on the database banner.

## Development

Copy your settings into `application/config/local.php` (see the installer output for the format) or use the `HBECOM_DB_HOST`, `HBECOM_DB_PORT`, `HBECOM_DB_NAME`, `HBECOM_DB_USER`, `HBECOM_DB_PASS` and `HBECOM_BASE_URL` environment variables. Set `CI_ENV=development` to display errors.
