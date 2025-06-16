from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flags_struct import Flags, Rule, Condition, EvaluateRequest
from dataclasses import dataclass
from typing import List, Dict, Any

app = Flask(__name__)
CORS(app)  # 启用CORS支持

@dataclass
class Condition:
    column: str
    operator: str
    value: Any

@dataclass
class Rule:
    conditions: List[Condition]
    priority: int
    rollout: int = None  # 可选

@dataclass
class Flags:
    name: str
    rules: List[Rule]
    default: Any

@dataclass
class EvaluateRequest:
    user_id: str
    flag: str

@app.route('/flags', methods=['POST'])
def handle_flags():
    try:
        data = request.get_json()
        return jsonify({
            "status": "success",
            "message": "Flags received successfully",
            "data": data
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/evaluate', methods=['POST'])
def handle_evaluate():
    try:
        data = request.get_json()
        return jsonify({
            "status": "success",
            "message": "Evaluation received successfully",
            "data": data
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/', methods=['GET'])
def hello():
    return 'hello', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 