
from fastapi import FastAPI

from services.document_service.app.api.ingestion import router

app = FastAPI(
    title="Intelligent Document Processing - Document Service",
    description="Document ingestion and processing APIs",
    version="0.1.0"
)


@app.get("/health")
def health_check():

    return {
        "service": "document_service",
        "status": "healthy"
    }


app.include_router(router)
