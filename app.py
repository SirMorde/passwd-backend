import sys
from flask import Flask, jsonify, request # Import objects from the Flask
app = Flask(__name__) # Define our main app using Flask


print "This is the name of the script: ", sys.argv[0]
print "Number of arguments: ", len(sys.argv)
print "The arguments are: " , str(sys.argv)

#passwd = sys.argv[1]
#groups = sys.argv[2]
passwdFileList = []
passwdUserList = []
groupFileList = []
groupEntryList = []
 # passwd = open('/etc/passwd.txt', 'r')

# Each entry should have 6 fields
with open('./etc/passwd.txt', 'r') as passwdFile:

    # Create a list of lists with each sublist containing the necessary fields for a user
    # [['root', 'x', '0', '0', 'root', '/root', '/bin/bash'], ['daemon', 'x', '1', '1', 'daemon', '/usr/sbin', '/bin/sh']]
    passwdFileList = [line.strip().split(':') for line in passwdFile]

    # **Note** Typically an etc/passwd.txt file contains 7 entries per user:
    # user name, placeholder for password information, user ID number (UID), user's group ID number (GID),
    # comment field, user home directory, and login shell
    #
    # This project will expect a typical passwd file as input, but will NOT return the placeholder for password information
    # as specified by the coding challenge instructions, so only 6 fields will be displayed
    for user in passwdFileList:
      if len(user) != 7:
        # !!!!!!!!!!!!!!RAISE EXCEPTION!!!!!!!!!!!!!!
        print "ERROR: Malformed passwd file\nMissing field detected for user: " + ":".join(user)
        print "Each user entry should contain 7 fields: Username, Password Info, UID, GID, Comments, Home, Shell"
        print "EX: root:x:0:0:root:/root:/bin/bash"
        # !!!!!!!!!!!!!!RAISE EXCEPTION!!!!!!!!!!!!!!

      # **Note** We are ignoring encrypted password (user[1]) as per the instructions
      #passwdUserEntry = PasswdUser(user[0], user[2], user[3], user[4], user[5], user[6])
      passwdUserEntry = {"username": user[0], "uid": user[2], "gid": user[3], "comment": user[4], "home": user[5], "shell": user[6]}
      passwdUserList.append(passwdUserEntry)

with open('./etc/group.txt', 'r') as groupFile:
    # Create a list of lists with each sublist containing the necessary fields for a user
    # [['root', 'x', '0', '0', 'root', '/root', '/bin/bash'], ['daemon', 'x', '1', '1', 'daemon', '/usr/sbin', '/bin/sh']]
    groupFileList = [line.strip().split(':') for line in groupFile]

    # **Note** Typically an etc/group.txt file contains 4 entries per user: Group Name, Password, Group ID, and Group List
    #
    # This project will expect a typical group file as input, but will NOT return the
    # Password as specified by the coding challenge instructions, so only 3 fields will be displayed
    for group in groupFileList:
      if len(group) != 4:
        print "ERROR: Malformed group file\nMissing field detected for group: " + ":".join(group)
        print "Each group entry should contain 4 fields: Group Name, Password, Group ID, and Group List"
        print "EX: cdrom:x:24:username, username1"
        # !!!!!!!!!!!!!!RAISE EXCEPTION!!!!!!!!!!!!!!

      # MAKE MEMBERS A LIST OF ALL MEMBERS! .SPLIT(,)
      groupEntry = {"name": user[0], "gid": user[2], "members": user[3]}
      groupEntryList.append(groupEntry)


# print(passwdFileList)
# print("\nSPACEEE\n")
# print(groupList)
# print("\nSPACEEE\n")

@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"

@app.route('/users', methods=['GET'])
def get_users():
    # Returns users as a list of JSON objects
    # for user in passwdList:
    #   entryToJson = [user.split(':')]
    #   for field in entryToJson:
    #     print field


    # print passwdUserList
    # for userEntry in passwdUserList:
    #   for thisProp in userEntry:
    #     print thisProp
    # # Convert Python object to JSON object
    # jsonObj = json.dumps(passwdUserList.__dict__)
    return jsonify(passwdUserList)

@app.route('/users/<string:uid>', methods=['GET'])
def get_single_user(uid):

    # Iterate through our user list and return user info if the provided uid exists
    for userList in passwdUserList:
      if userList['uid'] == uid:
        # does exist
        return jsonify(userList)
    # !!!!!!!!!!!!!!RAISE EXCEPTION!!!!!!!!!!!!!!
    return "404"
    # !!!!!!!!!!!!!!RAISE EXCEPTION!!!!!!!!!!!!!!


if __name__ == '__main__': # If this application is called directly, start in debug mode
    app.run(debug=True, port=1025, use_reloader=True) # Run the app on port 1025 in debug mode

