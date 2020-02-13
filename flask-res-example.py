from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def default():
    return jsonify({"key1":"Hello World!"})

@app.route('/hey', methods=['GET','POST'])
def hey():
    if request.method == 'POST':
        input_json = request.get_json()
        return jsonify({'you sent':input_json})
    else:
        return jsonify({"key1":"Hello World but from the /hey endpoint"})

@app.route('/get_times_ten/<int:num>', methods=['GET'])
def times_ten(num):
    return jsonify({'answer':num*10})

@app.route('/register', methods=['POST'])
def register():
    return

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)