import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.enum import UserRole
from app.auth.security import get_password_hash

from app.models.skills import Skill
from app.models.users import User

from app.seeds.data import (
    SKILLS,
    ADMIN,
    COMPANY,
    CANDIDATE,
)


async def seed_skills(db):

    for skill_name in SKILLS:

        result = await db.execute(select(Skill).where(Skill.name == skill_name ))

        if result.scalar_one_or_none() is None:
            db.add(Skill(name=skill_name))


async def seed_user(db,data,
    role: UserRole,
):

    result = await db.execute(
        select(User).where(
            User.email == data["email"]
        )
    )

    user = result.scalar_one_or_none()

    if user is None:

        user = User(
            email=data["email"],
            full_name=data["full_name"],
            password_hash=get_password_hash(
                data["password"]
            ),
            role=role,
        )

        db.add(user)

    else:
        user.role = role


async def main():

    async with AsyncSessionLocal() as db:

        # Skills
        await seed_skills(db)

        # Admin
        await seed_user(
            db,
            ADMIN,
            UserRole.ADMIN,
        )

        # Company
        await seed_user(
            db,
            COMPANY,
            UserRole.COMPANY,
        )

        # Candidate
        await seed_user(
            db,
            CANDIDATE,
            UserRole.CANDIDATE,
        )

        await db.commit()

        print("Seed completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())