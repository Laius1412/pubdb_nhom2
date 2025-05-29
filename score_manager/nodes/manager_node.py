from flask import Flask, request, jsonify
import requests
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import NODES, SCORE_WEIGHTS

app = Flask(__name__)

# Tạo mapping từ subject đến node URL
NODE_URLS = {
    'A': f"http://localhost:{NODES['node_a']['port']}",
    'B': f"http://localhost:{NODES['node_b']['port']}",
    'C': f"http://localhost:{NODES['node_c']['port']}"
}

def log_action(action, subject, details, status):
    """Ghi log cho một hành động của manager node"""
    try:
        log_data = {
            'action': action,
            'node_id': 'manager',
            'details': {**details, 'subject': subject},
            'status': status
        }
        requests.post(f"http://localhost:{NODES['logger']['port']}/log", json=log_data)
    except Exception as e:
        print(f"Error logging action: {e}")

@app.route('/write/<subject>', methods=['POST'])
def add_score(subject):
    """Thêm điểm số cho môn học"""
    if subject.upper() not in NODE_URLS:
        log_action('add_score', subject, {"error": "Invalid subject"}, 'failed')
        return jsonify({"error": "Môn học không hợp lệ"}), 400
    
    try:
        res = requests.post(f"{NODE_URLS[subject.upper()]}/add", json=request.json)
        if res.status_code == 201:
            log_action('add_score', subject, request.json, 'success')
        else:
            log_action('add_score', subject, {"error": res.json().get('error')}, 'failed')
        return jsonify(res.json()), res.status_code
    except Exception as e:
        log_action('add_score', subject, {"error": str(e)}, 'failed')
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
    log_action('summary_score', 'all', {"student_id": student_id, "results": results}, 'success')
    return jsonify(results)

@app.route('/all/<subject>', methods=['GET'])
def get_all_scores(subject):
    """Lấy tất cả điểm số của một môn học"""
    if subject.upper() not in NODE_URLS:
        log_action('get_all', subject, {"error": "Invalid subject"}, 'failed')
        return jsonify({"error": "Môn học không hợp lệ"}), 400
    
    try:
        res = requests.get(f"{NODE_URLS[subject.upper()]}/all")
        log_action('get_all', subject, {}, 'success')
        return jsonify(res.json()), res.status_code
    except Exception as e:
        log_action('get_all', subject, {"error": str(e)}, 'failed')
        return jsonify({"error": str(e)}), 500

@app.route('/student/<subject>/<id_or_name>', methods=['GET'])
def get_student_score(subject, id_or_name):
    """Tìm kiếm sinh viên theo ID hoặc tên trong một môn học"""
    if subject.upper() not in NODE_URLS:
        log_action('get_student', subject, {"error": "Invalid subject"}, 'failed')
        return jsonify({"error": "Môn học không hợp lệ"}), 400
    
    try:
        res = requests.get(f"{NODE_URLS[subject.upper()]}/student/{id_or_name}")
        if res.status_code == 200:
            log_action('get_student', subject, {"id_or_name": id_or_name}, 'success')
            return jsonify(res.json()), 200
        else:
            log_action('get_student', subject, {"id_or_name": id_or_name, "error": "Not found"}, 'failed')
            return jsonify({"error": "Không tìm thấy sinh viên"}), 404
    except Exception as e:
        log_action('get_student', subject, {"error": str(e)}, 'failed')
        return jsonify({"error": str(e)}), 500

@app.route('/score/<subject>/<student_id>', methods=['GET'])
def calculate_subject_score(subject, student_id):
    """Tính điểm tổng kết của sinh viên trong một môn học"""
    if subject.upper() not in NODE_URLS:
        log_action('calculate_score', subject, {"error": "Invalid subject"}, 'failed')
        return jsonify({"error": "Môn học không hợp lệ"}), 400
    
    try:
        # Lấy thông tin sinh viên
        res = requests.get(f"{NODE_URLS[subject.upper()]}/student/{student_id}")
        if res.status_code != 200:
            log_action('calculate_score', subject, {"student_id": student_id, "error": "Not found"}, 'failed')
            return jsonify({"error": "Không tìm thấy sinh viên"}), 404
        
        student_data = res.json()[0]  # Lấy kết quả đầu tiên
        
        # Tính điểm tổng kết
        score = (student_data.get('cc1', 0) * SCORE_WEIGHTS['CC1'] +
                student_data.get('cc2', 0) * SCORE_WEIGHTS['CC2'] +
                student_data.get('midterm', 0) * SCORE_WEIGHTS['MIDTERM'] +
                student_data.get('final', 0) * SCORE_WEIGHTS['FINAL'])
        
        # Cập nhật điểm tổng kết vào database
        update_data = {
            "id": student_data.get('id'),
            "name": student_data.get('name'),
            "cc1": student_data.get('cc1', 0),
            "cc2": student_data.get('cc2', 0),
            "midterm": student_data.get('midterm', 0),
            "final": student_data.get('final', 0),
            "score": round(score, 2)
        }
        
        # Gửi request cập nhật điểm
        update_res = requests.post(f"{NODE_URLS[subject.upper()]}/add", json=update_data)
        if update_res.status_code != 201:
            log_action('calculate_score', subject, {"student_id": student_id, "error": "Failed to update score"}, 'failed')
            return jsonify({"error": "Không thể cập nhật điểm"}), 500
        
        result = {
            "id": student_data.get('id'),
            "name": student_data.get('name'),
            "score": round(score, 2)
        }
        
        log_action('calculate_score', subject, {"student_id": student_id, "score": result['score']}, 'success')
        return jsonify(result)
    except Exception as e:
        log_action('calculate_score', subject, {"error": str(e)}, 'failed')
        return jsonify({"error": str(e)}), 500

@app.route('/delete/<subject>/<student_id>', methods=['DELETE'])
def delete_student(subject, student_id):
    """Xóa thông tin sinh viên trong một môn học"""
    if subject.upper() not in NODE_URLS:
        log_action('delete', subject, {"error": "Invalid subject"}, 'failed')
        return jsonify({"error": "Môn học không hợp lệ"}), 400
    
    try:
        res = requests.delete(f"{NODE_URLS[subject.upper()]}/delete/{student_id}")
        if res.status_code == 200:
            log_action('delete', subject, {"student_id": student_id}, 'success')
        else:
            log_action('delete', subject, {"student_id": student_id, "error": res.json().get('error')}, 'failed')
        return jsonify(res.json()), res.status_code
    except Exception as e:
        log_action('delete', subject, {"error": str(e)}, 'failed')
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Manager node đang chạy trên port 5000...")
    app.run(port=5000)
