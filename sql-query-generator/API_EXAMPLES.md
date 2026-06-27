# API Examples - SQL Query Generator

Complete examples of using the SQL Query Generator API.

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### 1. Health Check

**GET** `/health`

Check if the service is running.

```bash
curl http://localhost:5000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "SQL Query Generator is running"
}
```

---

### 2. Get Database Schema

**GET** `/schema`

Retrieve the complete database schema, including table names, columns, and relationships.

```bash
curl http://localhost:5000/api/schema
```

**Response:**
```json
{
  "tables": {
    "users": {
      "columns": {
        "id": {
          "type": "integer",
          "nullable": false,
          "primary_key": true
        },
        "email": {
          "type": "character varying",
          "nullable": false,
          "primary_key": false
        },
        "status": {
          "type": "character varying",
          "nullable": true,
          "primary_key": false
        }
      },
      "row_count": 8
    },
    "orders": {
      "columns": {
        "id": {
          "type": "integer",
          "nullable": false,
          "primary_key": true
        },
        "user_id": {
          "type": "integer",
          "nullable": false,
          "primary_key": false
        },
        "total_amount": {
          "type": "numeric",
          "nullable": true,
          "primary_key": false
        }
      },
      "row_count": 10
    }
  },
  "relationships": {
    "orders": [
      {
        "column": "user_id",
        "references": "users",
        "foreign_key": "id"
      }
    ]
  }
}
```

---

### 3. Generate SQL Query

**POST** `/query/generate`

Generate SQL from natural language without executing it.

**Request:**
```bash
curl -X POST http://localhost:5000/api/query/generate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Show top 5 customers by total spending",
    "explain": true
  }'
```

**Request Body:**
```json
{
  "question": "Show top 5 customers by total spending",
  "explain": true
}
```

**Response:**
```json
{
  "query": "SELECT u.id, u.email, SUM(o.total_amount) as total_spending FROM users u JOIN orders o ON u.id = o.user_id GROUP BY u.id, u.email ORDER BY total_spending DESC LIMIT 5;",
  "confidence": 0.92,
  "explanation": "This query joins the users table with orders, groups by user to calculate total spending, and returns the top 5 customers sorted by spending in descending order.",
  "is_valid": true
}
```

---

### 4. Execute Query

**POST** `/query/execute`

Generate and execute a SQL query with pagination.

**Request:**
```bash
curl -X POST http://localhost:5000/api/query/execute \
  -H "Content-Type: application/json" \
  -H "X-User-Email: user@example.com" \
  -d '{
    "question": "What are the monthly revenue trends",
    "page": 1,
    "page_size": 20,
    "explain_query": false
  }'
```

**Request Body:**
```json
{
  "question": "What are the monthly revenue trends",
  "page": 1,
  "page_size": 20,
  "explain_query": false
}
```

**Response (Success):**
```json
{
  "results": [
    {
      "month": 1,
      "total_revenue": 1529.88
    },
    {
      "month": 2,
      "total_revenue": 839.95
    }
  ],
  "total_rows": 2,
  "page": 1,
  "page_size": 20,
  "execution_time_ms": 45,
  "query": "SELECT EXTRACT(MONTH FROM created_at) as month, SUM(total_amount) as total_revenue FROM orders GROUP BY month ORDER BY month;",
  "confidence": 0.88
}
```

**Response (Error):**
```json
{
  "error": "Generated query failed security validation",
  "message": "Operation 'DELETE' is not allowed for security reasons"
}
```

---

### 5. Preview Query

**POST** `/query/preview`

Get a preview of query results (limited to 5 rows).

**Request:**
```bash
curl -X POST http://localhost:5000/api/query/preview \
  -H "Content-Type: application/json" \
  -d '{
    "question": "List all products with low stock"
  }'
```

**Response:**
```json
{
  "query": "SELECT * FROM products WHERE stock_quantity < reorder_level ORDER BY stock_quantity;",
  "preview": [
    {
      "id": 14,
      "sku": "BOOK-003",
      "name": "Machine Learning Guide",
      "price": 65.00,
      "stock_quantity": 15
    }
  ],
  "confidence": 0.90,
  "row_count": 1
}
```

---

### 6. Get Audit Logs

**GET** `/logs`

Retrieve audit logs with optional filters.

**Query Parameters:**
- `page` (int, default: 1) - Page number
- `page_size` (int, default: 20) - Results per page
- `user_email` (string, optional) - Filter by user email

**Request:**
```bash
curl "http://localhost:5000/api/logs?page=1&page_size=10&user_email=user@example.com"
```

**Response:**
```json
{
  "logs": [
    {
      "id": 1,
      "user_email": "user@example.com",
      "question": "Show top 5 customers",
      "generated_sql": "SELECT ...",
      "execution_status": "success",
      "error_message": null,
      "rows_returned": 5,
      "execution_time_ms": 45,
      "created_at": "2024-01-15T10:23:45"
    },
    {
      "id": 2,
      "user_email": "user@example.com",
      "question": "Delete all orders",
      "generated_sql": "SELECT ...",
      "execution_status": "validation_failed",
      "error_message": "Operation 'DELETE' is not allowed",
      "rows_returned": 0,
      "execution_time_ms": 12,
      "created_at": "2024-01-15T10:24:01"
    }
  ],
  "page": 1,
  "page_size": 10,
  "total": 2
}
```

---

### 7. Get Log Statistics

**GET** `/logs/stats`

Get statistics on query execution.

**Query Parameters:**
- `hours` (int, default: 24) - Time period in hours

**Request:**
```bash
curl "http://localhost:5000/api/logs/stats?hours=24"
```

**Response:**
```json
{
  "stats": {
    "total_queries": 45,
    "successful_queries": 42,
    "failed_queries": 3,
    "avg_execution_time": 32.5,
    "max_execution_time": 156,
    "total_rows_returned": 1205
  },
  "period_hours": 24
}
```

---

## Common Use Cases

### Get Total Revenue
```bash
curl -X POST http://localhost:5000/api/query/execute \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the total revenue from all orders?",
    "page": 1,
    "page_size": 1
  }'
```

### Find Customers Who Haven't Ordered Recently
```bash
curl -X POST http://localhost:5000/api/query/execute \
  -H "Content-Type: application/json" \
  -d '{
    "question": "List customers who haven not ordered in the last 6 months",
    "page": 1,
    "page_size": 20
  }'
```

### Check Inventory Levels
```bash
curl -X POST http://localhost:5000/api/query/execute \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Show products with stock below reorder level",
    "page": 1,
    "page_size": 50
  }'
```

### Product Performance
```bash
curl -X POST http://localhost:5000/api/query/execute \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Which products have the highest average rating and at least 100 units sold?",
    "page": 1,
    "page_size": 10
  }'
```

### Payment Status Report
```bash
curl -X POST http://localhost:5000/api/query/execute \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Count pending vs completed payments for this month",
    "page": 1,
    "page_size": 10
  }'
```

---

## Error Handling

### Security Validation Error
```json
{
  "error": "Generated query failed security validation",
  "message": "Operation 'DROP' is not allowed for security reasons"
}
```

### Database Error
```json
{
  "error": "Unknown column in select list",
  "execution_time_ms": 23
}
```

### Invalid Request
```json
{
  "error": "Invalid request: 'question' field is required"
}
```

### Timeout Error
```json
{
  "error": "Query timeout after 30000ms",
  "execution_time_ms": 30000
}
```

---

## Tips for Best Results

1. **Be specific in your questions:**
   - ❌ "Show me data"
   - ✅ "Show top 10 products by revenue in Q4"

2. **Include filtering criteria:**
   - ❌ "Customer information"
   - ✅ "Active customers from New York with more than 5 orders"

3. **Specify ordering:**
   - Include "top", "bottom", "highest", "lowest", "most recent", etc.
   - Example: "Top 5 customers by spending last quarter"

4. **Use natural date references:**
   - "Last week", "This month", "Last quarter", "2024"

5. **Ask for aggregations when needed:**
   - "Total", "Count", "Average", "Sum", "Monthly trends"

---

## Rate Limiting

The API currently has basic rate limiting:
- Default: 10 queries per minute per user
- Can be configured in `app/config.py`

---

## Authentication

Currently uses optional user identification:
- Send `X-User-Email` header for tracking
- Example: `curl -H "X-User-Email: user@example.com" ...`

---

For more information, see the [README.md](README.md) and [SETUP.md](SETUP.md).
