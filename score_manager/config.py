PORTS = {
    "MANAGER": 5000,
    "SUBJECT_A": 5001,
    "SUBJECT_B": 5002,
    "SUBJECT_C": 5003
}

NODE_URLS = {
    'A': f'http://localhost:{PORTS["SUBJECT_A"]}',
    'B': f'http://localhost:{PORTS["SUBJECT_B"]}',
    'C': f'http://localhost:{PORTS["SUBJECT_C"]}'
}

SCORE_WEIGHTS = {
    'CC1': 0.05,
    'CC2': 0.05,
    'MIDTERM': 0.30,
    'FINAL': 0.60
}
