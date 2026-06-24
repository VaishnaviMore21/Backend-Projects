# Project Overview

## 🎯 Real-Time Notification System - Complete Backend Project

This is a production-ready, event-driven notification system built with **Java Spring Boot**, **Apache Kafka**, **PostgreSQL**, and **Docker**.

## 📦 What's Included

### Core Features
✅ Multi-channel notifications (Email, SMS, Push)
✅ Event-driven architecture with Kafka
✅ Real-time async processing
✅ User preference management
✅ Retry mechanism with automatic recovery
✅ Notification tracking and status monitoring
✅ RESTful API endpoints
✅ Comprehensive error handling
✅ Docker containerization
✅ Database migrations with Flyway
✅ Unit and integration tests

### Technology Stack
- **Backend**: Java 17, Spring Boot 3.2
- **Message Queue**: Apache Kafka 7.6
- **Database**: PostgreSQL 16
- **Build Tool**: Maven 3.9
- **Testing**: JUnit 5, Mockito
- **Containerization**: Docker & Docker Compose
- **Database Migration**: Flyway

## 📁 Project Structure

```
realtime-notification-system/
├── src/
│   ├── main/
│   │   ├── java/com/notification/
│   │   │   ├── config/              # Kafka & Spring configuration
│   │   │   ├── controller/          # REST API endpoints
│   │   │   ├── service/             # Business logic
│   │   │   ├── entity/              # JPA entities
│   │   │   ├── repository/          # Data access layer
│   │   │   ├── producer/            # Kafka producer
│   │   │   ├── consumer/            # Kafka consumer
│   │   │   ├── dto/                 # Data transfer objects
│   │   │   └── exception/           # Custom exceptions
│   │   └── resources/
│   │       ├── application.yml      # Configuration
│   │       └── db/migration/        # Database migrations
│   └── test/
│       └── java/com/notification/   # Unit tests
├── docker-compose.yml               # Docker services
├── Dockerfile                       # Application container
├── pom.xml                         # Maven dependencies
├── README.md                       # Main documentation
├── SETUP.md                        # Installation guide
├── API_EXAMPLES.md                 # API usage examples
├── build.sh                        # Build script
└── start.sh                        # Startup script
```

## 🚀 Quick Start

### Using Docker Compose (Recommended)
```bash
# Clone and navigate
git clone <repository-url>
cd realtime-notification-system

# Start services
docker-compose up -d

# Test health
curl http://localhost:8080/api/notifications/health
```

### Manual Setup
```bash
# Build project
mvn clean install

# Run application
mvn spring-boot:run
```

## 📊 Key Components

### 1. **NotificationController**
RESTful endpoints for notification management:
- POST `/api/notifications/send` - Send notification
- GET `/api/notifications/{id}/status` - Get status
- GET `/api/notifications/recipient/{id}` - List by recipient
- GET `/api/notifications/channel/{channel}` - List by channel
- POST/GET `/api/notifications/preferences/{userId}` - User preferences

### 2. **NotificationService**
Core business logic:
- Validates notifications
- Checks user preferences
- Publishes events to Kafka
- Handles retry logic
- Manages user preferences

### 3. **NotificationProducer**
Kafka producer:
- Publishes notification events
- Batch processing support
- Automatic retry on failure

### 4. **NotificationConsumer**
Kafka consumer:
- Consumes notification events
- Routes to appropriate channel service
- Updates notification status
- Error handling and logging

### 5. **Channel Services**
- **EmailNotificationService** - Email sending
- **SmsNotificationService** - SMS sending
- **PushNotificationService** - Push notifications

### 6. **KafkaConfig**
Complete Kafka setup:
- Producer factory with JSON serialization
- Consumer factory configuration
- Topic creation (auto-provisioning)
- Performance optimization

## 🔄 Event Flow

```
1. API Request → NotificationController
   ↓
2. Validation → NotificationService
   ↓
3. Event Publishing → NotificationProducer
   ↓
4. Kafka Topic → notification-events
   ↓
5. Event Consumption → NotificationConsumer
   ↓
6. Channel Processing → Service (Email/SMS/Push)
   ↓
7. Database Update → PostgreSQL
   ↓
8. Status Available → API Response
```

## 💾 Database Schema

### notifications
- Stores all notification records
- Tracks status, retries, errors
- JSONB field for metadata

