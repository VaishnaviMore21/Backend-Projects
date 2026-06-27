# Real-Time Chat Backend (Spring Boot)

Backend scaffold for a real-time chat application with REST + WebSocket/STOMP and a built-in static UI.

## Stack

- Java 17
- Spring Boot 3 (Web, Security, Validation, WebSocket, JPA)
- PostgreSQL
- Redis
- Flyway
- JWT
- Docker Compose

## Quick Start

1. Copy environment template:

```powershell
Copy-Item .env.example .env
```

2. Start infra services:

```powershell
docker compose --env-file .env up -d postgres redis
```

3. Run application:

```powershell
mvn spring-boot:run
```

Application starts on `http://localhost:8080`.

UI starts on `http://localhost:8080/`.

## Build & Test

```powershell
mvn clean test
mvn clean package
```

## Key Endpoints

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/users/by-username/{username}`
- `POST /api/rooms`
- `GET /api/rooms`
- `GET /api/rooms/{roomId}/messages`
- `POST /api/rooms/{roomId}/messages`
- WebSocket endpoint: `/ws`
- STOMP app destination: `/app/chat.send/{roomId}`
- STOMP topic: `/topic/rooms/{roomId}`

## UI Features

- register and login
- lookup senderId by username
- create and list rooms
- send and read messages
- connect to room topics over WebSocket

## Notes

- JWT generation is implemented, but a full JWT authentication filter is intentionally left as a next step.
- `SecurityConfig` currently allows the API, WebSocket endpoint, health endpoint, and static UI assets publicly for development.
