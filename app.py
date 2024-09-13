from flask import Flask, request, jsonify, render_template

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

@app.route('/hello')
def hello():
    name = request.args.get('name', 'World')  # Default to 'World' if no name is provided
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    app.run()  # For local development; Gunicorn will be used in production
