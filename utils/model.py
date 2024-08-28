from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from utils.abstractions.models import SQLAlchemyModel


async def create_model_instance(
        *,
        db: AsyncSession,
        instance: SQLAlchemyModel,
        validated_data: dict
) -> SQLAlchemyModel:
    instance = instance(
        **validated_data
    )
    db.add(instance)
    await db.commit()
    return instance


async def get_or_create(
        *,
        db: AsyncSession,
        model: SQLAlchemyModel,
        save: bool = True,
        validated_data: dict
) -> tuple[SQLAlchemyModel, bool]:
    result = await db.execute(
        select(model).filter_by(id=validated_data.get('id'))
    )
    instance = result.scalar_one_or_none()
    if instance:
        return instance, False
    else:
        instance = model(**validated_data)
        db.add(instance)
        if save:
            try:
                await db.commit()
                await db.refresh(instance)
            except IntegrityError:
                await db.rollback()
                result = await db.execute(
                    select(model).filter_by(**validated_data)
                )
                instance = result.scalar_one()
                return instance, False
        return instance, True
