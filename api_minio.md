# MinIO File Management API Documentation

API này cung cấp các endpoints để quản lý files thông qua MinIO, hỗ trợ các thao tác như upload, download, liệt kê và xóa files.

## Base URL

```
http://localhost:8000
```

## Tổng quan các Endpoints

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/` | GET | Trang chủ API |
| `/health` | GET | Kiểm tra trạng thái hoạt động |
| `/buckets` | GET | Liệt kê tất cả buckets |
| `/buckets/{bucket_name}` | POST | Tạo bucket mới |
| `/upload` | POST | Upload file thông thường |
| `/upload-base64` | POST | Upload ảnh dạng base64 |
| `/download/{bucket_name}/{object_name}` | GET | Download file từ MinIO |
| `/files/{bucket_name}` | GET | Liệt kê files trong bucket |
| `/delete/{bucket_name}/{object_name}` | DELETE | Xóa file khỏi MinIO |
| `/info/{bucket_name}/{object_name}` | GET | Lấy thông tin file |
| `/presigned-url/{bucket_name}/{object_name}` | GET | Tạo URL có thời hạn để truy cập file |

## Chi tiết các Endpoints

### Trang chủ API

```
GET /
```

**Mô tả**: Hiển thị thông tin tổng quan về API

**Response**:
```json
{
  "message": "MinIO File Management API",
  "version": "1.0.0",
  "endpoints": {
    "buckets": "/buckets",
    "upload": "/upload",
    "download": "/download/{bucket_name}/{object_name}",
    "files": "/files/{bucket_name}",
    "delete": "/delete/{bucket_name}/{object_name}"
  }
}
```

### Kiểm tra trạng thái hoạt động

```
GET /health
```

**Mô tả**: Kiểm tra xem API và kết nối MinIO có hoạt động bình thường không

**Response thành công**:
```json
{
  "status": "healthy",
  "timestamp": "2025-05-29T15:30:45.123456",
  "minio_connected": true,
  "buckets_count": 3
}
```

**Response lỗi**:
```json
{
  "status": "unhealthy",
  "timestamp": "2025-05-29T15:30:45.123456",
  "minio_connected": false,
  "error": "Unable to connect to MinIO server"
}
```

### Liệt kê tất cả buckets

```
GET /buckets
```

**Mô tả**: Lấy danh sách tất cả buckets hiện có trong MinIO

**Response**:
```json
{
  "buckets": ["images", "documents", "videos"],
  "count": 3
}
```

### Tạo bucket mới

```
POST /buckets/{bucket_name}
```

**Mô tả**: Tạo một bucket mới trong MinIO

**Parameters**:
- `bucket_name` (path): Tên của bucket cần tạo

**Response thành công**:
```json
{
  "message": "Bucket 'new-bucket' được tạo thành công"
}
```

**Response lỗi**:
```json
{
  "detail": "Không thể tạo bucket"
}
```

### Upload file thông thường

```
POST /upload
```

**Mô tả**: Upload file thông thường lên MinIO

**Content-Type**: `multipart/form-data`

**Parameters**:
- `bucket_name` (form): Tên bucket để lưu file
- `file` (form): File cần upload

**Response thành công**:
```json
{
  "message": "Upload thành công",
  "bucket": "images",
  "object_name": "20250529_153045_example.jpg",
  "original_filename": "example.jpg",
  "size": 1048576,
  "content_type": "image/jpeg"
}
```

**Response lỗi**:
```json
{
  "detail": "Upload thất bại"
}
```

### Upload ảnh dạng base64

```
POST /upload-base64
```

**Mô tả**: Upload ảnh dạng base64 lên MinIO

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "bucket_name": "images",
  "file_name": "example.jpg",
  "base64_data": "iVBORw0KGgoAAAANSUhEUgAA...",
  "content_type": "image/jpeg"
}
```

**Chú ý**: `base64_data` có thể chứa prefix như `data:image/jpeg;base64,`, hệ thống sẽ tự động xử lý và loại bỏ prefix này.

