import os
import sys
import copy
from flask import Flask, jsonify, request, abort
app = Flask(__name__)

print "This is the name of the script: ", sys.argv[0]
print "Number of arguments: ", len(sys.argv)
print "The arguments are: " , str(sys.argv)

# TO DO - Code:
# - Read input arguments as path
# - If input arguments are not given default to system path
# - Detect changes in the file and recreate these lists
# - Create function for initializing file objects and running when change is detected

# To Do - Assignment:
# - Write unit tests
# - Test on vagrant using curl
# - Write Readme guide
# - Add instructions on /index
# - Clean up code and comments

passwdFileList = []
passwdUserList = []
groupFileList = []
groupEntryList = []

try:
    passwdFilePath = sys.argv[1]
except:
    passwdFilePath = './etc/passwd.txt'

try:
    groupFilePath = sys.argv[2]
except:
    groupFilePath = './etc/group.txt'

if os.path.isfile(passwdFilePath):
  print "Passwd file path exists!"
else:
  print "ERROR: Entered passwd file was not found: " + passwdFilePath

if os.path.isfile(groupFilePath):
  print "Group file path exists!"
else:
  print "ERROR: Entered group file was not found: " + groupFilePath

# Open passwd file as read only (Specified by 'r')
try:
  with open(passwdFilePath, 'r') as passwdFile:
      lineNumber = 1

      # Create a list of lists with each sublist containing the necessary fields for a user
      # Ex: [['root', 'x', '0', '0', 'root', '/root', '/bin/bash'], ['daemon', 'x', '1', '1', 'daemon', '/usr/sbin', '/bin/sh']]
      passwdFileList = [line.lower().strip().split(':') for line in passwdFile]

      # **Note** Typically an etc/passwd.txt file contains 7 entries per user: user name, placeholder for password information,
      # user ID number (UID), user's group ID number (GID), comment field, user home directory, and login shell.
      # This project will expect a typical passwd file as input, but will NOT return the placeholder for password information
      # as specified by the coding challenge instructions, so only 6 fields will be displayed
      for user in passwdFileList:
        if len(user) != 7:
          print "ERROR: Malformed passwd file - Incorrect number of fields detected for entry on line number " + str(lineNumber) + ": " + ":".join(user)
          print "Each user entry should contain 7 fields: Username, Password Info, UID, GID, Comments, Home, Shell"
          print "EX: root:x:0:0:root:/root:/bin/bash"
          sys.exit()

        # **Note** We are ignoring the encrypted password (user[1]) as per the instructions
        passwdUserEntry = {"name": user[0], "uid": user[2], "gid": user[3], "comment": user[4], "home": user[5], "shell": user[6]}
        passwdUserList.append(passwdUserEntry)
        lineNumber += 1
except IOError as err:
    print "ERROR: Could not read passwd file:", passwdFilePath, "\nException:", err.args
    sys.exit()


# Open group file as read only (Specified by 'r')
try:
  with open(groupFilePath, 'r') as groupFile:
      lineNumber = 1

      # Create a list of lists with each sublist containing the necessary fields for a group
      # Ex: [['dialout', 'x', '20', 'username'], ['cdrom', 'x', '24', 'username, username1']]
      groupFileList = [line.lower().strip().split(':') for line in groupFile]

      # **Note** Typically an etc/group.txt file contains 4 entries per user: Group Name, Password, Group ID, and Group List
      # This project will expect a typical group file as input, but will NOT return the
      # password as specified by the coding challenge instructions, so only 3 fields will be displayed
      for group in groupFileList:
        if len(group) != 4:
          print "ERROR: Malformed group file - Incorrect number of fields detected for entry on line number " + str(lineNumber) + ": " + ":".join(group)
          print "Each group entry should contain 4 fields: Group Name, Password Info, Group ID, and Group List"
          print "EX: cdrom:x:24:username, username1"
          sys.exit()

        # How the members list is built:
        # First remove all white spaces ( "".join(group[3].split()) ),
        # change text to lower case ( .lower() ), strip leading and trailing whitespaces ( .lower().strip().split(',') ),
        # then create a list seperating each element that has a comma inbetween ( .split(',') )

        # **Note** We are ignoring the encrypted password (user[1]) as per the instructions
        groupEntry = {"name": group[0], "gid": group[2], "members": "".join(group[3].split()).lower().strip().split(',')}
        groupEntryList.append(groupEntry)
        lineNumber += 1
