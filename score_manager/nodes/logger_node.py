from flask import Flask, request, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)

# Đường dẫn đến file JSON chứa log
LOG_JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'logs.json')

def ensure_log_file_exists():
    """Đảm bảo file JSON log tồn tại"""
    # Tạo thư mục database nếu chưa tồn tại
    os.makedirs(os.path.dirname(LOG_JSON_PATH), exist_ok=True)
    
    if not os.path.exists(LOG_JSON_PATH):
        with open(LOG_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2, ensure_ascii=False)

def append_log(action, node_id, details, status):
    """Thêm một log mới vào file JSON"""
    ensure_log_file_exists()
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'node_id': node_id,
        'details': details,
        'status': status
    }
    
    try:
        with open(LOG_JSON_PATH, 'r+', encoding='utf-8') as f:
            logs = json.load(f)
            logs.append(log_entry)
            f.seek(0)
            json.dump(logs, f, indent=2, ensure_ascii=False)
            f.truncate()
    except Exception as e:
        print(f"Error writing to log file: {e}")

@app.route('/log', methods=['POST'])
def log_action():
    """API endpoint để nhận và lưu log"""
    data = request.json
    required_fields = ['action', 'node_id', 'details', 'status']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    append_log(
        action=data['action'],
        node_id=data['node_id'],
        details=data['details'],
        status=data['status']
    )
    
    return jsonify({'message': 'Log recorded successfully'})

@app.route('/logs', methods=['GET'])
def get_logs():
    """API endpoint để lấy tất cả logs"""
    ensure_log_file_exists()
    
    try:
        with open(LOG_JSON_PATH, 'r', encoding='utf-8') as f:
            logs = json.load(f)
        return jsonify(logs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    ensure_log_file_exists()
    app.run(port=5004) 