# Event-Driven Ordering System

**Stack:** Java 17 · Spring Boot 3.2 · Apache Kafka · PostgreSQL · Lombok · Maven (multi-module)

## Project Structure

```text
ordering-service/
├── api-gateway/
├── service-registry/
├── config-server/
├── inventory-service/
├── payment-service/
├── user-service/
├── order-service/
├── notification-service/
└── shared-events/
```

## Event Flow

```
Step 1  POST /orders  →  Order Service saves PENDING  →  publishes  order.placed
Step 2  Inventory Service  receives order.placed
           OK  →  deducts stock  →  inventory.reserved
           FAIL →  inventory.failed
Step 3  Payment Service  receives inventory.reserved
           OK  (amount ≤ 10 000)  →  payment.processed
           FAIL (amount > 10 000) →  payment.failed
Step 4  Order Service  receives terminal event
           payment.processed   →  status = CONFIRMED
           payment.failed      →  status = CANCELLED
           inventory.failed    →  status = CANCELLED
Step 5  Notification Service  receives terminal event  →  logs email
```

## Kafka Topics

| Topic                | Producer          | Consumer(s)                           |
|----------------------|-------------------|---------------------------------------|
| order.placed         | order-service     | inventory-service                     |
| inventory.reserved   | inventory-service | payment-service                       |
| inventory.failed     | inventory-service | order-service, notification-service   |
| payment.processed    | payment-service   | order-service, notification-service   |
| payment.failed       | payment-service   | order-service, notification-service   |

## Services

| Service              | Port | DB          |
|----------------------|------|-------------|
| order-service        | 8081 | orderdb     |
| inventory-service    | 8082 | inventorydb |
| payment-service      | 8083 | paymentdb   |
| notification-service | 8084 | —           |
| kafka-ui             | 8080 | —           |

## Quick Start

```bash
# 1. Start infrastructure
docker-compose up -d

# 2. Build all modules
mvn clean install -DskipTests

# 3. Start services (separate terminals)
cd order-service        && mvn spring-boot:run
cd inventory-service    && mvn spring-boot:run
cd payment-service      && mvn spring-boot:run
cd notification-service && mvn spring-boot:run

# 4. Place an order
curl -X POST http://localhost:8081/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": "C001",
    "customerEmail": "alice@example.com",
    "items": [
      {"productId":"P001","productName":"Laptop","quantity":1,"unitPrice":999.99},
      {"productId":"P002","productName":"Mouse","quantity":2,"unitPrice":29.99}
    ]
  }'

# 5. Check order status
curl http://localhost:8081/orders/{orderId}

# 6. Check inventory
curl http://localhost:8082/inventory

# 7. Check payments
curl http://localhost:8083/payments
```

## Business Rules (Demo)
- Payment **succeeds** when total amount ≤ 10,000
- Payment **fails**   when total amount > 10,000
- Inventory pre-seeded: Laptop×50, Mouse×200, Keyboard×150, Monitor×30