except IOError as err:
    print "ERROR: Could not read group file:", groupFilePath, "\nException:", err.args
    sys.exit()

@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"

@app.route('/users', methods=['GET'])
def get_users():
    # Returns users as a list of JSON objects
    return jsonify(passwdUserList)

@app.route('/users/<string:uid>', methods=['GET'])
def get_single_user(uid):

    # Iterate through our user list and return user info if the provided uid exists
    for userList in passwdUserList:
      if userList['uid'] == uid:
        return jsonify(userList)
    return "404 Not found"

@app.route('/users/query', methods=['GET'])
def get_users_query():
    queryResult = []
    myQuery = {
      "name": request.args.get("name"),
      "uid": request.args.get("uid"),
      "gid": request.args.get("gid"),
      "comment": request.args.get("comment"),
      "home": request.args.get("home"),
      "shell": request.args.get("shell")
    }

    # Note: "!=" used for exact match. "not in" could be used for partial match.
    for user in passwdUserList:
      if myQuery["name"] is not None and myQuery["name"].lower().strip() != user["name"].lower().strip():
        print "No name!"
        continue
      if myQuery["uid"] is not None and myQuery["uid"].lower().strip() != user["uid"].lower().strip():
        print "No uid!"
        continue
      if myQuery["gid"] is not None and myQuery["gid"].lower().strip() != user["gid"].lower().strip():
        print "No gid!"
        continue
      if myQuery["comment"] is not None and myQuery["comment"].lower().strip() != user["comment"].lower().strip():
        print "No comment!"
        continue
      if myQuery["home"] is not None and myQuery["home"].lower().strip() != user["home"].lower().strip():
        print "No home!"
        continue
      if myQuery["shell"] is not None and myQuery["shell"].lower().strip() != user["shell"].lower().strip():
        print "No shell!"
        continue
      queryResult.append(user)
    return jsonify(queryResult)

@app.route('/groups', methods=['GET'])
def get_groups():
    return jsonify(groupEntryList)

@app.route('/groups/<string:gid>', methods=['GET'])
def get_single_group(gid):

    # Iterate through our user list and return group info if the provided gid exists
    for currentEntry in groupEntryList:
      if currentEntry['gid'] == gid:
        return jsonify(currentEntry)
    return "404 Not found"

@app.route('/groups/query', methods=['GET'])
def get_groups_query():
    queryResult = []
    myQuery = {
      "name": request.args.get("name"),
      "gid": request.args.get("gid"),
      "member": request.args.getlist("member")
    }

    for groupEntry in groupEntryList:

      # Match name field
      # Note: "!=" used for exact match. "not in" could be used for partial match.
      if myQuery["name"] is not None and myQuery["name"].lower().strip() != groupEntry["name"].lower().strip():
        print "No name!"
        continue # Return to loop "for groupEntry in groupEntryList:"

      # Match gid field
      if myQuery["gid"] is not None and myQuery["gid"].lower().strip() != groupEntry["gid"].lower().strip():
        print "No gid!"
        continue # Return to loop "for groupEntry in groupEntryList:"

      # match member fieldss
      if myQuery["member"] and groupEntry["members"]:

        # A deep copy of the current member list. We can modify this without tampering with the original data
        # We will remove a member from this list when a match is made so we don't double count
        tempGroupEntry = copy.deepcopy(groupEntry["members"])
        expectedMatches = len(myQuery["member"])
        foundMatches = 0
        for currentMember in myQuery["member"]:
          if currentMember in tempGroupEntry:

            # Remove current member so we don't double count
            tempGroupEntry.remove(currentMember)
            foundMatches += 1
          else:
            break # Return to start of loop "for currentMember in myQuery["members"]"

        # If we did not find all members in this entry, go on to the next entry in groupEntryList
        if foundMatches != expectedMatches:
          continue # Return to start of loop "for groupEntry in groupEntryList:"
      else:
        continue
      queryResult.append(groupEntry)
    return jsonify(queryResult) # End of "for groupEntry in groupEntryList:"

if __name__ == '__main__':

    # If this application is called directly, start in debug mode
    # Run the app on port 1025 in debug mode
    app.run(debug=True, port=1025, use_reloader=True)
