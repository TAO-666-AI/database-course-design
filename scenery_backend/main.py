from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import CORS_ORIGINS, DB_NAME
from db.init_db import init_database
from routers.admin import chats as admin_chats
from routers.admin import faqs as admin_faqs
from routers.admin import feedbacks as admin_feedbacks
from routers.admin import routes as admin_routes
from routers.admin import spots as admin_spots
from routers.admin import users as admin_users
from routers.tourist import auth, chat, faqs, favorites, feedback, routes, spots


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield


app = FastAPI(title="景区导览管理系统后端", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(spots.router)
app.include_router(routes.router)
app.include_router(favorites.router)
app.include_router(feedback.router)
app.include_router(faqs.router)
app.include_router(chat.router)
app.include_router(admin_users.router)
app.include_router(admin_spots.router)
app.include_router(admin_routes.router)
app.include_router(admin_faqs.router)
app.include_router(admin_feedbacks.router)
app.include_router(admin_chats.router)


@app.get("/")
def root():
    return {"name": "景区导览管理系统后端", "database": DB_NAME, "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
