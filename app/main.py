from fastapi import FastAPI
from app.api.endpoints import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from datetime import datetime
import uvicorn
from app.core.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Image Processing API",
        version="1.0.0",
        description="""
        This API provides endpoints for processing images and generating reports.

        Features:
        * Process images from local folder or Google Drive
        * Generate Excel reports with images and analysis
        * Generate PDF reports

        For more information, visit the /docs endpoint.
        """,
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Initialize FastAPI app
app = FastAPI(
    title="Image Processing API",
    description="API for processing images and generating Excel/PDF reports",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(router, prefix="/api/v1")

# Custom OpenAPI schema
app.openapi = custom_openapi

# Root route
@app.get("/",
         summary="Root endpoint",
         description="Returns basic information about the API")
async def root():
    logger.info("Root endpoint accessed")
    try:
        return JSONResponse(
            content={
                "message": "Welcome to the Image Processing API",
                "docs_url": "/docs",
                "redoc_url": "/redoc",
                "available_endpoints": {
                    "Process Images": "/api/v1/process-images",
                    "Health Check": "/health"
                },
                "version": "1.0.0"
            }
        )
    except Exception as e:
        logger.error(f"Error in root endpoint: {str(e)}")
        raise

# Health check endpoint
@app.get("/health",
         summary="Health check endpoint",
         description="Returns the current health status of the API")
async def health_check():
    logger.info("Health check endpoint accessed")
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "Image Processing API",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Error in health check endpoint: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# Error handler for generic exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "detail": str(exc)
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down")

if __name__ == "__main__":
    logger.info("Starting application")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)