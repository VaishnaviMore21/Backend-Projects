# SQL Query Generator from Natural Language

A powerful tool that converts natural language questions into executable SQL queries using LangChain and PostgreSQL with local LLM inference via Ollama.

## Features

✅ **Natural Language to SQL Conversion** - Ask questions in plain English  
✅ **Schema-Aware Prompting** - LLM constrained by actual database structure  
✅ **SQL-Only Output Mode** - Ensures only valid, executable SQL is generated  
✅ **Secure Query Execution** - Read-only role, validation, timeout, and parameterization  
✅ **Business Analytics Templates** - Pre-built queries for common patterns  
✅ **Paginated HTML Results** - Clean, sortable data tables  
✅ **Extensible Architecture** - Easy to add tables and business rules  
✅ **Auditability & Logging** - Full audit trail of prompts, queries, and execution  
✅ **Error Feedback Loop** - Automatic SQL regeneration on failures  
✅ **Local LLM Support** - Privacy-first with Ollama integration  

## Architecture

```
sql-query-generator/
├── app/
│   ├── core/
│   │   ├── schema_extractor.py    # Extract database schema
│   │   ├── query_generator.py     # LLM-powered SQL generation
│   │   ├── query_executor.py      # Secure execution layer
│   │   └── security.py            # Validation & guardrails
│   ├── schemas/
│   │   └── models.py              # Pydantic models
│   ├── routes.py                  # Flask endpoints
│   └── utils.py                   # Helper functions
├── database/
│   ├── schema.sql                 # Initial schema setup
│   ├── sample_data.sql            # Business sample data
│   └── migrations/
├── templates/
│   ├── index.html                 # Web UI
│   └── results.html               # Results display
├── static/
│   ├── style.css
│   └── script.js
├── logs/                          # Audit logs
├── main.py                        # Flask app entry
└── requirements.txt
```

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Ollama (with a model like `mistral` or `llama2`)

### Installation

1. Clone and setup:
```bash
cd sql-query-generator
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your PostgreSQL and Ollama settings
```

3. Initialize database:
```bash
psql -U postgres -f database/schema.sql
psql -U postgres -d business_db -f database/sample_data.sql
```

4. Start Ollama (in another terminal):
```bash
ollama serve
ollama pull mistral  # or your chosen model
```

5. Run the app:
```bash
python main.py
```

6. Open http://localhost:5000

## Usage

### Web Interface
- Navigate to home page
- Type a natural language question (e.g., "Show top 5 customers by total spending in 2024")
- Click "Generate & Execute"
- View paginated results with execution details

### Example Queries
- "What are the monthly revenue trends for Q4 2024?"
- "Which products have zero inventory?"
- "List customers who haven't ordered in the last 6 months"
- "Show the total discount given per product category"

## API Endpoints

### POST /api/query/generate
Generate SQL from natural language (without execution).

**Request:**
```json
{
  "question": "Show top 10 products by revenue",
  "explain": false
}
```

**Response:**
```json
{
  "query": "SELECT p.name, SUM(oi.quantity * oi.unit_price) as revenue FROM products p JOIN order_items oi ON p.id = oi.product_id GROUP BY p.id ORDER BY revenue DESC LIMIT 10;",
  "confidence": 0.92
}
```

### POST /api/query/execute
Execute a pre-validated SQL query.

**Request:**
```json
{
  "question": "List all active users",
  "page": 1,
  "page_size": 20
}
```

**Response:**
```json
{
  "results": [...],
  "total_rows": 150,
  "page": 1,
  "page_size": 20,
  "execution_time_ms": 45,
  "query": "SELECT * FROM users WHERE status='active' LIMIT 20 OFFSET 0;"
}
```

### GET /api/schema
Retrieve the full database schema.

**Response:**
```json
{
  "tables": [
    {
      "name": "users",
      "columns": [
        {"name": "id", "type": "integer", "nullable": false},
        {"name": "email", "type": "varchar", "nullable": false}
      ]
    }
  ]
}
```

### GET /api/logs
Retrieve audit logs (paginated).

## Security Features

- **Read-Only Execution**: Queries execute with restricted read-only PostgreSQL role
- **Query Validation**: Regex patterns block dangerous operations (DROP, DELETE, INSERT)
- **Timeout Protection**: Default 30s timeout to prevent resource exhaustion
- **Schema Filtering**: Only expose safe tables/columns for LLM context
- **Parameterization**: Prevent SQL injection through bound parameters where applicable
- **Audit Trail**: Every query logged with user, timestamp, execution details
- **Rate Limiting**: Optional per-user rate limiting (configurable)

## Configuration

### Schema & Table Exposure

Edit `app/core/security.py` to control which tables/columns the LLM sees:

```python
EXPOSED_TABLES = {
    'users': ['id', 'email', 'created_at'],
    'orders': ['id', 'user_id', 'total_amount'],
    'products': ['id', 'name', 'price']
}
```

### LLM Prompts

Customize SQL generation in `app/core/query_generator.py`:
- Adjust system prompt for domain-specific instructions
- Add business rules and constraints
- Define output format requirements

## Error Handling

When SQL generation or execution fails:
1. Error is logged with context
2. User receives friendly error message
3. Optional auto-regeneration with modified prompt
4. Suggestion for rephrasing question

## Logging & Auditability

All queries logged to `logs/sql_generator.log`:
```
[2024-01-15 10:23:45] USER: john@example.com | QUESTION: "Top 5 customers"
[2024-01-15 10:23:45] GENERATED SQL: SELECT ... LIMIT 5;
[2024-01-15 10:23:45] STATUS: SUCCESS | ROWS: 5 | EXECUTION_TIME: 23ms
```

## Advanced Usage

### Custom Business Rules

Add domain logic in `app/core/query_generator.py`:
```python
BUSINESS_RULES = {
    'sales_threshold': 1000,  # Minimum order value
    'active_status': 'active',
    'tax_rate': 0.08
}
```

### Template Queries

Pre-save complex queries in `database/templates.sql`:
```sql
-- Monthly Revenue Report
SELECT EXTRACT(MONTH FROM order_date) as month, SUM(total) FROM orders GROUP BY month;
```

## Performance Tips

1. **Index Key Columns**: Ensure `users.id`, `orders.user_id`, `products.id` are indexed
2. **Set Query Timeout**: Balance accuracy vs execution speed
3. **Batch Large Results**: Use pagination for 10K+ row results
4. **Monitor LLM Latency**: Ollama model selection impacts response time

## Troubleshooting

### "Connection refused" (PostgreSQL)
- Verify PostgreSQL is running: `psql --version`
- Check credentials in `.env`

### "No route to Ollama"
- Ensure Ollama is running: `ollama serve`
- Verify `OLLAMA_API_URL` matches Ollama port (default 11434)

### Slow SQL generation
- Check Ollama model size (mistral ~7B is faster than llama2 ~13B)
- Increase timeout in configuration

### Invalid SQL generated
- Review system prompt in `query_generator.py`
- Provide example questions to improve context
- Try rephrasing query

## Future Enhancements

- [ ] Multi-database support (MySQL, SQLServer, BigQuery)
- [ ] Query explanation in plain English
- [ ] Caching for repeated questions
- [ ] Chart visualization integration
- [ ] Role-based query access control
- [ ] Query optimization suggestions
- [ ] Integration with BI tools (Tableau, Metabase)

## License

MIT
