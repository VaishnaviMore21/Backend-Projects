# Project Details: Redis-Cached URL Shortener

## 1) Overview

This project is a production-style backend URL shortener built with:

- Java Spring Boot
- PostgreSQL (primary persistent storage)
- Redis (low-latency cache)

It supports shortening long URLs, redirecting via short codes, and health monitoring with Spring Actuator. A simple browser UI is included and served from the application root.

---

## 2) Core Features

- Shorten long URLs into compact short URLs
- Redirect short URL to original URL
- URL validation (only `http` / `https`)
- Redis-first lookup for low latency
- PostgreSQL fallback on cache miss
- Write-through cache population on create and on DB miss resolve
- Health endpoint via Actuator
- Consistent error response contract
- Dockerized full stack (API + PostgreSQL + Redis)
- Simple UI at `/`

---

## 3) High-Level Architecture

The project uses a layered architecture:

- **Controller layer**: REST API and redirect endpoints
- **Service layer**: URL business logic, validation, cache/database read flow
- **Repository layer**: JPA access and sequence ID allocation
- **Cache service**: Redis abstraction using `RedisTemplate<String, String>`
- **Utility layer**: Base62 encoder/decoder
- **Exception layer**: centralized global exception handling

### Request Flow (Create)

1. Validate input URL
2. Allocate numeric ID from PostgreSQL sequence
3. Encode ID to Base62 short code
4. Persist mapping to PostgreSQL
5. Store mapping in Redis
6. Return shortened URL

### Request Flow (Resolve)

1. Check Redis by `shortCode`
2. If cache hit: return immediately
3. If cache miss: query PostgreSQL by `shortCode`
4. Store found mapping in Redis
5. Return redirect response

---

## 4) Base62 Short Code Strategy

Alphabet used:

```text
0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
```

- Numeric ID from DB is encoded to Base62 to generate a compact URL-safe short code.
- This ensures deterministic and unique mapping based on sequence IDs.

Example:

- ID `1` -> short code `1`
- ID `62` -> short code `10`

Implementation file:

- `src/main/java/com/urlshortner/util/Base62Encoder.java`

---

## 5) Data Model and Schema

Primary table: `url_mapping`

```sql
CREATE TABLE IF NOT EXISTS url_mapping (
    id BIGSERIAL PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_code VARCHAR(20) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_url_mapping_short_code
    ON url_mapping (short_code);
```

Schema locations:

- `src/main/resources/schema.sql`
- `docker/postgres/init/01-schema.sql`

Entity:

- `src/main/java/com/urlshortner/entity/UrlMapping.java`

---

## 6) API Endpoints

### POST `/shorten`

Create short URL.

Request:

```json
{
  "fullUrl": "https://example.com/some/long/path"
}
```

Response (`201 Created`):

```json
{
  "shortUrl": "http://localhost:8080/abc123"
}
```

### GET `/{shortCode}`

Redirects to original URL.

- Returns `302 Found`
- Sets `Location` header with original URL
- Uses Redis-first, DB fallback strategy

### GET `/actuator/health`

Health status endpoint.

---

## 7) Error Handling

Global exception handling is centralized in:

- `src/main/java/com/urlshortner/exception/GlobalExceptionHandler.java`

Handled cases:

- Invalid URL -> `400 Bad Request`
- Validation errors -> `400 Bad Request`
- Short code not found -> `404 Not Found`
- Unexpected errors -> `500 Internal Server Error`

Error response shape:

```json
{
  "error": "message",
  "status": 400,
  "timestamp": "2026-06-28T12:00:00Z"
}
```

---

## 8) Redis Caching Details

Cache service:

- `src/main/java/com/urlshortner/service/RedisCacheService.java`

Design:

- Key: `shortCode`
- Value: `originalUrl`
- TTL controlled by `APP_CACHE_TTL_SECONDS` (default `86400`)

Caching points:

- On create: mapping written to Redis immediately
- On resolve miss: mapping loaded from DB and written back to Redis

