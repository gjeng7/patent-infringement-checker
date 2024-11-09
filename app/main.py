from flask import Flask, request, jsonify
from flask_cors import CORS
from app.utils import load_json, analyze_infringement

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Load data at app startup
companies = load_json('company_products.json')
patents = load_json('patents.json')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    patent_id = data.get("patent_id")
    company_name = data.get("company_name")
    
    if not patent_id or not company_name:
        return jsonify({"error": "Both patent_id and company_name are required"}), 400
    
    analysis = analyze_infringement(patent_id, company_name, patents, companies)
    if not analysis:
        return jsonify({"error": "Patent or company not found"}), 404
    
    return jsonify(analysis)


@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "API is working!"})


if __name__ == "__main__":
    app.run(debug=True)


