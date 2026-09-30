# eris_polardb


Installation steps is given below:

1. Download Xampp Server from Internet.
2. Install Xampp Server.
3. Go to phpmyadmin folder and find config.inc.php file and insert these lines of code which is given below:

              $cfg['Servers'][$i]['auth_type'] = 'config';
              $cfg['Servers'][$i]['user'] = 'bhasudb1';
              $cfg['Servers'][$i]['password'] = 'Bhasu@123';
              $cfg['Servers'][$i]['extension'] = 'mysqli';
              $cfg['Lang'] = '';
              /* Server parameters */
              /* Bind to the localhost ipv4 address and tcp */
              $cfg['Servers'][$i]['host'] = 'mysample.mysql.polardb.japan.rds.aliyuncs.com:3306';
              $cfg['Servers'][$i]['connect_type'] = 'tcp';
              $cfg['Servers'][$i]['compress'] = false;
              $cfg['Servers'][$i]['AllowNoPassword'] = true;
              
4. After adding these lines save the file.
5. Download the project file name eris.zip.
6. Copy the Eris Folder to htdocs folder.
7. Open Xampp Control Panel and start all the servers.
8. Then go to your browser type localhost/eris for homepage.
9. For admin panel, type localhost/eris/admin/index.php
10. Any issues, watch this video (Direct Preview is available)-> https://mega.nz/file/88EGCDRb#hyax79m45ITOenzeIihRkxdCxKglfGdOtu1Tkp7qGpw