**Response thành công**:
```json
{
  "message": "Upload base64 image thành công",
  "bucket": "images",
  "object_name": "20250529_153045_example.jpg",
  "original_filename": "example.jpg",
  "content_type": "image/jpeg"
}
```

**Response lỗi**:
```json
{
  "detail": "Upload base64 image thất bại"
}
```

### Download file từ MinIO

```
GET /download/{bucket_name}/{object_name}
```

**Mô tả**: Download file từ MinIO

**Parameters**:
- `bucket_name` (path): Tên bucket chứa file
- `object_name` (path): Tên object cần download

**Response**: 
- Thành công: File được download về máy client
- Lỗi:
```json
{
  "detail": "File không tồn tại"
}
```

### Liệt kê files trong bucket

```
GET /files/{bucket_name}
```

**Mô tả**: Liệt kê tất cả files trong một bucket

**Parameters**:
- `bucket_name` (path): Tên bucket cần liệt kê files
- `prefix` (query, optional): Tiền tố để lọc files

**Response**:
```json
{
  "bucket": "images",
  "prefix": "profile/",
  "objects": [
    {
      "name": "profile/user1.jpg",
      "size": 1048576,
      "last_modified": "2025-05-29T15:30:45.123456",
      "etag": "abcdef1234567890"
    },
    {
      "name": "profile/user2.jpg",
      "size": 2097152,
      "last_modified": "2025-05-28T12:15:30.456789",
      "etag": "0987654321fedcba"
    }
  ],
  "count": 2
}
```

### Xóa file khỏi MinIO

```
DELETE /delete/{bucket_name}/{object_name}
```

**Mô tả**: Xóa một file từ MinIO

**Parameters**:
- `bucket_name` (path): Tên bucket chứa file
- `object_name` (path): Tên object cần xóa

**Response thành công**:
```json
{
  "message": "Xóa thành công: images/example.jpg"
}
```

**Response lỗi**:
```json
{
  "detail": "Xóa thất bại"
}
```

### Lấy thông tin file

```
GET /info/{bucket_name}/{object_name}
```

**Mô tả**: Lấy thông tin chi tiết về một file trong MinIO

**Parameters**:
- `bucket_name` (path): Tên bucket chứa file
- `object_name` (path): Tên object cần lấy thông tin

**Response thành công**:
```json
{
  "name": "example.jpg",
  "size": 1048576,
  "last_modified": "2025-05-29T15:30:45.123456",
  "etag": "abcdef1234567890",
  "content_type": "image/jpeg"
}
```

**Response lỗi**:
```json
{
  "detail": "File không tồn tại"
}
```

### Tạo URL có thời hạn để truy cập file

```
GET /presigned-url/{bucket_name}/{object_name}
```

**Mô tả**: Tạo một URL có thời hạn để truy cập file, không cần xác thực

**Parameters**:
- `bucket_name` (path): Tên bucket chứa file
- `object_name` (path): Tên object cần tạo URL
- `expires_hours` (query, optional): Thời hạn URL tính bằng giờ, mặc định là 1 giờ

**Response thành công**:
```json
{
  "url": "http://localhost:9000/images/example.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...",
  "expires_in_hours": 1,
  "bucket": "images",
  "object": "example.jpg"
}
```

**Response lỗi**:
```json
{
  "detail": "Không thể tạo URL"
}
```

## Ví dụ sử dụng

### Upload file thông thường

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "bucket_name=images" \
  -F "file=@/path/to/local/image.jpg"
```

### Upload ảnh base64

```bash
curl -X POST "http://localhost:8000/upload-base64" \
  -H "Content-Type: application/json" \
  -d '{
    "bucket_name": "images",
    "file_name": "example.jpg",
    "base64_data": "iVBORw0KGgoAAAANSUhEUgAA...",
    "content_type": "image/jpeg"
  }'
```

### Download file

```bash
curl -X GET "http://localhost:8000/download/images/20250529_153045_example.jpg" --output downloaded_file.jpg
```

### Lấy presigned URL

```bash
curl -X GET "http://localhost:8000/presigned-url/images/20250529_153045_example.jpg?expires_hours=2"
```
