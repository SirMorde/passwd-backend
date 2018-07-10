import os, time, sys, copy, platform
from flask import Flask, jsonify, request, abort
app = Flask(__name__)

# Debug:
# print "This is the name of the script: ", sys.argv[0]
# print "Number of arguments: ", len(sys.argv)
# print "The arguments are: " , str(sys.argv)

def setFilePaths():
    '''
    Set file paths for passwd and group files to be accessed by the web service.
    Defaults to example file for Windows and Mac

    '''

    global passwdFilePath
    passwdFilePath = ""
    global groupFilePath
    groupFilePath = ""

    try:
      passwdFilePath = sys.argv[1]
      print "Entered passwd file: " + passwdFilePath
    except:

      # Used for running on Windows & Mac using an example passwd.txt file since /etc/passwd doesn't exist
      # Also used for unit testing
      if "windows" in str(platform.system()).lower() or "darwin" in str(platform.system()).lower():
        passwdFilePath = './etc/passwd.txt'
        print "No passwd file provided... defaulting to example passwd file: " + passwdFilePath
      else:
        passwdFilePath = "/etc/passwd"
        print "No passwd file provided... defaulting to system passwd file: " + passwdFilePath

    try:
      groupFilePath = sys.argv[2]
      print "Entered group file: " + groupFilePath
    except:

      # Used for running on Windows & Mac using an example group.txt file since /etc/passwd doesn't exist
      # Also used for unit testing
      if "windows" in str(platform.system()).lower() or "darwin" in str(platform.system()).lower():
        groupFilePath = './etc/group.txt'
        print "No group file provided... defaulting to example group file: " + groupFilePath
      else:
        groupFilePath = "/etc/group"
        print "No group file provided... defaulting to system group file: " + groupFilePath

def updateFileLists():
    '''
      Creates the lists containing the passwd and group file's contents

    '''

    global passwdUserList
    passwdUserList = []
    global groupEntryList
    groupEntryList = []
    global passwdModTime
    passwdModTime = ""
    global groupModTime
    groupModTime = ""

    try:

      # Ensure the passwd file exists
      if os.path.isfile(passwdFilePath):

        # Update the time of last modification of path. The return value is a number giving the number of
        # seconds since the epoch (see the time module)
        passwdModTime = os.path.getmtime(passwdFilePath)

        # Open passwd file as read only (Specified by 'r')
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
      else:
        print "ERROR: No such file or directory:", passwdFilePath
        sys.exit()
    except IOError as err:

      # Notice the syntax to concatenate using ','. This is important as concatenating wtih '+' may not work for different object types
      print "ERROR: Could not read passwd file:", passwdFilePath, "\nException:", err.args
      sys.exit()

    try:

      # Ensure the group file exists
      if os.path.isfile(groupFilePath):

        # Update the time of last modification of path. The return value is a number giving the number of
        # seconds since the epoch (see the time module)
        groupModTime = os.path.getmtime(groupFilePath)

        # Open group file as read only (Specified by 'r')
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
              # Finally filter(None, myList) Removes all empty entries from the list

              # **Note** We are ignoring the encrypted password (user[1]) as per the instructions
              groupEntry = {"name": group[0], "gid": group[2], "members": filter(None, "".join(group[3].split()).lower().strip().split(','))}
              groupEntryList.append(groupEntry)
              lineNumber += 1
      else:
        print "ERROR: No such file or directory:", groupFilePath
        sys.exit()
    except IOError as err:

      # Notice the syntax to concatenate using ','. This is important as concatenating wtih '+' may not work for different object types
      print "ERROR: Could not read group file:", groupFilePath, "\nException:", err.args
      sys.exit()

@app.route('/', methods=['GET'])
def index():
    return "Hello, World!\n"

@app.route('/users', methods=['GET'])
def get_users():
    '''
    Return a list of all users on the system, as defined in the /etc/passwd file.

    '''

    # Detect modifications made to our passwd file using the "time of last modification of path"
    if passwdModTime != os.path.getmtime(passwdFilePath):
      updateFileLists()

    # Returns users as a list of JSON objects
    return jsonify(passwdUserList)

@app.route('/users/query', methods=['GET'])
def get_users_query():
    '''
    Return a list of users matching all of the specified query fields. The bracket notation indicates that any of the
    following query parameters may be supplied:
    - name
    - uid
    - gid
    - comment
    - home
    - shell
    Only exact matches are supported.

    '''

    # Detect changes made to our passwd file using the "time of last modification of path"
    if passwdModTime != os.path.getmtime(passwdFilePath):
      updateFileLists()
    queryResult = []
    myQuery = {
      "name": request.args.get("name"),
      "uid": request.args.get("uid"),
      "gid": request.args.get("gid"),
      "comment": request.args.get("comment"),
      "home": request.args.get("home"),
      "shell": request.args.get("shell")
    }

    acceptableArgs = ["name", "uid", "gid", "comment", "home", "shell"]

    # Ensure that all of the query arguments the user provides are supported by the backend API
    all_args = request.args.lists()
    for requestArgs in all_args:
        if requestArgs[0] not in acceptableArgs:
            errorMessage = "Provided query not supported:" + str(requestArgs[0])
            abort(400, errorMessage)

    # Note: "!=" used for exact match. "not in" could be used for partial match.
    for user in passwdUserList:
      if myQuery["name"] is not None and myQuery["name"].lower().strip() != user["name"].lower().strip():
        continue
      if myQuery["uid"] is not None and myQuery["uid"].lower().strip() != user["uid"].lower().strip():
        continue
      if myQuery["gid"] is not None and myQuery["gid"].lower().strip() != user["gid"].lower().strip():
        continue
      if myQuery["comment"] is not None and myQuery["comment"].lower().strip() != user["comment"].lower().strip():
        continue
      if myQuery["home"] is not None and myQuery["home"].lower().strip() != user["home"].lower().strip():
        continue
      if myQuery["shell"] is not None and myQuery["shell"].lower().strip() != user["shell"].lower().strip():
        continue
      queryResult.append(user)
    return jsonify(queryResult)

