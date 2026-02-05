from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prompt', methods=['POST'])
def prompt():
    data = request.get_json()
    prompt = data.get('prompt')
    # For now, just echo the prompt back.
    return jsonify({'response': prompt})

if __name__ == '__main__':
    app.run(debug=True)
