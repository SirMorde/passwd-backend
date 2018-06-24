import sys
from flask import Flask, request # Import objects from the Flask
app = Flask(__name__) # Define our main app using Flask

print "This is the name of the script: ", sys.argv[0]
print "Number of arguments: ", len(sys.argv)
print "The arguments are: " , str(sys.argv)

#passwd = sys.argv[1]
#groups = sys.argv[2]

# passwd = open('/etc/passwd.txt', 'r')
# passwdList = [line.splitlines() for line in crimefile.readlines()]


@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"

if __name__ == '__main__': # If this application is called directly, start in debug mode
    app.run(debug=True, port=1025) # Run the app on port 1025 in debug mode

