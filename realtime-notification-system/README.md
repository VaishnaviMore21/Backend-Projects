# Real-Time Notification System

A high-performance, event-driven notification system built with Spring Boot, Apache Kafka, and PostgreSQL.

## 🎯 Features

- **Multi-Channel Notifications**: Email, SMS, Push Notifications
- **Event-Driven Architecture**: Kafka-based async processing
- **High Reliability**: Retry mechanism with exponential backoff
- **User Preferences**: Manage notification preferences per user
- **Template Support**: Reusable notification templates
- **Real-time Processing**: Sub-second notification delivery
- **Comprehensive Logging**: Full traceability of notifications
- **REST API**: Easy integration with other services
- **Database Persistence**: PostgreSQL for reliable storage
- **Docker Support**: Docker Compose for easy deployment

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    REST API                              │
├─────────────────────────────────────────────────────────┤
│              NotificationController                      │
├─────────────────────────────────────────────────────────┤
│              NotificationService                         │
├──────────────────────┬──────────────────────────────────┤
│  NotificationProducer │      UserPreferenceService       │
└──────────────┬───────┴──────────────────────────────────┘
               │
          [Kafka Topics]
               │
┌──────────────┴───────────────────────────────────────────┐
│              NotificationConsumer                         │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┬──────────────┬──────────────┐          │
│  │    Email     │     SMS      │    Push      │          │
│  │   Service    │   Service    │   Service    │          │
│  └──────────────┴──────────────┴──────────────┘          │
├─────────────────────────────────────────────────────────┤
│                   PostgreSQL                             │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Java 17+
- Maven 3.9+
- Docker & Docker Compose

### Setup with Docker Compose

```bash
# Clone the repository
git clone <repository-url>
cd realtime-notification-system

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f notification-service
```

The application will be available at: `http://localhost:8080/api`

### Manual Setup

1. **Install PostgreSQL & Kafka locally**

2. **Build the project**
```bash
mvn clean install
```

3. **Run the application**
```bash
mvn spring-boot:run
```

## 📚 API Endpoints

### Send Notification
```http
POST /api/notifications/send
Content-Type: application/json

{
  "recipient_id": "user123",
  "channel": "EMAIL",
  "subject": "Welcome",
  "message": "Welcome to our platform",
  "recipient_address": "user@example.com",
  "priority": "HIGH",
  "metadata": {
    "source": "signup"
  }
}

Response:
{
  "notification_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "ACCEPTED",
  "message": "Notification queued for processing",
  "timestamp": 1700000000000
}
```

### Get Notification Status
```http
GET /api/notifications/{notificationId}/status

Response:
{
  "notification_id": "550e8400-e29b-41d4-a716-446655440000",
  "recipient_id": "user123",
  "channel": "EMAIL",
  "status": "SENT",
  "error_message": null,
  "retry_count": 0,
  "created_at": 1700000000000,
  "updated_at": 1700000001000
}
```

### Get Notifications by Recipient
```http
GET /api/notifications/recipient/{recipientId}

Response: Array of NotificationStatusDto
```

### Get Notifications by Channel
```http
GET /api/notifications/channel/{channel}

Response: Array of NotificationStatusDto
```

### Save User Preferences
```http
POST /api/notifications/preferences/{userId}
Content-Type: application/json

{
  "email_enabled": true,
  "sms_enabled": true,
  "push_enabled": false,
  "email_address": "user@example.com",
  "phone_number": "+1234567890",
  "push_device_token": "device_token_xyz"
}
```

### Get User Preferences
```http
GET /api/notifications/preferences/{userId}

Response:
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user123",
  "email_enabled": true,
  "sms_enabled": true,
  "push_enabled": false,
  "email_address": "user@example.com",
  "phone_number": "+1234567890",
  "push_device_token": "device_token_xyz",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

## 🔧 Configuration

### application.yml

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/notification_db
    username: postgres
    password: postgres
  
  kafka:
    bootstrap-servers: localhost:9092
    producer:
      acks: all
      retries: 3
    consumer:
      group-id: notification-consumer-group
      auto-offset-reset: earliest
```

## 📊 Database Schema

### notifications
- `id`: UUID Primary Key
- `recipient_id`: String (indexed)
- `channel`: VARCHAR(50) - EMAIL, SMS, PUSH
- `subject`: VARCHAR(255)
- `message`: TEXT
- `recipient_address`: VARCHAR(255)
- `status`: VARCHAR(50) - PENDING, SENT, FAILED, DELIVERED
- `retry_count`: INTEGER
- `priority`: VARCHAR(20) - HIGH, NORMAL, LOW
- `error_message`: TEXT
- `created_at`: TIMESTAMP
- `updated_at`: TIMESTAMP
- `sent_at`: TIMESTAMP
- `metadata`: JSONB

### notification_templates
- `id`: UUID Primary Key
- `template_name`: VARCHAR(255) Unique
- `channel`: VARCHAR(50)
- `subject`: VARCHAR(255)
- `body`: TEXT
- `is_active`: BOOLEAN
- `created_at`: TIMESTAMP
- `updated_at`: TIMESTAMP

### user_preferences
- `id`: UUID Primary Key
- `user_id`: VARCHAR(100) Unique (indexed)
- `email_enabled`: BOOLEAN
- `sms_enabled`: BOOLEAN
- `push_enabled`: BOOLEAN
- `email_address`: VARCHAR(255)
- `phone_number`: VARCHAR(20)
- `push_device_token`: VARCHAR(255)
- `created_at`: TIMESTAMP
- `updated_at`: TIMESTAMP

## 🔄 Kafka Topics

| Topic | Partitions | Retention | Purpose |
|-------|-----------|-----------|---------|
| notification-events | 3 | 7 days | Main notification event stream |
| notification-retry | 1 | 1 day | Failed notification retry queue |

## 🔄 Retry Mechanism

- Failed notifications are automatically retried
- Retry scheduler runs every 60 seconds
- Maximum retry attempts: 3 (configurable)
- Retry backoff: 5 minutes
- Higher priority notifications are retried first

## 📈 Monitoring

### Health Check
```http
GET /api/notifications/health
```

### Kafka UI
Access the Kafka UI at: `http://localhost:8888`

### Logs
```bash
# View application logs
docker-compose logs -f notification-service

# View Kafka logs
docker-compose logs -f kafka
```

## 🛠️ Development

### Project Structure
```
src/main/java/com/notification/
├── config/           # Kafka & Spring configuration
├── controller/       # REST endpoints
├── service/          # Business logic
├── entity/           # JPA entities
├── repository/       # Data access layer
├── producer/         # Kafka producer
├── consumer/         # Kafka consumer
├── dto/              # Data transfer objects
└── exception/        # Custom exceptions
```

### Adding a New Notification Channel

1. Create a new service in `service/` package:
```java
@Service
public class SlackNotificationService {
    public void sendSlack(NotificationEventDto event, Notification notification) {
        // Implementation
    }
}
```

2. Update `NotificationConsumer` to handle the new channel:
```java
case "SLACK":
    slackNotificationService.sendSlack(event, notification);
    break;
```

## 🐛 Troubleshooting

### Kafka Connection Error
- Check if Kafka is running: `docker-compose ps`
- Verify bootstrap servers configuration
- Check network connectivity

### Database Connection Error
- Ensure PostgreSQL is running
- Verify credentials in `application.yml`
- Check database exists: `notification_db`

### Notifications Not Being Processed
- Check consumer group: `notification-consumer-group`
- Verify topic exists: `notification-events`
- Check application logs for errors
- Use Kafka UI to inspect messages

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For issues and questions, please create an issue in the repository.
