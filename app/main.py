from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
import time

from app.core.config import settings
from app.core.logger import logger, log_request
from app.core.database import db_manager
from app.routes import schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("=" * 50)
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info("=" * 50)
    
    # Test database connection
    if db_manager.test_connection():
        logger.info("✓ Database connection successful")
    else:
        logger.error("✗ Database connection failed")
        raise RuntimeError("Failed to connect to database")
    
    # Log database statistics
    try:
        from app.repo import get_bank_repo, get_branch_repo
        bank_count = get_bank_repo().count_banks()
        branch_count = get_branch_repo().count_branches()
        logger.info(f"✓ Database contains {bank_count} banks and {branch_count} branches")
    except Exception as e:
        logger.warning(f"Could not fetch database statistics: {e}")
    
    logger.info(f"✓ GraphQL endpoint: {settings.GRAPHQL_ENDPOINT}")
    logger.info(f"✓ Debug mode: {settings.DEBUG}")
    logger.info(f"✓ API Key protection: {settings.API_KEY_ENABLED}")
    logger.info("Application ready to accept requests")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    logger.info("=" * 50)


# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="GraphQL API for querying Indian bank branches data",
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# Middleware for logging requests
@app.middleware("http")
async def log_requests(request, call_next):
    """Log all incoming requests"""
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    log_request(
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration=duration
    )
    
    return response


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    Returns application status and database connectivity
    """
    db_status = db_manager.test_connection()
    
    return {
        "status": "healthy" if db_status else "unhealthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "connected" if db_status else "disconnected",
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint
    Returns basic API information
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "graphql_endpoint": settings.GRAPHQL_ENDPOINT,
        "docs": "/docs",
        "health": "/health",
    }


# GraphQL Router
logger.info("Initializing GraphQL router...")
graphql_app = GraphQLRouter(
    schema,
    graphiql=settings.DEBUG,  # Enable GraphiQL interface in debug mode
)
app.include_router(graphql_app, prefix=settings.GRAPHQL_ENDPOINT)
logger.info(f"✓ GraphQL router mounted at {settings.GRAPHQL_ENDPOINT}")


# API Stats endpoint
@app.get("/stats", tags=["Stats"])
async def api_stats():
    """
    Get API statistics
    Returns counts of banks and branches
    """
    logger.info("Fetching API statistics")
    try:
        from app.repo import get_bank_repo, get_branch_repo
        
        bank_count = get_bank_repo().count_banks()
        branch_count = get_branch_repo().count_branches()
        
        stats = {
            "banks": bank_count,
            "branches": branch_count,
            "graphql_endpoint": settings.GRAPHQL_ENDPOINT,
            "api_version": settings.APP_VERSION,
        }
        
        logger.info(f"Stats retrieved: {stats}")
        return stats
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        return {
            "error": "Failed to fetch statistics",
            "banks": 0,
            "branches": 0,
        }


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )
