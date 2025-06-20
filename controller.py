from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from model import Flag, EvaluateRequest
from service import evaluate, addOrUpdateFlag

app = Flask(__name__)
CORS(app)  # 启用CORS支持

@app.route('/flags', methods=['POST'])
def flags_endpoint():
    try:
        data = request.get_json()
        flags_data = Flag.from_dict(data)
        result = addOrUpdateFlag(flags_data)
        return str(result), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/evaluate', methods=['POST'])
def evaluate_endpoint():
    try:
        data = request.get_json()
        evaluate_data = EvaluateRequest(**data)
        result = evaluate(evaluate_data.user_id, evaluate_data.flag)
        return str(result), 200
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