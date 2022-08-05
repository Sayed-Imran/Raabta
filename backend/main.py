from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scripts.service.user_service import users_router
from scripts.service.login_service import user_cred
# from scripts.service.password_reset_service import passwd_reset
from scripts.service.post_service import posts_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.include_router(users_router)
app.include_router(user_cred,tags=["Register/Login"])
app.include_router(users_router, tags=["Users"])
# app.include_router(passwd_reset, tags=["Reset Password"])
app.include_router(posts_router,tags=["Posts"])