### notification_templates
- Reusable notification templates
- Per-channel templates
- Active/inactive management

### user_preferences
- User notification settings
- Channel preferences
- Contact information

## 🔧 Configuration

### application.yml
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/notification_db
  kafka:
    bootstrap-servers: localhost:9092
```

### Kafka Topics
| Topic | Partitions | Retention |
|-------|-----------|-----------|
| notification-events | 3 | 7 days |
| notification-retry | 1 | 1 day |

## 📈 Performance Features

- **Async Processing**: Non-blocking notification delivery
- **Batch Support**: Send multiple notifications efficiently
- **Retry Logic**: Automatic failed notification recovery
- **Connection Pooling**: HikariCP for database connections
- **Consumer Concurrency**: 3 concurrent message consumers
- **Message Compression**: Snappy compression for Kafka
- **Auto Commit**: 1-second commit interval

## 🧪 Testing

### Unit Tests
```bash
mvn test
```

Includes tests for:
- NotificationService
- NotificationController
- NotificationProducer

### Running Specific Tests
```bash
mvn test -Dtest=NotificationServiceTest
```

## 📚 API Examples

### Send Notification
```bash
curl -X POST http://localhost:8080/api/notifications/send \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_id": "user123",
    "channel": "EMAIL",
    "subject": "Welcome",
    "message": "Welcome to our platform",
    "recipient_address": "user@example.com",
    "priority": "HIGH"
  }'
```

### Get Status
```bash
curl http://localhost:8080/api/notifications/{notificationId}/status
```

See [API_EXAMPLES.md](API_EXAMPLES.md) for more examples.

## 🛠️ Development

### Add New Notification Channel

1. Create service:
```java
@Service
public class SlackNotificationService {
    public void sendSlack(NotificationEventDto event, Notification notification) {
        // Implementation
    }
}
```

2. Update consumer:
```java
case "SLACK":
    slackNotificationService.sendSlack(event, notification);
    break;
```

3. Test the channel

### Extend Database Schema

1. Create migration file: `src/main/resources/db/migration/V2__description.sql`
2. Add SQL statements
3. Restart application (migration runs automatically)

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Verify PostgreSQL running on port 5432 |
| Kafka connection error | Check Kafka bootstrap server configuration |
| Port already in use | Kill process: `lsof -ti :8080 \| xargs kill -9` |
| Build fails | Verify Java 17+ installed: `java -version` |

See [SETUP.md](SETUP.md) for detailed troubleshooting.

## 📋 Kafka UI

Access Kafka UI at: **http://localhost:8888**

Features:
- View topics and partitions
- Monitor consumer groups
- Inspect messages
- Topic statistics

## 🔐 Security Considerations

Currently implemented:
- Input validation on all endpoints
- Error handling without exposing internals
- Database prepared statements (JPA)

Recommended for production:
- Add authentication (JWT/OAuth2)
- Implement authorization (roles/permissions)
- Add rate limiting
- Encrypt sensitive data
- Use HTTPS/TLS
- Implement audit logging

## 📈 Scaling

### Horizontal Scaling
- Increase Kafka partitions for more parallelism
- Deploy multiple instances behind load balancer
- Use database replicas for read operations

### Vertical Scaling
- Increase consumer concurrency: `factory.setConcurrency(10)`
- Increase batch size: `MAX_POLL_RECORDS_CONFIG: 500`
- Adjust JVM heap: `-Xmx2g -Xms1g`

## 📝 Next Steps

1. **Integrate Email Provider**: SendGrid, AWS SES, or Mailgun
2. **Integrate SMS Provider**: Twilio, AWS SNS, or Nexmo
3. **Add Monitoring**: Prometheus, Grafana, or ELK stack
4. **Implement Caching**: Redis for frequently accessed data
5. **Add Rate Limiting**: Prevent abuse
6. **Implement Authentication**: Secure API endpoints
7. **Deploy to Cloud**: AWS, GCP, Azure, or Kubernetes

## 📞 Support

For help:
1. Check [SETUP.md](SETUP.md) for installation
2. Review [API_EXAMPLES.md](API_EXAMPLES.md) for usage
3. Check [README.md](README.md) for documentation
4. View logs: `docker-compose logs -f`
5. Create an issue in the repository

## 📄 License

MIT License - Feel free to use in your projects!

---

**Happy Coding! 🚀**
