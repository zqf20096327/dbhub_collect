tidbit
======

Bookmarking service running on node.js/PostgreSQL

### SETUP
1. Create *tidbit* database
2. Load *etc/pg.sql*
3. Modify PostgreSQL credentials in *etc/config.js*
4. Add your hostname to *bookmarklet/source.js* 
5. Start *app.js*
6. Add *bookmarklet/source.js* to your browser nav
7. Enjoy

### TODO
* user authentication/multiuser support with passport
* display pages per user
* tag mining functions
* abstract db functions/add support for other databases
