from client_base import ClientBase

if __name__ == "__main__":
    # Nhập thông tin môn học
    while True:
        subject = input("Nhập mã môn học: ").upper()
        if subject in ['A', 'B', 'C']:
            break
        print("❌ Môn học không hợp lệ. Vui lòng nhập A, B hoặc C.")
    
    # Khởi tạo client
    client = ClientBase(subject)
    
    # Nhập mã sinh viên
    student_id = input("Nhập mã số sinh viên cần xóa: ")
    
    # Xác nhận xóa
    confirm = input(f"\n⚠️ Bạn có chắc chắn muốn xóa thông tin sinh viên {student_id} trong môn {subject}? (y/n): ").lower()
    
    if confirm == 'y':
        try:
            result = client.delete_student(student_id)
            if 'error' in result:
                print(f"\n❌ Lỗi: {result['error']}")
            else:
                print(f"\n✅ {result['message']}")
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}")
    else:
        print("\n❌ Đã hủy thao tác xóa.") 