from fastapi import FastAPI


app = FastAPI(
    openapi_url="/api/",
    docs_url="/api/docs/",
    redoc_url="api/redoc/",
    title="Test Task",
    description="Test task for UkrenergoDigitalSolutions from Mykhailo Kukol",
    version="0.1",
)
