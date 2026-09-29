# tidbit-deleteoldfolders
Deletes folders (named) older than n days ago from target directory

## DISCLAIMER
If you delete anything that you shouldn't using this tool - I am not to be held responsible

## Who this is for
You back up your cctv footage via FTP to a remote server. The 

## Please note
Folders are checked by NAME not by mtime, ctime or atime. This means that the name of the folder needs to = the date of the recordings within.

## Prerequisites
* Python 3
* A file structure similar to this (the important part is the existence of a folder, whose subfolders are all in ISO date format - which would be 192.168.1.1 in this case)

```
/home/ftpuser/cctv
└── files
    └── 192.168.1.1
        ├── 2020-06-08
        │   ├── NVR_ch9_main_20200608000000_20200608010000.dav
        │   ├── NVR_ch9_main_20200608010000_20200608020000.dav
        │   ├── NVR_ch9_main_20200608020000_20200608030000.dav
        │   └── NVR_ch9_main_20200608030000_20200608040000.dav
        |
        ├── 2020-06-09
        │   ├── NVR_ch9_main_20200609000000_20200609010000.dav
        │   ├── NVR_ch9_main_20200609010000_20200609020000.dav
        │   └── ....dav
        │
        └── 2020-06-10
            ├── NVR_ch9_main_20200610000000_20200610010000.dav
            ├── NVR_ch9_main_20200610010000_20200610020000.dav
            └── ....dav
```            

# INSTALLATION
1. CD to your directory above your ftp directory (the below assumes that the ftp directory is somewhere in home folder)

   `cd ~`
  
2. Clone repo

   `git clone https://github.com/mthan160/tidbit-deleteoldfolders`
   
3. Run Python script. Takes two arguments - the first is how many days you wish to keep (including today). The second is the directory to scan. Using the directory structure above and wanting to keep 3 days for example:

   `python3 ./tidbit-deleteoldfolders/deleteoldfolders.py 3 ./cctv/files/192.168.1.1/`
 
4. (Optionally) install via crontab
30 12 * * * python3 <location of .py file> <days to keep> <location of files>cctv/files/192.168.1.108 >> <normal logs> 2>> <error logs>

