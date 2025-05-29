from client_base import ClientBase
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import NODES

def main():
    subject = input("Nhập mã môn học: ").upper()
    client = ClientBase(subject)
    student_id = input("Nhập mã sinh viên: ")
    result = client.calculate_score(student_id)
    print(result)

if __name__ == "__main__":
    main() 