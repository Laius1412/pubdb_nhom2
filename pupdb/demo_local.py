from pupdb.core import PupDB

# Tạo đối tượng cơ sở dữ liệu (dùng file db.json)
db = PupDB('db.json')

# Ghi dữ liệu vào file db.json
db.set('name', 'LapTrinhAI')
db.set('email', 'laptrinh@example.com')

# Đọc dữ liệu
print("Tên:", db.get('name'))
print("Email:", db.get('email'))

# Hiển thị toàn bộ key, value
print("Keys:", list(db.keys()))
print("Values:", list(db.values()))
print("Items:", list(db.items()))

# Xóa một key
db.remove('name')

# In nội dung DB ở dạng JSON
print("Dumps:", db.dumps())

# Xóa toàn bộ dữ liệu
db.truncate_db()

# In lại nội dung sau khi xóa
print("Sau khi truncate:", db.dumps())
