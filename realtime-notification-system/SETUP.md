# Setup and Installation Guide

## Prerequisites

- **Java 17+** - Download from [Oracle](https://www.oracle.com/java/technologies/downloads/#java17) or use OpenJDK
- **Maven 3.9+** - Download from [Maven](https://maven.apache.org/)
- **Docker & Docker Compose** - Download from [Docker](https://www.docker.com/products/docker-desktop)
- **Git** - Download from [Git](https://git-scm.com/)
- **Postman** (optional) - For API testing

## Installation Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd realtime-notification-system
```

### 2. Verify Prerequisites
```bash
# Check Java version
java -version  # Should be 17 or higher

# Check Maven version
mvn -version  # Should be 3.9 or higher

# Check Docker
docker --version
docker-compose --version
```

### 3. Build the Project
```bash
# Option 1: Using Maven
mvn clean install

# Option 2: Using build script
chmod +x build.sh
./build.sh
```

### 4. Start Services with Docker Compose
```bash
# Start all services
docker-compose up -d

# Or use the startup script
chmod +x start.sh
./start.sh
```

### 5. Verify Services are Running
```bash
# Check service status
docker-compose ps

# Check logs
docker-compose logs -f
```

### 6. Test the Application
```bash
# Health check
curl http://localhost:8080/api/notifications/health

# Should return: Notification service is running
```

## Service URLs

| Service | URL |
|---------|-----|
| Notification API | http://localhost:8080/api |
| Kafka UI | http://localhost:8888 |
| PostgreSQL | localhost:5432 |
| Kafka Bootstrap | localhost:9092 |

## Manual Setup (Without Docker)

### 1. Install PostgreSQL
- Download and install from [PostgreSQL](https://www.postgresql.org/download/)
- Create database: `notification_db`
- Create user: `postgres` with password `postgres`

### 2. Install Kafka
- Download from [Apache Kafka](https://kafka.apache.org/downloads)
- Extract and configure

### 3. Configure Application
Edit `src/main/resources/application.yml`:
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/notification_db
    username: postgres
    password: postgres
  kafka:
    bootstrap-servers: localhost:9092
```

### 4. Run Application
```bash
# Using Maven
mvn spring-boot:run

# Or run the JAR
java -jar target/realtime-notification-system-1.0.0.jar
```

## Development Setup

### IDE Setup (IntelliJ IDEA)
1. Open project: File → Open → Select project folder
2. Maven will auto-detect pom.xml
3. Right-click project → Maven → Reload Project
4. Run application: Right-click `NotificationServiceApplication` → Run

### IDE Setup (VS Code)
1. Install Extensions:
   - Spring Boot Extension Pack
   - Maven for Java
   - Lombok Annotations Support

2. Open folder with VS Code
3. Maven will auto-detect pom.xml

## Database Migrations

Migrations are automatically applied using Flyway on application startup.

Location: `src/main/resources/db/migration/`

To create a new migration:
1. Create file: `V{number}__{description}.sql`
2. Add SQL statements
3. Restart application (migrations run automatically)

Example:
```sql
-- V2__Add_notification_archive_table.sql
CREATE TABLE notification_archive (
    id VARCHAR(36) PRIMARY KEY,
    notification_id VARCHAR(36) NOT NULL,
    archived_at TIMESTAMP,
    FOREIGN KEY (notification_id) REFERENCES notifications(id)
);
```

## Troubleshooting

### Issue: "Connection refused" on localhost:5432
**Solution:**
- Verify PostgreSQL is running
- Check credentials in application.yml
- Verify database `notification_db` exists

### Issue: "Kafka bootstrap failed"
**Solution:**
- Verify Kafka is running
- Check bootstrap servers in application.yml
- Verify Kafka topics exist or enable auto-topic creation

### Issue: "Port already in use"
**Solution:**
```bash
# Kill process using port 8080
# On Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# On macOS/Linux
lsof -ti :8080 | xargs kill -9
```

### Issue: Build fails with "Java version"
**Solution:**
- Ensure Java 17+ is installed
- Set JAVA_HOME environment variable
- Verify Maven uses correct Java version: `mvn -version`

### Issue: Docker container won't start
**Solution:**
```bash
# View logs
docker-compose logs notification-service

# Restart containers
docker-compose down
docker-compose up -d

# Rebuild container
docker-compose up -d --build
```

## Performance Tuning

### Kafka Consumer Configuration
In `KafkaConfig.java`:
```java
props.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, 500);  // Increase for higher throughput
props.put(ConsumerConfig.FETCH_MIN_BYTES_CONFIG, 1024);  // Batch processing
```

### Database Connection Pooling
In `application.yml`:
```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      idle-timeout: 600000
```

### JVM Tuning
In `docker-compose.yml`:
```yaml
environment:
  JAVA_OPTS: "-Xmx512m -Xms256m -XX:+UseG1GC"
```

## Next Steps

1. [Read API Documentation](API_EXAMPLES.md)
2. [Configure notification channels](src/main/java/com/notification/service/)
3. [Set up real email/SMS providers](README.md#integration)
4. [Configure production database](src/main/resources/application.yml)
5. [Deploy to production](README.md#deployment)

## Support

For issues and questions:
1. Check [Troubleshooting](#troubleshooting) section
2. View application logs: `docker-compose logs -f notification-service`
3. Check Kafka UI: http://localhost:8888
4. Create an issue in the repository

## Additional Resources

- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Flyway Documentation](https://flywaydb.org/documentation/)
