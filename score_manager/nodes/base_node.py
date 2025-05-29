from flask import Flask, request, jsonify
import sys
import os
import json
from datetime import datetime
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import SCORE_WEIGHTS, NODES

class BaseNode:
    def __init__(self, node_id, port, db_path):
        self.node_id = node_id
        self.port = port
        self.db_path = db_path
        self.logger_url = f'http://localhost:{NODES["logger"]["port"]}/log'
        self.app = Flask(__name__)
        self._setup_routes()
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Đảm bảo file database tồn tại"""
        # Tạo thư mục database nếu chưa tồn tại
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=2, ensure_ascii=False)

    def _log_action(self, action, details, status):
        """Ghi log cho một hành động"""
        try:
            log_data = {
                'action': action,
                'node_id': self.node_id,
                'details': details,
                'status': status
            }
            requests.post(self.logger_url, json=log_data)
        except Exception as e:
            print(f"Error logging action: {e}")

    def _setup_routes(self):
        @self.app.route('/add', methods=['POST'])
        def add_score():
            try:
                data = request.json
                if not data:
                    self._log_action('add', {"error": "No data provided"}, 'failed')
                    return jsonify({"error": "No data provided"}), 400
                
                student_id = data.get('id')
                if not student_id:
                    self._log_action('add', {"error": "Student ID is required"}, 'failed')
                    return jsonify({"error": "Student ID is required"}), 400
                
                # Đọc dữ liệu hiện tại
                try:
                    with open(self.db_path, 'r', encoding='utf-8') as f:
                        current_data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    current_data = {}
                
                # Thêm dữ liệu mới
                current_data[student_id] = data
                
                # Lưu lại vào file
                with open(self.db_path, 'w', encoding='utf-8') as f:
                    json.dump(current_data, f, indent=2, ensure_ascii=False)
                
                self._log_action('add', {"student_id": student_id, "data": data}, 'success')
                return jsonify({"message": "Score added", "data": data}), 201
            except Exception as e:
                self._log_action('add', {"error": str(e)}, 'failed')
                return jsonify({"error": str(e)}), 500

        @self.app.route('/all', methods=['GET'])
        def get_all_scores():
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self._log_action('get_all', {}, 'success')
                return jsonify(data)
            except (FileNotFoundError, json.JSONDecodeError):
                self._log_action('get_all', {}, 'success')
                return jsonify({})
            except Exception as e:
                self._log_action('get_all', {"error": str(e)}, 'failed')
                return jsonify({"error": str(e)}), 500

        @self.app.route('/student/<id_or_name>', methods=['GET'])
        def get_student_score(id_or_name):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                result = []
                for student_id, student_data in data.items():
                    if (student_data.get('id') == id_or_name or 
                        student_data.get('name', '').lower() == id_or_name.lower()):
                        result.append(student_data)
                
                if result:
                    self._log_action('get_student', {"student_id": id_or_name}, 'success')
                    return jsonify(result)
                else:
                    self._log_action('get_student', {"student_id": id_or_name, "error": "Not found"}, 'failed')
                    return jsonify({"error": "Student not found"}), 404
            except Exception as e:
                self._log_action('get_student', {"error": str(e)}, 'failed')
                return jsonify({"error": str(e)}), 500

        @self.app.route('/score/<student_id>', methods=['GET'])
        def calculate_subject_score(student_id):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                student = data.get(student_id)
                if not student:
                    self._log_action('get_score', {"student_id": student_id, "error": "Student not found"}, 'failed')
                    return jsonify({"error": "Student not found"}), 404
                
                score = (student.get('cc1', 0) * SCORE_WEIGHTS['CC1'] +
                        student.get('cc2', 0) * SCORE_WEIGHTS['CC2'] +
                        student.get('midterm', 0) * SCORE_WEIGHTS['MIDTERM'] +
                        student.get('final', 0) * SCORE_WEIGHTS['FINAL'])
                
                # Thêm trường score vào dữ liệu sinh viên
                student['score'] = round(score, 2)
                data[student_id] = student
                
                # Lưu lại vào file
                with open(self.db_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                result = {
                    "id": student.get('id'),
                    "name": student.get('name'),
                    "score": student['score']
                }
                
                self._log_action('get_score', {"student_id": student_id, "score": result['score']}, 'success')
                return jsonify(result)
            except Exception as e:
                self._log_action('get_score', {"error": str(e)}, 'failed')
                return jsonify({"error": str(e)}), 500

        @self.app.route('/delete/<student_id>', methods=['DELETE'])
        def delete_student(student_id):
            try:
                with open(self.db_path, 'r+', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    if student_id not in data:
                        self._log_action('delete', {"student_id": student_id, "error": "Student not found"}, 'failed')
                        return jsonify({"error": "Student not found"}), 404
                    
                    del data[student_id]
                    f.seek(0)
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    f.truncate()
                
                self._log_action('delete', {"student_id": student_id}, 'success')
                return jsonify({"message": f"Student {student_id} deleted successfully"}), 200
            except Exception as e:
                self._log_action('delete', {"error": str(e)}, 'failed')
                return jsonify({"error": str(e)}), 500

    def run(self):
        print(f"Node {self.node_id} đang chạy trên port {self.port}...")
        self.app.run(port=self.port)