"""
Main application entry point.
Initializes the FastAPI/Flask application, registers routes, sets up database connection, and starts the server.
Coordinates all application components and serves as the entry point for running the app.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

# Import models to ensure they're registered with SQLAlchemy Base
import model  # This imports all models from model/__init__.py

# Import database utilities
from core.database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup: Create tables if they don't exist
    # Uncomment the line below if you want tables created automatically on startup
    # create_tables()
    yield
    # Shutdown: Add any cleanup code here if needed

# Create FastAPI app instance
app = FastAPI(
    title="Fitness Center Management API",
    description="API for managing fitness center operations",
    version="1.0.0",
    lifespan=lifespan
)

# Health check endpoint
@app.get("/")
def root():
    """Root endpoint - returns API information"""
    return {
        "message": "Fitness Center Management API",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/health/db")
def health_check_db():
    """Database health check endpoint"""
    from core.database import engine
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# Register routers
from routers import trainer_routes, admin_routes, member_routes

# Trainer routes
app.include_router(trainer_routes.router, prefix="/api")

# Admin routes  
app.include_router(admin_routes.router, prefix="/api")

# Member routes
app.include_router(member_routes.router, prefix="/api")