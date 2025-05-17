# Công Nghệ Sử Dụng Trong Dự Án

## Tổng Quan

Dự án William Travel Backend được xây dựng trên một stack công nghệ hiện đại, sử dụng Python làm ngôn ngữ chính và một loạt công nghệ đi kèm để xây dựng một API hiệu suất cao, có khả năng mở rộng và bảo mật. Tài liệu này mô tả chi tiết các công nghệ được sử dụng và vai trò của chúng trong dự án.

## Công Nghệ Chính

### Python
**Vai trò**: Ngôn ngữ lập trình chính của dự án.  
**Công dụng**: Python được chọn vì sự đơn giản, dễ đọc và có hệ sinh thái thư viện phong phú phù hợp cho việc phát triển backend. Phiên bản sử dụng là Python 3.12, tận dụng các tính năng mới nhất của ngôn ngữ.

### FastAPI
**Vai trò**: Web Framework chính.  
**Công dụng**: FastAPI là framework API hiện đại với hiệu suất cao, dựa trên tiêu chuẩn ASGI. Nó cung cấp:
- Hiệu suất cao nhờ tính năng bất đồng bộ (asynchronous) native
- Hệ thống validation dữ liệu tự động thông qua Pydantic
- Tạo tài liệu API tự động (OpenAPI + Swagger UI)
- Dependency injection đơn giản và mạnh mẽ

### SQLAlchemy
**Vai trò**: ORM (Object-Relational Mapping).  
**Công dụng**: SQLAlchemy cung cấp một cách trừu tượng hóa để làm việc với cơ sở dữ liệu:
- Hỗ trợ bất đồng bộ (asyncio) thông qua sqlalchemy.ext.asyncio
- Định nghĩa cấu trúc cơ sở dữ liệu với các model Python
- Query builder linh hoạt
- Hỗ trợ nhiều RDBMS khác nhau (PostgreSQL, MySQL, SQLite...)

### Alembic
**Vai trò**: Công cụ quản lý migration cơ sở dữ liệu.  
**Công dụng**: Alembic giúp theo dõi, áp dụng và hoàn tác các thay đổi schema cơ sở dữ liệu:
- Tạo các phiên bản (version) cơ sở dữ liệu
- Hỗ trợ migration tự động dựa trên sự thay đổi model
- Tính năng rollback để hoàn tác các thay đổi
- Tích hợp tốt với SQLAlchemy

### GeoAlchemy2
**Vai trò**: Mở rộng SQLAlchemy cho dữ liệu không gian địa lý.  
**Công dụng**: GeoAlchemy2 cung cấp các kiểu dữ liệu không gian địa lý và các hàm để làm việc với dữ liệu đó:
- Hỗ trợ các kiểu dữ liệu PostGIS như Point, LineString, Polygon
- Hỗ trợ các truy vấn không gian (spatial queries)
- Cần thiết cho việc lưu trữ và tìm kiếm vị trí địa lý trong dự án du lịch

### PostgreSQL
**Vai trò**: Hệ quản trị cơ sở dữ liệu quan hệ.  
**Công dụng**: PostgreSQL được chọn vì:
- Hỗ trợ mạnh mẽ cho dữ liệu không gian địa lý thông qua PostGIS
- Độ tin cậy và hiệu suất cao
- Khả năng mở rộng tốt
- Tuân thủ ACID cho tính toàn vẹn dữ liệu

### Poetry
**Vai trò**: Công cụ quản lý gói và môi trường ảo.  
**Công dụng**: Poetry giúp quản lý dependencies và môi trường phát triển:
- Quản lý phiên bản dependency chính xác thông qua pyproject.toml và poetry.lock
- Tạo và quản lý môi trường ảo (virtual environment)
- Đơn giản hóa việc cài đặt và build package

## Các Thư Viện và Công Cụ Hỗ Trợ

### Pydantic
**Vai trò**: Thư viện validation dữ liệu và serialization.  
**Công dụng**: Pydantic được sử dụng để:
- Định nghĩa schema cho request/response
- Validation dữ liệu tự động
- Chuyển đổi giữa định dạng dữ liệu (serialization/deserialization)
- Tạo tài liệu API tự động khi kết hợp với FastAPI

### Passlib + Python-jose
**Vai trò**: Bảo mật và xác thực.  
**Công dụng**:
- Passlib được sử dụng để mã hóa và xác thực mật khẩu
- Python-jose cung cấp hỗ trợ cho JWT (JSON Web Tokens) dùng trong xác thực người dùng
- Bảo vệ endpoints API yêu cầu đăng nhập

### Pytest
**Vai trò**: Framework kiểm thử.  
**Công dụng**: Pytest được sử dụng để viết và chạy các bài kiểm thử:
- Unit tests cho các thành phần riêng lẻ
- Integration tests cho API endpoints
- Fixture để thiết lập môi trường kiểm thử

## Cấu Trúc Dự Án

Dự án được tổ chức theo mô hình phân lớp rõ ràng:

### Lớp API (app/api)
Chứa các router và endpoint API, phân chia theo phiên bản (v1) và các module chức năng.

### Lớp Core (app/core)
Chứa các thành phần cốt lõi như cấu hình ứng dụng, bảo mật và các hằng số.

### Lớp CRUD (app/crud)
Chứa các hàm thao tác với cơ sở dữ liệu theo mô hình CRUD (Create, Read, Update, Delete).

### Lớp DB (app/db)
Chứa các model SQLAlchemy, kết nối cơ sở dữ liệu và các hàm tiện ích liên quan đến DB.

### Lớp Schemas (app/schemas)
Chứa các Pydantic model cho request/response API.

### Lớp Services (app/services)
Chứa các dịch vụ bên ngoài như email, thanh toán, hoặc các dịch vụ tích hợp bên thứ ba.

### Lớp Scripts (app/scripts)
Chứa các script tiện ích như khởi tạo dữ liệu mẫu, thiết lập cơ sở dữ liệu.

## Tính Năng Chính của Dự Án

Dự án William Travel Backend tập trung vào các tính năng sau:

1. **Quản lý người dùng và xác thực**:
   - Đăng ký, đăng nhập, quên mật khẩu
   - Phân quyền (user, admin)
   - JWT authentication

2. **Quản lý địa điểm du lịch**:
   - Phân cấp địa lý (quốc gia > vùng > quận/huyện > phường/xã)
   - Lưu trữ thông tin chi tiết địa điểm với dữ liệu không gian địa lý
   - Phân loại địa điểm theo danh mục

3. **Đánh giá và bình luận**:
   - Người dùng có thể đánh giá và để lại bình luận cho địa điểm
   - Tính điểm trung bình và sắp xếp theo mức độ phổ biến

4. **Tìm kiếm không gian địa lý**:
   - Tìm kiếm địa điểm theo vị trí hiện tại
   - Lọc theo khoảng cách, danh mục, tiện ích...

## Kết Luận

William Travel Backend sử dụng một stack công nghệ hiện đại, tập trung vào hiệu suất và khả năng mở rộng. Cấu trúc dự án được thiết kế theo các nguyên tắc phân tách mối quan tâm (separation of concerns) để dễ dàng bảo trì và phát triển trong tương lai.

Việc sử dụng các công nghệ như FastAPI, SQLAlchemy Async, GeoAlchemy2 và PostgreSQL/PostGIS cung cấp một nền tảng vững chắc để xây dựng các tính năng ứng dụng du lịch phức tạp với hiệu suất cao.