@app.route('/users/<string:uid>', methods=['GET'])
def get_single_user(uid):
    '''
    Return a single user with <uid>. Returns 404 if <uid> is not found

    '''

    # Detect modifications made to our passwd file using the "time of last modification of path"
    if passwdModTime != os.path.getmtime(passwdFilePath):
      updateFileLists()

    # Iterate through our user list and return user info if the provided uid exists
    for userList in passwdUserList:
      if userList['uid'] == uid:
        return jsonify(userList)
    return abort(404)

@app.route('/users/<string:uid>/groups', methods=['GET'])
def get_single_user_groups(uid):
    """
    Return all the groups for a given user.
    This implementation will find the name corresponding to the provided uid, then check each group's membership
    to see if the current name can be found.

    """

    usersGroups = []

    # Detect modifications made to our passwd and group file using the "time of last modification of path"
    if passwdModTime != os.path.getmtime(passwdFilePath) or groupModTime != os.path.getmtime(groupFilePath):
      updateFileLists()

    # Iterate through our user list and see if the provided uid exists
    for userList in passwdUserList:
      if userList["uid"] == uid:

        # If the uid exists, begin searching to see which groups the current user is in
        for groupEntry in groupEntryList:

          # If the current user's name is a member of the current group entry, add that group to the return list
          if userList["name"] in groupEntry["members"]:
            usersGroups.append(groupEntry)
        return jsonify(usersGroups)
    return abort(404)

@app.route('/groups', methods=['GET'])
def get_groups():
    '''
    Return a list of all groups on the system, a defined by /etc/group.

    '''

    # Detect changes made to our group file using the "time of last modification of path"
    if groupModTime != os.path.getmtime(groupFilePath):
      updateFileLists()
    return jsonify(groupEntryList)

@app.route('/groups/query', methods=['GET'])
def get_groups_query():
    '''
    Return a list of groups matching all of the specified query fields. The bracket notation indicates that any of the
    following query parameters may be supplied:
    - name
    - gid
    - member (repeated)

    '''

    queryResult = []

    # Detect changes made to our group file using the "time of last modification of path"
    if groupModTime != os.path.getmtime(groupFilePath):
      updateFileLists()
    myQuery = {
      "name": request.args.get("name"),
      "gid": request.args.get("gid"),
      "member": request.args.getlist("member")
    }

    acceptableArgs = ["name", "gid", "member"]

    # Determines whether or not "member" was provided as a query
    memberQuery = 0

    # Ensure that all of the query arguments the user provides are supported by the backend API
    all_args = request.args.lists()
    for requestArgs in all_args:
        if requestArgs[0] not in acceptableArgs:
            errorMessage = "Provided query not supported:" + str(requestArgs[0])
            abort(400, errorMessage)

    for groupEntry in groupEntryList:

      # Match name field
      # Note: "!=" used for exact match. "not in" could be used for partial match.
      if myQuery["name"] is not None and myQuery["name"].lower().strip() != groupEntry["name"].lower().strip():
        continue # Return to start of the loop "for groupEntry in groupEntryList:"

      # Match gid field
      if myQuery["gid"] is not None and myQuery["gid"].lower().strip() != groupEntry["gid"].lower().strip():
        continue # Return to start of the loop "for groupEntry in groupEntryList:"

      # Match member fields
      # If both member lists are not empty. A non empty list will evaluate to "True"
      if myQuery["member"]:
        memberQuery = 1
        foundMatches = 0
        expectedMatches = len(myQuery["member"])

        if groupEntry["members"]:

          # tempGroupEntry is a deep copy of the current member list. We can modify this without tampering with the original data
          # We will remove a member from tempGroupEntry when a match is made so that we don't double count
          tempGroupEntry = copy.deepcopy(groupEntry["members"])
          for currentMember in myQuery["member"]:
            if currentMember in tempGroupEntry:

              # Remove current member so we don't double count
              tempGroupEntry.remove(currentMember)
              foundMatches += 1
            else:
              break # If no match was made, stop searching the current groupEntry

        # If we did not find all queried members in this entry, go on to the next entry in groupEntryList
        if foundMatches != expectedMatches and memberQuery == 1:
          continue # Return to start of loop "for groupEntry in groupEntryList:"

      # If the query passes each check, only then will we append it to our final result. Move on to the next groupEntry
      queryResult.append(groupEntry)
    return jsonify(queryResult) # End of "for groupEntry in groupEntryList:"

@app.route('/groups/<string:gid>', methods=['GET'])
def get_single_group(gid):
    '''
    Return a single group with <gid>. Return 404 if <gid> is not found.

    '''

    # Detect changes made to our group file using the "time of last modification of path"
    if groupModTime != os.path.getmtime(groupFilePath):
      updateFileLists()

    # Iterate through our user list and return group info if the provided gid exists
    for currentEntry in groupEntryList:
      if currentEntry['gid'] == gid:
        return jsonify(currentEntry)
    return abort(404)

# If this application is started directly, not imported
if __name__ == '__main__':
    setFilePaths()
    updateFileLists()

    # Run the app at http://127.0.0.1:1025/ in debug mode.
    app.run(debug=True, port=1025, use_reloader=True)
