# opengauss-mate

#### set administrator user's password by env `PASSWORD`
#### set remote access user by `USER_NAME`,`USER_PASSWORD` 

#### example:
```shell
docker run -dit --privileged -p 5432:5432 --name opengauss -e PASSWORD=Test@123 -e USER_NAME=test -e USER_PASSWORD=Test@123 ttbb/opengauss:mate  
```
