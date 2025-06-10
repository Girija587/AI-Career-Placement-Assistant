from initial import *
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.form.get('data', '')
    key_pressed = request.form.get('key_pressed', '')

    if key_pressed == "enter_key":
        data = data[:-1]

    if data:
        try:
            final_answer = thinking(data)
        except Exception as e:
            import traceback
            error_message = traceback.format_exc()
            final_answer = f"❗ Error occurred:\n{error_message}"  # Show full traceback
        return jsonify({'answer': final_answer})

    return jsonify({'answer': "???"})

if __name__ == '__main__':
    app.run(debug=True)
