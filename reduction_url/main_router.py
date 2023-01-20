from fastapi import FastAPI

from reduction_url.api.operations import router as router_operations
from reduction_url.api.auth import router as router_auth
app = FastAPI()

app.include_router(router_operations)
app.include_router(router_auth)
