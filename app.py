from flask import Flask, request # Import objects from the Flask
app = Flask(__name__) # Define our main app using Flask

@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"

if __name__ == '__main__': # If this application is called directly, start in debug mode
    app.run(debug=True, port=8080) # Run the app on port 8080 in debug mode
