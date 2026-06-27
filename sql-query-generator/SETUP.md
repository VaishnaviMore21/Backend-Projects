# Setup Guide for SQL Query Generator

This guide will help you set up the SQL Query Generator locally.

## Prerequisites

### Option 1: Docker Setup (Recommended)
- Docker 20.10+
- Docker Compose 2.0+
- At least 4GB RAM available

### Option 2: Local Setup
- Python 3.10+
- PostgreSQL 14+
- Ollama (with mistral or llama2 model)

---

## Quick Start with Docker

### 1. Clone and navigate to the project
```bash
cd sql-query-generator
```

### 2. Run the start script

**On Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**On Windows:**
```bash
start.bat
```

### 3. Access the application
- Web UI: http://localhost:5000
- API: http://localhost:5000/api/health

### 4. Pull Ollama model (if not done automatically)
```bash
docker-compose exec ollama ollama pull mistral
```

---

## Local Setup (Without Docker)

### 1. Install PostgreSQL

**Windows:**
- Download from https://www.postgresql.org/download/windows/
- Run installer, remember your password
- Ensure postgres service is running

**Mac:**
```bash
brew install postgresql
brew services start postgresql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 2. Create database and user

```bash
# Connect to PostgreSQL
psql -U postgres

# In psql prompt:
CREATE USER sqlgen WITH PASSWORD 'SecurePassword123!';
CREATE DATABASE business_db OWNER sqlgen;

# Create readonly role
CREATE ROLE sqlgen_readonly;
GRANT CONNECT ON DATABASE business_db TO sqlgen_readonly;
GRANT USAGE ON SCHEMA public TO sqlgen_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO sqlgen_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO sqlgen_readonly;

# Exit psql
\q
```

### 3. Initialize database schema

```bash
psql -U sqlgen -d business_db -f database/schema.sql
psql -U sqlgen -d business_db -f database/sample_data.sql
```

### 4. Install Ollama

**Windows/Mac:**
- Download from https://ollama.ai/download

**Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

### 5. Start Ollama and pull model

```bash
# In one terminal
ollama serve

# In another terminal
ollama pull mistral
```

### 6. Set up Python environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 7. Configure environment variables

```bash
cp .env.example .env

# Edit .env with your settings (if different from defaults)
# Important: Make sure POSTGRES_PASSWORD matches your setup
```

### 8. Run the application

```bash
python main.py
```

Access the application at http://localhost:5000

---

## Troubleshooting

### PostgreSQL Connection Issues

**Error: "FATAL: Ident authentication failed"**
- Edit PostgreSQL config: `sudo nano /etc/postgresql/*/main/pg_hba.conf`
- Change `ident` to `md5` for local connections
- Restart PostgreSQL: `sudo systemctl restart postgresql`

**Error: "FATAL: role 'sqlgen' does not exist"**
- Ensure you created the user as shown above
- Verify with: `psql -U postgres -l` (list databases)

### Ollama Issues

**Error: "No route to Ollama"**
- Ensure Ollama is running: `ollama serve`
- Check if it's listening on port 11434: `curl http://localhost:11434/api/tags`

**Error: Model not found**
- Pull the model: `ollama pull mistral`
- Check available models: `ollama list`

### Flask Issues

**Error: "Port 5000 already in use"**
```bash
# Find process using port 5000
lsof -i :5000  # On Linux/Mac
netstat -ano | findstr :5000  # On Windows

# Kill the process (replace PID with actual process ID)
kill -9 <PID>  # On Linux/Mac
taskkill /PID <PID> /F  # On Windows
```

**Error: "Module not found"**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Docker Issues

**Error: "Docker daemon is not running"**
- Start Docker Desktop (Windows/Mac)
- Or start service: `sudo systemctl start docker` (Linux)

**Error: "Compose version mismatch"**
```bash
# Update Docker Compose
docker-compose --version
# Should be 2.0+

# If using old version, upgrade:
pip install --upgrade docker-compose
```

---

## Verifying Installation

### 1. Check database connection
```bash
psql -U sqlgen -d business_db -c "SELECT COUNT(*) FROM users;"
```
Should return: 8

### 2. Check Ollama
```bash
curl http://localhost:11434/api/tags
```
Should show mistral model

### 3. Check Flask app
```bash
curl http://localhost:5000/api/health
```
Should return: `{"status": "healthy", "message": "..."}`

### 4. Test sample query via API
```bash
curl -X POST http://localhost:5000/api/query/generate \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me all users"}'
```

---

## Performance Tuning

### PostgreSQL
- Add indexes on frequently queried columns
- Increase `shared_buffers` for better performance
- Adjust `work_mem` based on available RAM

### Ollama
- Use smaller models (mistral ~7B) for faster responses
- Run on GPU if available for better performance
- Increase `OLLAMA_NUM_GPU` if using GPU

### Application
- Use caching for repeated questions
- Consider async query execution for long-running queries
- Monitor audit logs for optimization opportunities

---

## Security Considerations

### Before Production Deployment

1. **Change default passwords:**
   - PostgreSQL: Change `sqlgen` user password
   - Flask: Change `SECRET_KEY`

2. **Enable SSL/TLS:**
   - PostgreSQL: Enable SSL connections
   - Flask: Use HTTPS proxy

3. **Implement authentication:**
   - Add user authentication to Flask app
   - Implement API key authentication

4. **Restrict network access:**
   - Firewall: Only allow necessary ports
   - Database: Restrict to local network
   - API: Implement rate limiting

5. **Audit and logging:**
   - Enable PostgreSQL logging
   - Monitor audit_logs table regularly
   - Set up log rotation

---

## Next Steps

1. Read [README.md](README.md) for feature overview
2. Check [API_EXAMPLES.md](API_EXAMPLES.md) for API usage
3. Explore the sample data in the database
4. Try asking questions in the web UI

---

## Getting Help

- Check the logs: `tail -f logs/sql_generator.log`
- View Docker logs: `docker-compose logs -f app`
- Check PostgreSQL logs: `sudo tail -f /var/log/postgresql/postgresql.log`
- Review audit logs in the database: `SELECT * FROM audit_logs;`

---

For more information, see README.md
