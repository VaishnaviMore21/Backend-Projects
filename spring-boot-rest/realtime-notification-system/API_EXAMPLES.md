# API Examples

## 1. Send Email Notification

### Request
```bash
curl -X POST http://localhost:8080/api/notifications/send \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_id": "user@123",
    "channel": "EMAIL",
    "subject": "Welcome to Our Platform",
    "message": "Hello, welcome to our awesome service!",
    "recipient_address": "john.doe@example.com",
    "priority": "HIGH",
    "metadata": {
      "source": "signup",
      "campaign_id": "camp_001"
    }
  }'
```

### Response
```json
{
  "notification_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "ACCEPTED",
  "message": "Notification queued for processing",
  "timestamp": 1700000000000
}
```

---

## 2. Send SMS Notification

### Request
```bash
curl -X POST http://localhost:8080/api/notifications/send \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_id": "user@456",
    "channel": "SMS",
    "message": "Your verification code is: 123456",
    "recipient_address": "+1234567890",
    "priority": "HIGH"
  }'
```

### Response
```json
{
  "notification_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "ACCEPTED",
  "message": "Notification queued for processing",
  "timestamp": 1700000001000
}
```

---

## 3. Send Push Notification

### Request
```bash
curl -X POST http://localhost:8080/api/notifications/send \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_id": "user@789",
    "channel": "PUSH",
    "subject": "Special Offer",
    "message": "Get 50% off on your next purchase!",
    "recipient_address": "ios_device_token_xyz",
    "priority": "NORMAL",
    "metadata": {
      "offer_id": "OFF_123",
      "expires_at": 1700086400000
    }
  }'
```

### Response
```json
{
  "notification_id": "770e8400-e29b-41d4-a716-446655440002",
  "status": "ACCEPTED",
  "message": "Notification queued for processing",
  "timestamp": 1700000002000
}
```

---

## 4. Get Notification Status

### Request
```bash
curl -X GET http://localhost:8080/api/notifications/550e8400-e29b-41d4-a716-446655440000/status
```

### Response
```json
{
  "notification_id": "550e8400-e29b-41d4-a716-446655440000",
  "recipient_id": "user@123",
  "channel": "EMAIL",
  "status": "SENT",
  "error_message": null,
  "retry_count": 0,
  "created_at": 1700000000000,
  "updated_at": 1700000001000
}
```

---

## 5. Get Notifications by Recipient

### Request
```bash
curl -X GET http://localhost:8080/api/notifications/recipient/user@123
```

### Response
```json
[
  {
    "notification_id": "550e8400-e29b-41d4-a716-446655440000",
    "recipient_id": "user@123",
    "channel": "EMAIL",
    "status": "SENT",
    "error_message": null,
    "retry_count": 0,
    "created_at": 1700000000000,
    "updated_at": 1700000001000
  },
  {
    "notification_id": "550e8400-e29b-41d4-a716-446655440003",
    "recipient_id": "user@123",
    "channel": "SMS",
    "status": "SENT",
    "error_message": null,
    "retry_count": 0,
    "created_at": 1700001000000,
    "updated_at": 1700001001000
  }
]
```

---

## 6. Get Notifications by Channel

### Request
```bash
curl -X GET http://localhost:8080/api/notifications/channel/EMAIL
```

### Response
```json
[
  {
    "notification_id": "550e8400-e29b-41d4-a716-446655440000",
    "recipient_id": "user@123",
    "channel": "EMAIL",
    "status": "SENT",
    "error_message": null,
    "retry_count": 0,
    "created_at": 1700000000000,
    "updated_at": 1700000001000
  },
  {
    "notification_id": "550e8400-e29b-41d4-a716-446655440004",
    "recipient_id": "user@200",
    "channel": "EMAIL",
    "status": "FAILED",
    "error_message": "Invalid email format",
    "retry_count": 1,
    "created_at": 1700002000000,
    "updated_at": 1700002005000
  }
]
```

---

## 7. Save User Preferences

### Request
```bash
curl -X POST http://localhost:8080/api/notifications/preferences/user@123 \
  -H "Content-Type: application/json" \
  -d '{
    "email_enabled": true,
    "sms_enabled": true,
    "push_enabled": false,
    "email_address": "john.doe@example.com",
    "phone_number": "+1234567890",
    "push_device_token": null
  }'
```

### Response
```
Preferences saved successfully
```

---

## 8. Get User Preferences

### Request
```bash
curl -X GET http://localhost:8080/api/notifications/preferences/user@123
```

### Response
```json
{
  "id": "850e8400-e29b-41d4-a716-446655440005",
  "user_id": "user@123",
  "email_enabled": true,
  "sms_enabled": true,
  "push_enabled": false,
  "email_address": "john.doe@example.com",
  "phone_number": "+1234567890",
  "push_device_token": null,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

---

## 9. Health Check

### Request
```bash
curl -X GET http://localhost:8080/api/notifications/health
```

### Response
```
Notification service is running
```

---

## Using Postman

You can also use Postman to test these endpoints. Here's a sample environment:

```json
{
  "name": "Local",
  "values": [
    {
      "key": "base_url",
      "value": "http://localhost:8080/api",
      "enabled": true
    },
    {
      "key": "recipient_id",
      "value": "user@123",
      "enabled": true
    },
    {
      "key": "notification_id",
      "value": "550e8400-e29b-41d4-a716-446655440000",
      "enabled": true
    }
  ]
}
```

Then use `{{base_url}}` and `{{recipient_id}}` in your requests.

---

## Error Responses

### 400 Bad Request
```json
{
  "status": 400,
  "message": "Validation failed",
  "errors": {
    "recipient_id": "Recipient ID is required"
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

### 404 Not Found
```json
{
  "status": 404,
  "message": "Notification not found",
  "details": "Notification not found with id: invalid-id",
  "timestamp": "2024-01-15T10:30:00"
}
```

### 500 Internal Server Error
```json
{
  "status": 500,
  "message": "Internal server error",
  "details": "An unexpected error occurred",
  "timestamp": "2024-01-15T10:30:00"
}
```
