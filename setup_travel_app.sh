#!/bin/bash
# filepath: /Users/williamnguyen/Documents/william travel/backend/setup_travel_app.sh

# Màu sắc cho output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== WILLIAM TRAVEL APP SETUP SCRIPT =====${NC}"
echo -e "${YELLOW}Script này sẽ thiết lập môi trường phát triển cho William Travel Backend${NC}"
echo ""

# Kiểm tra Docker đã cài đặt chưa
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker chưa được cài đặt. Vui lòng cài đặt Docker trước khi tiếp tục.${NC}"
    exit 1
fi

echo -e "${BLUE}Bước 1: Khởi chạy PostgreSQL với PostGIS trong Docker${NC}"

# Kiểm tra container PostgreSQL đã tồn tại chưa
if docker ps -a --format '{{.Names}}' | grep -q "postgres-postgis"; then
    echo -e "${YELLOW}Container postgres-postgis đã tồn tại.${NC}"
    
    # Kiểm tra container có đang chạy không
    if docker ps --format '{{.Names}}' | grep -q "postgres-postgis"; then
        echo -e "${GREEN}Container postgres-postgis đang chạy.${NC}"
    else
        echo -e "${YELLOW}Container postgres-postgis không chạy. Đang khởi động...${NC}"
        docker start postgres-postgis
        echo -e "${GREEN}Đã khởi động container postgres-postgis.${NC}"
    fi
else
    echo -e "${YELLOW}Đang tạo container PostgreSQL với PostGIS...${NC}"
    docker run --name postgres-postgis \
        -e POSTGRES_PASSWORD=postgres \
        -e POSTGRES_USER=postgres \
        -e POSTGRES_DB=travel \
        -p 5432:5432 \
        -d postgis/postgis:14-3.3
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Đã tạo và khởi động container PostgreSQL với PostGIS thành công.${NC}"
        
        # Đợi PostgreSQL khởi động
        echo -e "${YELLOW}Đang đợi PostgreSQL khởi động...${NC}"
        sleep 5
    else
        echo -e "${RED}Không thể tạo container PostgreSQL. Vui lòng kiểm tra lỗi và thử lại.${NC}"
        exit 1
    fi
fi

echo -e "${BLUE}Bước 2: Kiểm tra và thiết lập cơ sở dữ liệu${NC}"
echo -e "${YELLOW}Đang chạy script thiết lập cơ sở dữ liệu...${NC}"

# Chạy script Python để thiết lập database
cd "$(dirname "$0")"
poetry run python -m app.scripts.setup_database

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Thiết lập cơ sở dữ liệu thành công.${NC}"
else
    echo -e "${RED}Không thể thiết lập cơ sở dữ liệu. Vui lòng kiểm tra lỗi và thử lại.${NC}"
    exit 1
fi

echo -e "${BLUE}Bước 3: Chạy Alembic migrations${NC}"
echo -e "${YELLOW}Đang chạy database migrations...${NC}"

# Chạy migrations
poetry run alembic upgrade head

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Migrations thành công.${NC}"
else
    echo -e "${RED}Migrations thất bại. Có thể đã có bảng trong cơ sở dữ liệu.${NC}"
    
    read -p "Bạn có muốn khởi tạo lại cơ sở dữ liệu không? (y/n) " reset_db
    if [[ $reset_db == "y" || $reset_db == "Y" ]]; then
        echo -e "${YELLOW}Đang khởi tạo lại cơ sở dữ liệu...${NC}"
        
        # Kết nối vào PostgreSQL và xóa tất cả bảng
        docker exec -it postgres-postgis psql -U postgres -d travel -c "
        DO \$\$
        DECLARE
            r RECORD;
        BEGIN
            FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
            END LOOP;
        END
        \$\$;
        "
        
        # Chạy migrations lại
        echo -e "${YELLOW}Đang chạy migrations lại...${NC}"
        poetry run alembic upgrade head
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Migrations thành công sau khi khởi tạo lại.${NC}"
        else
            echo -e "${RED}Migrations vẫn thất bại. Vui lòng kiểm tra logs để biết thêm chi tiết.${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}Bỏ qua việc khởi tạo lại cơ sở dữ liệu.${NC}"
    fi
fi

echo -e "${BLUE}Bước 4: Tạo dữ liệu mẫu${NC}"
read -p "Bạn có muốn tạo dữ liệu mẫu không? (y/n) " seed_data
if [[ $seed_data == "y" || $seed_data == "Y" ]]; then
    echo -e "${YELLOW}Đang tạo dữ liệu mẫu...${NC}"
    poetry run python -m app.scripts.init_test_data
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Tạo dữ liệu mẫu thành công.${NC}"
    else
        echo -e "${RED}Không thể tạo dữ liệu mẫu. Vui lòng kiểm tra lỗi.${NC}"
    fi
else
    echo -e "${YELLOW}Bỏ qua việc tạo dữ liệu mẫu.${NC}"
fi

echo -e "${BLUE}Bước 5: Khởi động ứng dụng${NC}"
read -p "Bạn có muốn khởi động ứng dụng ngay bây giờ không? (y/n) " start_app
if [[ $start_app == "y" || $start_app == "Y" ]]; then
    echo -e "${YELLOW}Đang khởi động ứng dụng...${NC}"
    poetry run uvicorn app.main:app --reload
else
    echo -e "${YELLOW}Bỏ qua việc khởi động ứng dụng.${NC}"
    echo -e "${GREEN}Để khởi động ứng dụng sau này, hãy chạy lệnh:${NC}"
    echo -e "  ${BLUE}poetry run uvicorn app.main:app --reload${NC}"
fi

echo -e "${GREEN}===== THIẾT LẬP HOÀN TẤT =====${NC}"
echo -e "${YELLOW}Swagger UI:${NC} http://localhost:8000/docs"
echo -e "${YELLOW}ReDoc:${NC} http://localhost:8000/redoc"
