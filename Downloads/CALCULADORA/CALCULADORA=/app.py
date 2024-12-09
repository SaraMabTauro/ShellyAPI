from flask import Flask, request, jsonify, send_file
from parser.grammar import evaluate_expression
from parser.tree import generate_tree_image

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    expression = request.json['expression']
    try:
        result = evaluate_expression(expression)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/tree', methods=['POST'])
def tree():
    expression = request.json['expression']
    try:
        image_path = generate_tree_image(expression)
        return jsonify({'tree_image': image_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
