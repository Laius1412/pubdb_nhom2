import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nodes.base_node import BaseNode

def init_database(db_path):
    """Khởi tạo file database nếu chưa tồn tại hoặc không hợp lệ"""
    # Tạo thư mục database nếu chưa tồn tại
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Kiểm tra và tạo file JSON nếu cần
    if not os.path.exists(db_path):
        with open(db_path, 'w') as f:
            json.dump({}, f)
    else:
        # Kiểm tra file JSON có hợp lệ không
        try:
            with open(db_path, 'r') as f:
                json.load(f)
        except json.JSONDecodeError:
            # Nếu file không hợp lệ, tạo lại
            with open(db_path, 'w') as f:
                json.dump({}, f)

if __name__ == "__main__":
    # Đường dẫn đến file database
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'subject_b.json')
    
    # Khởi tạo database
    init_database(db_path)
    
    # Khởi động node
    node = BaseNode(db_path)
    print("Node B đang chạy trên port 5002...")
    node.app.run(port=5002)
