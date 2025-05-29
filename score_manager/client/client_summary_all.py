import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client_base import ClientBase

if __name__ == "__main__":
    # Khởi tạo client cho môn
    client = ClientBase("A")
    
    student_id = input("Nhập mã số sinh viên: ")
    print(f"\n📊 Tổng kết điểm của sinh viên {student_id}:")
    
    try:
        # Lấy tổng kết điểm thông qua client_base
        results = client.summary_score(student_id)
        
        # Đếm số môn có điểm
        valid_subjects = 0
        total_score = 0
        
        # In kết quả từng môn
        for subject, data in results.items():
            if subject != 'total':  # Bỏ qua trường total
                if isinstance(data, dict) and 'error' not in data:
                    print(f"\nMôn {subject}:")
                    print(f"  - Điểm tổng kết: {data['score']}")
                    valid_subjects += 1
                    total_score += data['score']
                else:
                    print(f"\nMôn {subject}: {data.get('error', 'Không có dữ liệu')}")
        
        # Tính và in điểm trung bình
        if valid_subjects > 0:
            average_score = total_score / valid_subjects
            print(f"\n📈 Điểm trung bình các môn: {round(average_score, 2)}")
        else:
            print("\n❌ Không có môn học nào có điểm")
        
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")