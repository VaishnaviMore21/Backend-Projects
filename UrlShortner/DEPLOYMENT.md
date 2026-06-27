# Easy Production Deploy (Automated Setup + Minimal Manual Steps)

This repo is prepared for a free-tier deployment with:

- Render (Spring Boot API container)
- Neon (PostgreSQL)
- Upstash (Redis)

## What is already automated in this repo

- `src/main/resources/application-prod.yml`
- `render.yaml`
- `.dockerignore`
- `scripts/deploy-render.ps1`

## 1) One command to push deployment config

```powershell
Set-Location "C:\Users\vaishmor\Desktop\BackendProjects\UrlShortner"
.\scripts\deploy-render.ps1
```

This script commits current changes (if any) and pushes to `origin/main`.

## 2) Create managed services (manual, 5 minutes)

### PostgreSQL (Neon)

Create a free Neon project and copy:

- host
- database
- username
- password

Build JDBC URL:

```text
jdbc:postgresql://<NEON_HOST>/<DB_NAME>?sslmode=require
```

### Redis (Upstash)

Create a free Upstash Redis database and copy:

- host
- port
- password

## 3) Create Render service

1. In Render, choose **New +** -> **Blueprint** (recommended)
2. Select this GitHub repo (Render reads `render.yaml`)
3. Render creates `urlshortner-api`

## 4) Add required Render environment variables

Add these in Render service settings:

- `SPRING_DATASOURCE_URL`
- `SPRING_DATASOURCE_USERNAME`
- `SPRING_DATASOURCE_PASSWORD`
- `SPRING_DATA_REDIS_HOST`
- `SPRING_DATA_REDIS_PORT`
- `SPRING_DATA_REDIS_PASSWORD`
- `SPRING_DATA_REDIS_SSL_ENABLED=true`
- `APP_BASE_URL=https://<your-render-service>.onrender.com`

Already set in `render.yaml`:

- `SPRING_PROFILES_ACTIVE=prod`
- `APP_CACHE_TTL_SECONDS=86400`

## 5) Verify deployment

Once deployed, test:

- `https://<service>.onrender.com/actuator/health`
- `https://<service>.onrender.com/`

Create short URL:

```bash
curl -X POST "https://<service>.onrender.com/shorten" \
  -H "Content-Type: application/json" \
  -d '{"fullUrl":"https://example.com/some/long/path"}'
```

## Notes

- Fully automatic cloud account creation/secrets setup is not possible from this local project alone.
- The repo is now preconfigured so deployment is mostly click-through + secret values.

