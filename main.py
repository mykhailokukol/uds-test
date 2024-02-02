from fastapi import FastAPI

from endpoints.file_storage import router as fs_router


app = FastAPI(
    openapi_url="/api/",
    docs_url="/api/docs/",
    redoc_url="/api/redoc/",
    title="Test Task",
    description="Test task for UkrenergoDigitalSolutions from Mykhailo Kukol",
    version="0.1",
)

app.include_router(fs_router, prefix="")
