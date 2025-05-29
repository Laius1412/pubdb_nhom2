# Score Manager with PupDB

## Giới thiệu

Score Manager là một ứng dụng quản lý điểm số được xây dựng trên nền tảng PupDB - một cơ sở dữ liệu key-value đơn giản và hiệu quả. Ứng dụng này được thiết kế để giúp quản lý và theo dõi điểm số một cách dễ dàng và hiệu quả.

## PupDB là gì?

PupDB là một cơ sở dữ liệu key-value đơn giản được viết bằng Python, với các đặc điểm nổi bật:

- Giao diện đơn giản như một Python dictionary
- Hỗ trợ đa luồng và đa tiến trình
- Giao diện REST API cho phép tích hợp với nhiều ngôn ngữ lập trình khác nhau
- Không yêu cầu cấu hình phức tạp
- Lý tưởng cho các ứng dụng có dữ liệu nhỏ và vừa

## Cài đặt và Thiết lập

### Yêu cầu hệ thống
- Python 3.6 trở lên
- pip (Python package manager)

### Cài đặt PupDB
```bash
pip install pupdb
```

### Cài đặt Score Manager
1. Clone repository:
```bash
git clone [repository-url]
cd score_manager
```

2. Cài đặt các dependencies:
```bash
pip install -r requirements.txt
```

## Cấu trúc dự án

```
score_manager/
├── client/         # Giao diện người dùng
├── database/       # Cấu hình và quản lý cơ sở dữ liệu
├── nodes/          # Các node xử lý dữ liệu
├── pupdb/          # Thư viện PupDB
├── config.py       # Cấu hình ứng dụng
└── requirements.txt # Danh sách dependencies
```

## Công nghệ và Kỹ thuật

### Công nghệ chính
   - Python 3.6+
   - PupDB (Cơ sở dữ liệu key-value)
   - Flask (Web framework)
## Chức năng chính

1. **Quản lý điểm số**
   - Thêm, sửa, xóa điểm số
   - Tìm kiếm và lọc điểm số
   - Xuất báo cáo điểm số

2. **Tính năng nâng cao**
   - Phân tích thống kê
   - Theo dõi tiến độ
   - Báo cáo tự động

3. **Bảo mật**
   - Xác thực người dùng
   - Phân quyền truy cập
   - Mã hóa dữ liệu

## Ứng dụng thực tế

Score Manager có thể được sử dụng trong nhiều môi trường khác nhau:

1. **Giáo dục**
   - Quản lý điểm số học sinh/sinh viên
   - Theo dõi tiến độ học tập
   - Tạo báo cáo học tập

2. **Thể thao**
   - Ghi nhận điểm số trận đấu
   - Thống kê thành tích
   - Xếp hạng vận động viên

3. **Doanh nghiệp**
   - Đánh giá hiệu suất nhân viên
   - Theo dõi KPI
   - Báo cáo hiệu suất

## Sử dụng PupDB trong Score Manager

Score Manager sử dụng PupDB để lưu trữ dữ liệu với các ưu điểm:

1. **Đơn giản trong sử dụng**
```python
from pupdb.core import PupDB

# Khởi tạo database
db = PupDB('scores.json')

# Lưu điểm số
db.set('student_001', {'math': 9.5, 'physics': 8.5})

# Lấy điểm số
scores = db.get('student_001')
```

2. **Hiệu suất cao**
   - Truy cập dữ liệu nhanh chóng
   - Hỗ trợ đa luồng
   - Tối ưu cho dữ liệu vừa và nhỏ

3. **Tích hợp REST API**
   - Dễ dàng tích hợp với các ứng dụng web
   - Hỗ trợ nhiều ngôn ngữ lập trình
   - API đơn giản và trực quan

## Đóng góp

Chúng tôi luôn hoan nghênh sự đóng góp từ cộng đồng. Nếu bạn muốn đóng góp, vui lòng:

1. Fork repository
2. Tạo branch mới cho tính năng của bạn
3. Commit các thay đổi
4. Push lên branch
5. Tạo Pull Request

## Giấy phép

Dự án này được cấp phép theo MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết. 
