# Cấu hình cho các node
NODES = {
    'node_a': {
        'port': 5001,
        'db_path': '../database/subject_a.json'
    },
    'node_b': {
        'port': 5002,
        'db_path': '../database/subject_b.json'
    },
    'node_c': {
        'port': 5003,
        'db_path': '../database/subject_c.json'
    },
    'logger': {
        'port': 5004,
        'db_path': '../database/logs.json'
    }
}

# Cấu hình cho manager node
MANAGER_PORT = 5000

# Cấu hình cho client
CLIENT_PORT = 5005

SCORE_WEIGHTS = {
    'CC1': 0.05,
    'CC2': 0.05,
    'MIDTERM': 0.30,
    'FINAL': 0.60
}
