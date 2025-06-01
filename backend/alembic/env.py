import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import DATABASE_URL, Base
from app.models.models import (  # 모델 import
    SearchLocation,
    WeatherForecast,
    WeatherHistory,
)

# Alembic Config 객체 가져오기
config = context.config

# logging 설정 적용
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 메타데이터 객체 - 이것을 기반으로 마이그레이션이 생성됨
target_metadata = Base.metadata


def get_url():
    return DATABASE_URL


def run_migrations_offline() -> None:
    """오프라인 마이그레이션 실행"""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """온라인 마이그레이션 실행"""
    configuration = config.get_section(config.config_ini_section)
    if configuration is not None:
        configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
