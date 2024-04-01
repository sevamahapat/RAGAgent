from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from rag_modified import generate_response

app = Flask(__name__)
CORS(app)

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    query = data.get('query')
    
    response = generate_response(query)
    
    # return jsonify({'response': response})
    response_str = str(response)
    return Response(response_str, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=False)