from flask import Flask, request, jsonify
import json
app = Flask(__name__)

mock_test_data = json.load(open('output_api.json'))
mock_test_emails ={
    "example@mail.com":mock_test_data
}
@app.route('/get_linkedin_data', methods=['GET'])
def get_linkedin_data():
    email = request.args.get('email')
    if email in mock_test_emails:
        return jsonify(mock_test_emails[email])
    else:
        return jsonify({"error": "Data not found for the provided email"}), 404

if __name__ == '__main__':
    app.run(debug=True)
