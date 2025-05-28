import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import PORTS

class ClientBase:
    def __init__(self, subject):
        self.subject = subject
        self.manager_url = f"http://localhost:{PORTS['MANAGER']}"

    def add_score(self, student_data):
        """Thêm điểm số của sinh viên"""
        response = requests.post(f"{self.manager_url}/write/{self.subject}", json=student_data)
        return response.json()

    def get_all(self):
        """Lấy tất cả điểm số"""
        response = requests.get(f"{self.manager_url}/all/{self.subject}")
        return response.json()

    def get_student(self, id_or_name):
        """Tìm kiếm sinh viên theo ID hoặc tên"""
        response = requests.get(f"{self.manager_url}/student/{self.subject}/{id_or_name}")
        return response.json()

    def calculate_score(self, student_id):
        """Tính điểm tổng kết của sinh viên"""
        response = requests.get(f"{self.manager_url}/score/{self.subject}/{student_id}")
        return response.json()

    def summary_score(self, student_id):
        """Lấy tổng kết điểm của sinh viên ở tất cả các môn"""
        response = requests.get(f"{self.manager_url}/student/{student_id}/summary")
        return response.json()

    def delete_student(self, student_id):
        """Xóa thông tin sinh viên"""
        response = requests.delete(f"{self.manager_url}/delete/{self.subject}/{student_id}")
        return response.json()
