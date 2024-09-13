from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.get_json()
    if data:
        response = {
            'status': 'success',
            'received_data': data
        }
    else:
        response = {
            'status': 'error',
            'message': 'No data provided'
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run()  # For local development; Gunicorn will be used in production

