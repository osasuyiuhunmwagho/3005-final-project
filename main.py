"""
Main application entry point.
Initializes the FastAPI/Flask application, registers routes, sets up database connection, and starts the server.
Coordinates all application components and serves as the entry point for running the app.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import models to ensure they're registered with SQLAlchemy Base
import app.model  # This imports all models from app.model/__init__.py

# Import database utilities
from app.core.database import Base, engine, create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup: Create tables if they don't exist
    # This will only run when the app actually starts, not at import time
    try:
        create_tables()
    except Exception as e:
        # Log error but don't crash - allows app to start even if DB is not ready
        print(f"Warning: Could not create tables on startup: {e}")
        print("Tables may need to be created manually or database connection may need to be configured.")
    yield
    # Shutdown: Add any cleanup code here if needed

# Create FastAPI app instance
app = FastAPI(
    title="Fitness Center Management API",
    description="API for managing fitness center operations",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    from app.core.database import engine
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# Register routers
from app.routers import trainer_routes, admin_routes, member_routes

# Trainer routes
app.include_router(trainer_routes.router, prefix="/api")

# Admin routes  
app.include_router(admin_routes.router, prefix="/api")

# Member routes
app.include_router(member_routes.router, prefix="/api")