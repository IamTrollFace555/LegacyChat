from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/api/program', methods=['GET'])
def run_program():
    # Your Python program logic goes here

    # Should change this yo an open AI API call
    response = {
        'message': 'Hello, world!'
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run()
