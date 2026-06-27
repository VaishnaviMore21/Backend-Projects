# SQL Query Generator from Natural Language

A production-ready solution for converting natural language questions into SQL queries using LangChain, PostgreSQL, and local LLM inference via Ollama.

## Project Summary

This project implements a complete SQL Query Generator that:
- Accepts natural language questions from users
- Converts them to valid PostgreSQL queries using an LLM (Ollama)
- Executes queries securely with multiple validation layers
- Returns results in a paginated, user-friendly HTML interface
- Maintains comprehensive audit logs for compliance

## What's Included

### Core Features
✅ **Natural Language Processing** - Converts English questions to SQL  
✅ **Schema-Aware Generation** - LLM understands your database structure  
✅ **Security-First Execution** - Read-only roles, query validation, timeouts  
✅ **Web UI** - Modern, responsive interface for queries  
✅ **REST API** - Full API for programmatic access  
✅ **Audit Logging** - Complete trail of all queries  
✅ **Docker Support** - One-command deployment  
✅ **Local LLM** - Privacy-first with Ollama integration  

### Project Structure
```
sql-query-generator/
├── app/                           # Flask application
│   ├── core/
│   │   ├── schema_extractor.py   # Extract DB schema
│   │   ├── query_generator.py    # LLM integration
│   │   ├── query_executor.py     # Secure execution
│   │   ├── security.py           # Validation & guardrails
│   │   └── logging_service.py    # Audit logging
│   ├── schemas/models.py          # Pydantic models
│   ├── routes.py                  # Flask endpoints
│   ├── config.py                  # Configuration
│   ├── utils.py                   # Helper functions
│   └── __init__.py                # App factory
├── database/
│   ├── schema.sql                 # Initial setup
│   ├── sample_data.sql            # Business data
├── templates/
│   ├── index.html                 # Main UI
│   └── results.html               # Logs page
├── static/
│   ├── style.css                  # Styling
│   ├── script.js                  # UI logic
│   └── logs.js                    # Log viewer
├── logs/                          # Audit trail
├── main.py                        # Entry point
├── requirements.txt               # Python deps
├── Dockerfile                     # Container image
├── docker-compose.yml             # Full stack setup
├── start.sh / start.bat           # Quick start
├── README.md                      # Full documentation
├── SETUP.md                       # Setup guide
├── API_EXAMPLES.md                # API usage
└── .env.example                   # Configuration template
```

## Key Modules

### 1. **schema_extractor.py**
- Connects to PostgreSQL and extracts schema
- Gets table names, columns, data types
- Identifies primary keys and foreign keys
- Formats schema for LLM context

### 2. **query_generator.py**
- Integrates with Ollama API
- Uses schema-aware prompting
- Generates SQL with low temperature (deterministic)
- Handles retries on validation failure
- Calculates confidence scores

### 3. **query_executor.py**
- Executes queries with read-only role
- Implements pagination
- Handles timeouts (30s default)
- Returns structured results
- Calculates execution metrics

### 4. **security.py**
- Validates SQL syntax
- Blocks dangerous operations (DROP, DELETE, etc.)
- Prevents SQL injection patterns
- Restricts table/column access
- Masks sensitive data

### 5. **logging_service.py**
- Logs all queries to file and database
- Tracks success/failure
- Records execution time and row count
- Provides audit statistics
- Enables compliance reporting

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: PostgreSQL 14+
- **LLM**: Ollama (local inference)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Containerization**: Docker & Docker Compose
- **Security**: Parameterized queries, read-only roles

## Quick Start

### With Docker (Recommended)
```bash
cd sql-query-generator
./start.sh    # Linux/Mac
# or
start.bat     # Windows
```

### Local Setup
1. Install PostgreSQL and Ollama
2. Create database: `psql -f database/schema.sql`
3. Load sample data: `psql -f database/sample_data.sql`
4. Start Ollama: `ollama serve` (pull mistral)
5. Setup Python: `python -m venv venv && pip install -r requirements.txt`
6. Run app: `python main.py`
7. Visit: http://localhost:5000

## Usage Examples

### Web Interface
1. Navigate to http://localhost:5000
2. Type a question: "Show top 5 products by revenue"
3. Click "Generate & Execute"
4. View paginated results

### REST API
```bash
# Generate SQL
curl -X POST http://localhost:5000/api/query/generate \
  -H "Content-Type: application/json" \
  -d '{"question": "Active users"}'

# Execute query
curl -X POST http://localhost:5000/api/query/execute \
  -H "Content-Type: application/json" \
  -d '{"question": "List all orders", "page": 1, "page_size": 20}'

# View logs
curl http://localhost:5000/api/logs
```

## Security Features

- **Read-Only Execution**: Separate PostgreSQL role for queries
- **Query Validation**: Regex patterns block dangerous operations
- **Timeout Protection**: 30s default (configurable)
- **Schema Filtering**: Only safe tables exposed to LLM
- **Audit Trail**: Every query logged with user/timestamp/status
- **Input Sanitization**: HTML escaping, type conversion
- **Error Masking**: Friendly user messages, detailed logs

## Configuration

Edit `.env` to customize:
```env
POSTGRES_HOST=localhost          # DB host
POSTGRES_PORT=5432              # DB port
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=mistral            # Model to use
QUERY_TIMEOUT_MS=30000          # Query timeout
DEFAULT_PAGE_SIZE=20            # Results per page
LOG_LEVEL=INFO                  # Logging level
```

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health` | Health check |
| GET | `/api/schema` | Get database schema |
| POST | `/api/query/generate` | Generate SQL only |
| POST | `/api/query/execute` | Generate and execute |
| POST | `/api/query/preview` | Preview first 5 rows |
| GET | `/api/logs` | View audit logs |
| GET | `/api/logs/stats` | Query statistics |

## Performance Tips

1. **Database**: Create indexes on frequently queried columns
2. **LLM**: Use mistral (~7B) for faster response than llama2 (~13B)
3. **Pagination**: Use pagination for large result sets
4. **Caching**: Cache schema extraction (already done)
5. **Monitoring**: Review audit logs for optimization opportunities

## Troubleshooting

### "Connection refused" (PostgreSQL)
- Ensure PostgreSQL is running
- Check connection string in `.env`

### "No route to Ollama"
- Ensure Ollama is running: `ollama serve`
- Check port 11434 is accessible

### Slow SQL generation
- Try simpler questions
- Use faster model (mistral vs llama2)
- Check LLM logs

### SQL validation errors
- Review generated query in error message
- Rephrase question more specifically
- Check [API_EXAMPLES.md](API_EXAMPLES.md) for patterns

## Future Enhancements

- [ ] Multi-database support (MySQL, SQL Server, BigQuery)
- [ ] Query explanation in natural English
- [ ] Result visualization (charts, graphs)
- [ ] Caching for repeated questions
- [ ] Role-based access control
- [ ] Query optimization suggestions
- [ ] BI tool integration (Tableau, Metabase)
- [ ] Time-series data support
- [ ] Advanced aggregations (window functions)
- [ ] Real-time query monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file

## Support

For issues, questions, or contributions:
1. Check [SETUP.md](SETUP.md) for setup help
2. Review [API_EXAMPLES.md](API_EXAMPLES.md) for API usage
3. Check [README.md](README.md) for detailed documentation
4. Review logs in `logs/sql_generator.log`

---

**Built with ❤️ using LangChain, PostgreSQL, and Ollama**
