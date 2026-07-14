from fastapi import FastAPI

import app.models

from app.routers import (auth, user,profile,company,application,
education,experience,job,skills,user_skill
)
from app.core.exception_handler import global_exception_handler
from app.routers import admin

app = FastAPI(
    title="TalentFlow Backend",
    description="API for TalentFlow Management System",
    version="1.0.0",
)


app.add_exception_handler(Exception, global_exception_handler,)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(profile.router)
app.include_router(company.router)
app.include_router(application.router)
app.include_router(job.router)
app.include_router(skills.router)
app.include_router(user_skill.router)
app.include_router(education.router)
app.include_router(experience.router)
app.include_router(admin.router)