Config files:

- `src/main/java/com/urlshortner/config/RedisConfig.java`
- `src/main/resources/application.yml`

---

## 9) UI

A simple static UI is served from:

- `src/main/resources/static/index.html`
- `src/main/resources/static/styles.css`
- `src/main/resources/static/app.js`

UI URL:

```text
http://localhost:8080/
```

Capabilities:

- Input long URL
- Call `POST /shorten`
- Show generated short URL
- Copy short URL to clipboard
- Open short/original URLs directly

---

## 10) Configuration

Main config file:

- `src/main/resources/application.yml`

Environment variables:

- `SPRING_DATASOURCE_URL`
- `SPRING_DATASOURCE_USERNAME`
- `SPRING_DATASOURCE_PASSWORD`
- `SPRING_DATA_REDIS_HOST`
- `SPRING_DATA_REDIS_PORT`
- `APP_BASE_URL`
- `APP_CACHE_TTL_SECONDS` (default `86400`)

---

## 11) Docker and Deployment

### Docker files

- `Dockerfile`
- `docker-compose.yml`

### Compose services

- `api` (Spring Boot application)
- `postgres` (PostgreSQL 16)
- `redis` (Redis 7 alpine)

### Start full stack

```powershell
Set-Location "C:\Users\vaishmor\Desktop\BackendProjects\UrlShortner"
docker compose up --build
```

### Stop stack

```powershell
Set-Location "C:\Users\vaishmor\Desktop\BackendProjects\UrlShortner"
docker compose down
```

---

## 12) Local Run (without full app container)

Start dependencies only:

```powershell
Set-Location "C:\Users\vaishmor\Desktop\BackendProjects\UrlShortner"
docker compose up postgres redis
```

Run Spring Boot locally:

```powershell
Set-Location "C:\Users\vaishmor\Desktop\BackendProjects\UrlShortner"
mvn spring-boot:run
```

---

## 13) Testing and Verification

Unit tests included:

- `src/test/java/com/urlshortner/util/Base62EncoderTest.java`
- `src/test/java/com/urlshortner/service/UrlShortenerServiceTest.java`

Run tests:

```powershell
Set-Location "C:\Users\vaishmor\Desktop\BackendProjects\UrlShortner"
mvn test
```

Manual smoke tests:

```powershell
Invoke-RestMethod -Uri "http://localhost:8080/actuator/health"
```

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8080/shorten" -ContentType "application/json" -Body '{"fullUrl":"https://example.com/some/long/path"}'
```

```powershell
Invoke-WebRequest -Uri "http://localhost:8080/1" -MaximumRedirection 0
```

---

## 14) Current Project Structure (important files)

```text
UrlShortner/
  pom.xml
  Dockerfile
  docker-compose.yml
  README.md
  projectdetails.md
  src/
    main/
      java/com/urlshortner/
        UrlShortnerApplication.java
        config/RedisConfig.java
        controller/UrlShortenerController.java
        dto/
        entity/UrlMapping.java
        exception/
        repository/
        service/
        util/Base62Encoder.java
      resources/
        application.yml
        schema.sql
        static/
          index.html
          styles.css
          app.js
    test/
      java/com/urlshortner/
        service/UrlShortenerServiceTest.java
        util/Base62EncoderTest.java
  docker/
    postgres/
      init/
        01-schema.sql
```

---

## 15) Notes and Troubleshooting

- If Docker image pulls fail due to transient registry/network issues, retry with:

```powershell
docker login
docker compose build --no-cache api
docker compose up
```

- If `/` UI does not open, verify app logs include:

```text
Adding welcome page: class path resource [static/index.html]
```

- If redirects fail, validate the short code exists and database/redis services are healthy.

---

## 16) Future Enhancements

Potential additions:

- URL click analytics
- Expiration policies per URL
- Custom aliases
- Rate limiting and abuse protection
- Integration tests using Testcontainers
- OpenAPI/Swagger documentation

