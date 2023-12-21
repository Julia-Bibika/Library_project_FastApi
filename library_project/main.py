from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from routers.router import router
# from routers.auth import auth_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/ORM")
# app.include_router(auth_router, prefix='/api/auth', tags=['Auth'])

@app.get("/")
async def root():
    return RedirectResponse(url='/docs')


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}