#!/usr/bin/env python
# filepath: /Users/williamnguyen/Documents/william travel/backend/app/scripts/setup_database.py

"""
Script để thiết lập cơ sở dữ liệu và PostGIS extension.
Sử dụng: python -m app.scripts.setup_database
"""

import asyncio
import asyncpg
import sys

from app.core.config import settings


async def setup_database():
    """Thiết lập cơ sở dữ liệu và PostGIS extension."""
    
    # Trích xuất các thông tin kết nối từ cấu hình
    host = settings.POSTGRES_SERVER
    port = int(settings.POSTGRES_PORT)
    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD
    db_name = settings.POSTGRES_DB
    
    print(f"Đang kết nối đến PostgreSQL ({host}:{port}) với user '{user}'")
    
    try:
        # Kết nối tới server PostgreSQL (không phải database cụ thể)
        sys_conn = await asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database='postgres'  # Database mặc định cho kết nối hệ thống
        )
        
        # Kiểm tra xem database đã tồn tại chưa
        db_exists = await sys_conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1",
            db_name
        )
        
        if not db_exists:
            print(f"Database '{db_name}' không tồn tại. Đang tạo mới...")
            # Tạo database nếu chưa tồn tại
            await sys_conn.execute(f'CREATE DATABASE "{db_name}"')
            print(f"Đã tạo database '{db_name}' thành công.")
        else:
            print(f"Database '{db_name}' đã tồn tại.")
        
        # Đóng kết nối hệ thống
        await sys_conn.close()
        
        # Kết nối tới database vừa tạo
        conn = await asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name
        )
        
        # Kiểm tra PostGIS extension
        postgis_exists = await conn.fetchval(
            "SELECT 1 FROM pg_extension WHERE extname = 'postgis'"
        )
        
        if not postgis_exists:
            print("PostGIS extension chưa được cài đặt. Đang cài đặt...")
            # Tạo PostGIS extension
            await conn.execute('CREATE EXTENSION IF NOT EXISTS postgis')
            print("Đã cài đặt PostGIS extension thành công.")
        else:
            print("PostGIS extension đã được cài đặt.")
        
        # Hiển thị phiên bản PostGIS
        postgis_version = await conn.fetchval("SELECT PostGIS_version()")
        print(f"Phiên bản PostGIS: {postgis_version}")
        
        # Đóng kết nối
        await conn.close()
        
        print("===== Thiết lập cơ sở dữ liệu hoàn tất =====")
        return True
        
    except Exception as e:
        print(f"Lỗi khi thiết lập cơ sở dữ liệu: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(setup_database())
    sys.exit(0 if success else 1)
