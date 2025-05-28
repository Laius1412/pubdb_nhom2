from client_base import ClientBase

# Nhập thông tin môn học
while True:
    subject = input("Nhập mã môn học: ").upper()
    if subject in ['A', 'B', 'C']:
        break
    print("❌ Môn học không hợp lệ. Vui lòng nhập A, B hoặc C.")

# Khởi tạo client
client = ClientBase(subject)

# Nhập thông tin tìm kiếm
search_term = input("\nNhập mã số hoặc tên sinh viên cần tìm: ")

try:
    print(f"\n🔍 Kết quả tìm kiếm '{search_term}' trong môn {subject}:")
    results = client.get_student(search_term)
    
    if not results:
        print("❌ Không tìm thấy sinh viên")
    else:
        for student in results:
            print(f"\nThông tin sinh viên:")
            print(f"  - Mã số: {student.get('id')}")
            print(f"  - Họ tên: {student.get('name')}")
            print(f"  - Điểm chuyên cần 1: {student.get('cc1')}")
            print(f"  - Điểm chuyên cần 2: {student.get('cc2')}")
            print(f"  - Điểm giữa kỳ: {student.get('midterm')}")
            print(f"  - Điểm cuối kỳ: {student.get('final')}")
            print("---")
except Exception as e:
    print(f"\n❌ Lỗi: {str(e)}")
