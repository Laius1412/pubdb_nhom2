from client_base import ClientBase

# Nhập thông tin môn học
while True:
    subject = input("Nhập mã môn học: ").upper()
    if subject in ['A', 'B', 'C']:
        break
    print("❌ Môn học không hợp lệ. Vui lòng nhập A, B hoặc C.")

# Khởi tạo client
client = ClientBase(subject)

try:
    print(f"\n📋 Danh sách sinh viên môn {subject}:")
    students = client.get_all()
    
    if not students:
        print("❌ Không có dữ liệu sinh viên")
    else:
        for student_id, student_data in students.items():
            print(f"\nID: {student_id}")
            print(f"Thông tin: {student_data}")
            print("---")
except Exception as e:
    print(f"\n❌ Lỗi: {str(e)}")
