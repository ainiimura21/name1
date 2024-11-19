from flask import Flask, request, jsonify

# Create a Flask application instance
app = Flask(__name__)

# Define a route for the root URL that acts like a servlet
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return "Hello from the Python Servlet (GET request)!"

    elif request.method == 'POST':
        data = request.json  # Get JSON data from POST request
        return jsonify({"message": "Hello from the Python Servlet (POST request)", "data": data})

# Another example "servlet" that handles specific routes
@app.route('/greet/<name>', methods=['GET'])
def greet(name):
    return f"Hello, {name}! Welcome to the Python Servlet."

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
