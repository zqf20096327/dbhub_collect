# docker-why

```bash
# change directory
cd src
# build compose files from scratch
docker-compose build --no-cache
# start compose
docker-compose up
```

Need to wait about 25-30 seconds for the SQL Server to boot and load test data.

Browse to http://localhost:57270  and click the Names link

## Adding development certificate for ASP.NET

```bash
# Remove and certs from the app if there
dotnet dev-certs https --clean

# Export certificate with a password and TRUST using the --trust flag
# to the path ${HOME}/.aspnet/https/<appname>.pfx -p <password> --trust
dotnet dev-certs https -ep ${HOME}/.aspnet/https/namesweb.pfx -p P@55w0rd --trust

# Add the password of the cert to the user secrets for the app
dotnet user-secrets set "Kestrel:Certificates:Development:Password" "P@55w0rd" --id 7A303942-47A6-491F-80AD-78057FA8B0CB
```

## Docker and docker-compose elements

* EXPOSE 443 in the Dockerfile (80 is EXPOSED by default)
* docker-compose map ports and environment variables

```docker
environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ASPNETCORE_URLS=https://+;http://+
      - ASPNETCORE_HTTPS_PORT=44349
    ports:
    # Replace the values on the left by the values on your launchSettings.json
      - "57270:80"
      - "44348:443"
    volumes:
      - ${HOME}/.microsoft/usersecrets/:/root/.microsoft/usersecrets
      - ${HOME}/.aspnet/https:/root/.aspnet/https/
```

## ASP.NET Core App launchsettings.json

````javascript
 "applicationUrl": "http://localhost:57270",
      "sslPort": 44348
    }
```