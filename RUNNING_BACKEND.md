# Running the FastAPI Backend

This guide will walk you through setting up and running the FastAPI backend, then testing it using Swagger documentation.

## Prerequisites

- Python 3.8+ installed
- PostgreSQL database running (see `env/GROUP_SETUP.md` for database setup)
- `.env` file configured (see `env/template.env`)

## Step 1: Set Up Python Virtual Environment

1. **Create a virtual environment** (if you haven't already):
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt):**
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Verify activation** - you should see `(venv)` in your terminal prompt.

## Step 2: Install Dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI
- Uvicorn (ASGI server to run FastAPI)
- SQLAlchemy (database ORM)
- psycopg2-binary (PostgreSQL driver)
- Pydantic (data validation)
- And other dependencies

## Step 3: Configure Environment Variables

1. **Copy the template environment file**:
   ```bash
   copy env\template.env .env
   ```
   (On Linux/Mac: `cp env/template.env .env`)

2. **Edit `.env` file** with your database credentials:
   ```env
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   DATABASE_NAME=your_database_name
   DATABASE_USER=your_username
   DATABASE_PASSWORD=your_password
   DATABASE_URL=postgresql://your_username:your_password@localhost:5432/your_database_name
   
   APP_HOST=127.0.0.1
   APP_PORT=8000
   ```

## Step 4: Verify Database Connection

Make sure your PostgreSQL database is running and accessible with the credentials in your `.env` file.

## Step 5: Run the FastAPI Server

1. **From the project root directory**, run:
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

   Or use the shorter version:
   ```bash
   uvicorn main:app --reload
   ```

   **Parameters explained:**
   - `main:app` - tells uvicorn to look for `app` in `main.py`
   - `--reload` - enables auto-reload on code changes (great for development!)
   - `--host 127.0.0.1` - makes it accessible on localhost
   - `--port 8000` - runs on port 8000

2. **You should see output like:**
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process [xxxxx] using WatchFiles
   INFO:     Started server process [xxxxx]
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

## Step 6: Access Swagger Documentation

FastAPI automatically generates interactive API documentation! You can access it in two ways:

### Option A: Swagger UI (Interactive)
Open your browser and go to:
```
http://127.0.0.1:8000/docs
```

This gives you an interactive interface where you can:
- See all available endpoints
- View request/response schemas
- **Test endpoints directly** - click "Try it out", fill in parameters, and click "Execute"
- See example requests and responses

### Option B: ReDoc (Alternative Documentation)
Open your browser and go to:
```
http://127.0.0.1:8000/redoc
```

This provides a cleaner, more readable documentation format (but not interactive like Swagger).

## Step 7: Testing Endpoints with Swagger

1. **Open Swagger UI**: Navigate to `http://127.0.0.1:8000/docs`

2. **Browse available endpoints**: You'll see all your API routes organized by tags (e.g., Members, Trainers, Admin)

3. **Test an endpoint**:
   - Click on an endpoint to expand it
   - Click the **"Try it out"** button
   - Fill in any required parameters or request body
   - Click **"Execute"**
   - View the response below (status code, response body, headers)

4. **Example workflow**:
   - GET `/health` or `/` - Simple test to see if server is running
   - POST `/members` - Create a new member
   - GET `/members/{id}` - Retrieve a member by ID
   - etc.

## Troubleshooting

### Port Already in Use
If you get an error about port 8000 being in use:
```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

### Module Not Found Error
Make sure:
- Your virtual environment is activated
- You've installed all dependencies (`pip install -r requirements.txt`)
- You're running from the project root directory

### Database Connection Error
- Verify PostgreSQL is running
- Check your `.env` file has correct credentials
- Test connection with: `psql -h localhost -U your_username -d your_database_name`

### Import Errors
If `main.py` doesn't have an `app` object yet, you'll need to create it. The file should have:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}
```

## Quick Commands Reference

```bash
# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload

# Run server on different port
uvicorn main:app --reload --port 8001

# Run server accessible from network (not just localhost)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Next Steps

- Build out your API endpoints in the `routers/` directory
- Register routers in `main.py`
- Add database models and repositories
- Test endpoints using Swagger UI

---

**Note**: If your `main.py` file is empty or incomplete, you'll need to set up the basic FastAPI app structure first. The server won't start without a valid FastAPI application instance.


