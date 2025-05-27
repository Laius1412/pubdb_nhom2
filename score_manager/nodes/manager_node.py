from flask import Flask, request, jsonify
import requests
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import NODE_URLS, PORTS, SCORE_WEIGHTS

app = Flask(__name__)

@app.route('/write/<subject>', methods=['POST'])
def add_score(subject):
    """Thêm điểm số cho môn học"""
    if subject.upper() not in NODE_URLS:
        return jsonify({"error": "Môn học không hợp lệ"}), 400
    try:
        res = requests.post(f"{NODE_URLS[subject.upper()]}/add", json=request.json)
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/student/<student_id>/summary', methods=['GET'])
def summary_score(student_id):
    """Xem tổng kết điểm của sinh viên ở tất cả các môn"""
    results = {}
    total_score = 0
    for sub, url in NODE_URLS.items():
        try:
            r = requests.get(f"{url}/score/{student_id}")
            if r.status_code == 200:
                s = r.json()
                results[sub] = s
                total_score += s['score']
            else:
                results[sub] = {"error": "Không tìm thấy"}
        except Exception as e:
            results[sub] = {"error": str(e)}
    results['total'] = round(total_score, 2)
    return jsonify(results)

@app.route('/all/<subject>', methods=['GET'])
def get_all_scores(subject):
    """Lấy tất cả điểm số của một môn học"""
    if subject.upper() not in NODE_URLS:
        return jsonify({"error": "Môn học không hợp lệ"}), 400
    try:
        res = requests.get(f"{NODE_URLS[subject.upper()]}/all")
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/student/<subject>/<id_or_name>', methods=['GET'])
def get_student_score(subject, id_or_name):
    """Tìm kiếm sinh viên theo ID hoặc tên trong một môn học"""
    if subject.upper() not in NODE_URLS:
        return jsonify({"error": "Môn học không hợp lệ"}), 400
    try:
        res = requests.get(f"{NODE_URLS[subject.upper()]}/student/{id_or_name}")
        if res.status_code == 200:
            return jsonify(res.json()), 200
        else:
            return jsonify({"error": "Không tìm thấy sinh viên"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/score/<subject>/<student_id>', methods=['GET'])
def calculate_subject_score(subject, student_id):
    """Tính điểm tổng kết của sinh viên trong một môn học"""
    if subject.upper() not in NODE_URLS:
        return jsonify({"error": "Môn học không hợp lệ"}), 400
    
    try:
        # Lấy thông tin sinh viên
        res = requests.get(f"{NODE_URLS[subject.upper()]}/student/{student_id}")
        if res.status_code != 200:
            return jsonify({"error": "Không tìm thấy sinh viên"}), 404
        
        student_data = res.json()[0]  # Lấy kết quả đầu tiên
        
        # Tính điểm tổng kết
        score = (student_data.get('cc1', 0) * SCORE_WEIGHTS['CC1'] +
                student_data.get('cc2', 0) * SCORE_WEIGHTS['CC2'] +
                student_data.get('midterm', 0) * SCORE_WEIGHTS['MIDTERM'] +
                student_data.get('final', 0) * SCORE_WEIGHTS['FINAL'])
        
        result = {
            "id": student_data.get('id'),
            "name": student_data.get('name'),
            "score": round(score, 2)
        }
        
        # Lưu điểm tổng kết vào file JSON của môn học
        db_path = os.path.join(os.path.dirname(__file__), '..', 'database', f'subject_{subject.lower()}.json')
        try:
            with open(db_path, 'r') as f:
                data = json.load(f)
            
            if student_id in data:
                data[student_id]['total_score'] = round(score, 2)
                
                with open(db_path, 'w') as f:
                    json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Lỗi khi lưu điểm tổng kết: {str(e)}")
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete/<subject>/<student_id>', methods=['DELETE'])
def delete_student(subject, student_id):
    """Xóa thông tin sinh viên trong một môn học"""
    if subject.upper() not in NODE_URLS:
        return jsonify({"error": "Môn học không hợp lệ"}), 400
    
    try:
        res = requests.delete(f"{NODE_URLS[subject.upper()]}/delete/{student_id}")
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Manager node đang chạy trên port 5000...")
    app.run(port=5000)
