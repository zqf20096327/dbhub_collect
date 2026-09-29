# URL Shortener

A simple, high-performance URL shortening service built with .NET 10.

## Features

- **URL Shortening**: Generate short, unique codes for long URLs.
- **Redirection**: Instant redirection from short codes to original URLs.
- **Analytics**: Track hit counts for each shortened link.
- **Rate Limiting**: Built-in protection for both API and public endpoints.
- **Security**: API key protection for management endpoints.
- **Storage**: Lightweight persistence using SQLite.

## Technology Stack

- **Framework**: .NET 10
- **Database**: SQLite with Entity Framework Core
- **Hosting**: Azure Web App
- **DNS**: Azure DNS

## API Reference

### Public Endpoints

#### Resolve Short Link
`GET /{code}`
Redirects to the original long URL.

#### Ping
`GET /ping`
Check service health.

### Management Endpoints (Requires API Key)

All management endpoints require the `X-Api-Key` header.

#### Create Short Link
`POST /api/links`
- **Request Body**: `{"url": "https://example.com"}`
- **Response**: `{"code": "...", "shortUrl": "...", "longUrl": "..."}`

#### Get Link Details
`GET /api/links/{code}`
- **Response**: `{"code": "...", "shortUrl": "...", "longUrl": "...", "createdUtc": "...", "hitCount": 0}`

## Configuration

### Security
In production, ensure the `ApiKeys:Default` configuration value is set. Requests to `/api/*` endpoints must include this key in the `X-Api-Key` header.

### Database
- **Development**: The SQLite database is stored in the `URLShortener.API/Data` folder.
- **Production (Azure)**: The database is stored at `/home/data/shortener.db` to ensure persistence across Web App restarts (mapped to persistent storage).

## Running with Docker / Podman

The application can be containerized using the provided `Dockerfile`. This works on Windows, Linux, and macOS using either Docker or Podman.

1. **Build the image**:
   ```bash
   docker build -t url-shortener .
   ```
   *(If using Podman, replace `docker` with `podman`)*

2. **Run the container**:
   ```bash
   docker run -d -p 5051:5051 --name url-shortener-app url-shortener
   ```
   The application will be available at `http://localhost:5051`. Test is by going to `http://localhost:5051/ping`.

## Local Development

1. Clone the repository.
2. Open `URLShortener.slnx` in your IDE.
3. Run the `URLShortener.API` project.
4. Use the provided `URLShortener.http` file to test endpoints.

## Deployment to Azure

The application is designed to run as an Azure Web App.

1. **Persistent Storage**: Ensure the Web App has a mount or configuration that persists `/home/data` if you want to keep the SQLite database across deployments.
2. **Environment Variables**: Set `ApiKeys__Default` in the Azure App Service Configuration.
3. **Custom Domain**: Use Azure DNS to map your custom short domain to the Web App.
