from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.routers.auth import router, get_current_user
from app.routers.library import library_router
from app.session import get_session, engine, Base

app = FastAPI(title="Library")

Base.metadata.create_all(bind=engine)

app.include_router(router)
app.include_router(library_router)

db_dependency = Annotated[Session, Depends(get_session)]
user_dependency = Annotated[dict, Depends(get_current_user)]
@app.get("/")
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    return {"User": user}