[![GitHub issues](https://img.shields.io/github/issues/john-pels/cbt-software.svg)](https://github.com/John-pels/cbt-software/issuess)
[![GitHub last commit](https://img.shields.io/github/last-commit/john-pels/cbt-software.svg)](https://github.com/John-pels/cbt-software/tree/master)
[![Analytics](https://ga-beacon.appspot.com/UA-83446952-1/github.com/john-pels/cbt-software/README.md)](https://github.com/john-pels/cbt-software/)

![Trisight](./images/tri_icon-02.png)

# cbt-software

CBT Software - This is a computer based test system for any type of institutions(Majorly Primary and Secondary schools) to take Examination. This is the newly introduced system rather than using a manual system which is paper pencil test.

Folder structure:

- `admin/` - An admin route to upload questions and answers to appropriate subject or course.
- `assets/` - fonts, images (png or svg).
- `bootstrap/` - CSS framework files
- `ckeditor/` - ckeditor plugin files
- `css/` - cascading stylesheet files
- `db/` - sql database file
- `dist/` - generated production folder
- `images/` - images such as png or svg
- `includes/` - abstraction files
- `onlineForm/` - form to upload questions and aswers
- `scss/` - CSS preprocessor files
- `uploads/` - uploaded images

## Getting started

1. Fork the repository, then clone it
2. Download and install WAMP or XAMPP for windows,
   i. AMPP for MacOS
   ii. LAMPP for linux
   You can download here https://www.apachefriends.org

3. After installation,start the server, Open your browser and visit https://localhost/phpmyadmin
4. create database and name it 'tri_exam'
5. import the database from the db folder.
6. Copy the whole folder and paste it into the htdocs folder in Xampp root folder.
7. Now open your browser and visit https://localhost/examination

# Notes

&mdash; The folder's name is very important as it is what you will reference in the browser. If you change the folder's name,
then the link would be https://localhost/foldername
&mdash; Please make sure you copy the whole folder and paste in the htdocs inside XAMPP folder.

## LICENSE

MIT
