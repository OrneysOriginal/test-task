from datetime import datetime
from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from analytics.schemas import SCalculateInterval, SCalculateAllTime, SStats, SOnNameAllDevice, SOnNameOneDevice
from database import get_async_session
from user.models import DeviceORM, UserOrm

analytics_router = APIRouter(
    prefix='/analytics',
    tags=['analytics'],
)


@analytics_router.post('/on_name_one_device')
async def stat_on_username_device(data: SOnNameOneDevice, session: AsyncSession = Depends(get_async_session)) -> dict:
    user = await get_user(session, data.username)
    if user is None:
        return {'status_code': 404, 'info': 'user not found'}
    query = select(DeviceORM).filter((DeviceORM.user == user.id) & (DeviceORM.device_name == data.device_name))

    return await calculate_statistic(session, query)


@analytics_router.post('/on_username_all_device')
async def stat_on_username_all_device(data: SOnNameAllDevice, session: AsyncSession = Depends(get_async_session)) -> dict:
    user = await get_user(session, data.username)
    if user is None:
        return {'status_code': 404, 'info': 'user not found'}

    query = select(DeviceORM).filter(DeviceORM.user == user.id)
    return await calculate_statistic(session, query)


@analytics_router.post('/all_time')
async def stat_all_time(data: SCalculateAllTime, session: AsyncSession = Depends(get_async_session)) -> dict:
    query = select(DeviceORM).filter(DeviceORM.device_name == data.device_name)
    return await calculate_statistic(session, query)


@analytics_router.post('/interval')
async def stat_interval(data: SCalculateInterval, session: AsyncSession = Depends(get_async_session)) -> dict:
    query = select(DeviceORM).filter(
        (data.device_name == DeviceORM.device_name) &
        (data.start <= DeviceORM.created_at) &
        (data.end >= DeviceORM.created_at)
    )
    return await calculate_statistic(session, query)


@analytics_router.post('/add_elements')
async def add_statistics(data: SStats, session: AsyncSession = Depends(get_async_session)) -> dict:
    data = data.model_dump()
    data['created_at'] = datetime.now()

    if data.get('user') is not None:
        user = await get_user(session, data['user'])
        if user is None:
            return {'status_code': 404, 'info': 'user not found'}
        data['user'] = user.id

    stat = DeviceORM(**data)
    session.add(stat)
    await session.commit()
    await session.refresh(stat)
    return {'status_code': 200}


async def get_user(session: AsyncSession, username: str) -> UserOrm | None:
    query = select(UserOrm).filter(UserOrm.username == username)
    data = await session.execute(query)
    user = data.first()
    if user is None:
        return None
    user = user[0]
    return user


async def calculate_statistic(session: AsyncSession, query: Select) -> dict:
    result = await session.execute(query)
    result = list(result.scalars().all())
    if len(result) == 0:
        return {'status_code': 200, 'info': 'is empty'}
    data = sorted(get_x_y_z(result))
    return calculate_stat(data)


def get_x_y_z(result: Sequence) -> list:
    x_values = [0] * len(result)
    y_values = [0] * len(result)
    z_values = [0] * len(result)
    for i in range(len(result)):
        x_values[i] = result[i].x
        y_values[i] = result[i].y
        z_values[i] = result[i].z
    return x_values + y_values + z_values


def calculate_stat(data: list) -> dict:
    min_v = data[0]
    max_v = data[-1]
    count_nums = len(data)
    sum_nums = sum(data)
    if count_nums % 2 == 0:
        median = (data[count_nums // 2] + data[count_nums // 2 - 1]) / 2
    else:
        median = data[count_nums // 2]
    return {
        'min_v': min_v,
        'max_v': max_v,
        'count_nums': count_nums,
        'sum_nums': sum_nums,
        'median': median,
    }
