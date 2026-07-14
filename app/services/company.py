from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company

from app.repositories import (
    company_repository,
    user_repository,
)

from app.schemas.company import (
    CreateCompany,
    UpdateCompany,
)

from app.exceptions import (
    ConflictError,
    NotFoundError,
)

from app.core.logger import logger


class CompanyService:

    def __init__(self,db: AsyncSession, ):
        self.db = db
        
    #=======================create_company===============

    async def create_company(
        self,
        user_id: int,
        company_data: CreateCompany,
    ) -> Company:

        user = await user_repository.get_by_id(user_id,self.db, )

        if user is None:
            logger.warning( f"Create company failed. User not found. user_id={user_id}")
            raise NotFoundError( "User not found")

        existing_company = await company_repository.get_by_owner_id(user_id,self.db, )

        if existing_company is not None:
            logger.warning( f"Create company failed. Company already exists. owner_id={user_id}" )
            raise ConflictError( "Company already exists")

        company = Company(
            owner_id=user_id,
            name=company_data.name,
            description=company_data.description,
            location=company_data.location,
            website_url=company_data.website_url,
            logo_url=company_data.logo_url,
        )

        created = await company_repository.create_company( company, self.db, )

        logger.info( f"Company created. owner_id={user_id}")

        return created
    #====================get_company===============
    async def get_company(self,user_id: int, ) -> Company:

        company = await company_repository.get_by_owner_id( user_id, self.db,)

        if company is None:
            logger.warning( f"Get company failed. Company not found. owner_id={user_id}")
            raise NotFoundError("Company not found")

        return company
    
    #=================update_company================

    async def update_company( self,user_id: int,company_data: UpdateCompany, ) -> Company:

        company = await self.get_company( user_id)

        update_data = company_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if not update_data:
            logger.warning( f"Update company skipped. No fields provided. owner_id={user_id}" )
            return company

        updated = await company_repository.update_company(
            company,
            self.db,
            update_data,
        )

        logger.info( f"Company updated. owner_id={user_id}" )

        return updated
    #==================delete_company===============

    async def delete_company( self, user_id: int, ) -> None:

        company = await self.get_company( user_id)

        await company_repository.delete_company(company, self.db,)

        logger.info(  f"Company deleted. owner_id={user_id}")