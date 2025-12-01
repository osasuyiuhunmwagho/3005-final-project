"""
Database connection and session management.
Handles database initialization, connection pooling, and session creation.
Central point for all database interactions in the application.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create database engine with better error handling
try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using them
        echo=settings.DEBUG,  # Log SQL queries in debug mode
        connect_args={"connect_timeout": 10}  # 10 second timeout
    )
    logger.info(f"Database engine created for: {settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()

# Dependency to get database session
def get_db():
    """
    Dependency function that yields a database session.
    Used with FastAPI's Depends() to inject database sessions into route handlers.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# Function to create all tables (useful for initialization)
def create_tables():
    """Create all tables defined in models."""
    Base.metadata.create_all(bind=engine)

# Function to drop all tables (useful for testing/reset)
def drop_tables():
    """Drop all tables."""
    Base.metadata.drop_all(bind=engine)
