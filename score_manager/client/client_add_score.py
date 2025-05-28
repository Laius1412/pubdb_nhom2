from client_base import ClientBase

# Nhập thông tin môn học
while True:
    subject = input("Nhập mã môn học: ").upper()
    if subject in ['A', 'B', 'C']:
        break
    print("❌ Môn học không hợp lệ. Vui lòng nhập A, B hoặc C.")

# Khởi tạo client
client = ClientBase(subject)

# Nhập thông tin sinh viên
print("\nNhập thông tin sinh viên:")
student_data = {
    "id": input("Mã số sinh viên: "),
    "name": input("Họ tên sinh viên: "),
    "cc1": float(input("Điểm chuyên cần 1: ")),
    "cc2": float(input("Điểm chuyên cần 2: ")),
    "midterm": float(input("Điểm giữa kỳ: ")),
    "final": float(input("Điểm cuối kỳ: "))
}

try:
    result = client.add_score(student_data)
    print(f"\n✅ Kết quả thêm điểm: {result}")
except Exception as e:
    print(f"\n❌ Lỗi: {str(e)}")
