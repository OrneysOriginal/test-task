from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from user.models import UserOrm
from user.schemas import SRegister

user_router = APIRouter(
    prefix='/user',
    tags=['User']
)


@user_router.post('/register')
async def register(data: SRegister, session: AsyncSession = Depends(get_async_session)) -> dict:
    data = data.model_dump()
    user = UserOrm(**data)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {'status_code': 200}
