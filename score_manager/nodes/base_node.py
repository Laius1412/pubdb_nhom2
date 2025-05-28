from flask import Flask, request, jsonify
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pupdb.core import PupDB
from config import SCORE_WEIGHTS

class BaseNode:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = PupDB(db_path)
        self.app = Flask(__name__)
        self.define_routes()

    def define_routes(self):
        @self.app.route('/add', methods=['POST'])
        def add_score():
            try:
                data = request.json
                if not data:
                    return jsonify({"error": "No data provided"}), 400
                
                student_id = data.get('id')
                if not student_id:
                    return jsonify({"error": "Student ID is required"}), 400
                
                # Đọc dữ liệu hiện tại
                try:
                    with open(self.db_path, 'r') as f:
                        current_data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    current_data = {}
                
                # Thêm dữ liệu mới
                current_data[student_id] = data
                
                # Lưu lại vào file
                with open(self.db_path, 'w') as f:
                    json.dump(current_data, f, indent=4)
                
                return jsonify({"message": "Score added", "data": data}), 201
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route('/all', methods=['GET'])
        def get_all_scores():
            try:
                # Đọc trực tiếp từ file JSON
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                return jsonify(data)
            except (FileNotFoundError, json.JSONDecodeError):
                return jsonify({})
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route('/student/<id_or_name>', methods=['GET'])
        def get_student_score(id_or_name):
            try:
                # Đọc trực tiếp từ file JSON
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                
                result = []
                for student_id, student_data in data.items():
                    if (student_data.get('id') == id_or_name or 
                        student_data.get('name', '').lower() == id_or_name.lower()):
                        result.append(student_data)
                return jsonify(result)
            except (FileNotFoundError, json.JSONDecodeError):
                return jsonify([])
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route('/score/<student_id>', methods=['GET'])
        def calculate_subject_score(student_id):
            try:
                # Đọc trực tiếp từ file JSON
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                
                student = data.get(student_id)
                if not student:
                    return jsonify({"error": "Student not found"}), 404
                
                score = (student.get('cc1', 0) * SCORE_WEIGHTS['CC1'] +
                        student.get('cc2', 0) * SCORE_WEIGHTS['CC2'] +
                        student.get('midterm', 0) * SCORE_WEIGHTS['MIDTERM'] +
                        student.get('final', 0) * SCORE_WEIGHTS['FINAL'])
                
                return jsonify({
                    "id": student.get('id'),
                    "name": student.get('name'),
                    "score": round(score, 2)
                })
            except (FileNotFoundError, json.JSONDecodeError):
                return jsonify({"error": "Database not found or invalid"}), 500
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route('/delete/<student_id>', methods=['DELETE'])
        def delete_student(student_id):
            try:
                # Đọc dữ liệu hiện tại
                try:
                    with open(self.db_path, 'r') as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    return jsonify({"error": "Database not found or invalid"}), 500

                # Kiểm tra sinh viên có tồn tại không
                if student_id not in data:
                    return jsonify({"error": "Student not found"}), 404

                # Xóa sinh viên
                del data[student_id]

                # Lưu lại vào file
                with open(self.db_path, 'w') as f:
                    json.dump(data, f, indent=4)

                return jsonify({"message": f"Student {student_id} deleted successfully"}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500