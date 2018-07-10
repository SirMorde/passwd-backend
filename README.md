# passwd-backend
passwd-backend is a minimal HTTP service that exposes the user and group information on a UNIX-like system that is usually locked away in the UNIX /etc/passwd and /etc/groups files.

Table of contents
=================

<!--ts-->
   * [Requirements](#requirements)
   * [API Resources](#api-resources)
      * [GET /users](#get-/users)
      * [GET /users/query[?name=<nq>][&uid=<uq>][&gid=<gq>][&comment=<cq>][&home=<hq>][&shell=<sq>]](#get-/users/query[?name=<nq>][&uid=<uq>][&gid=<gq>][&comment=<cq>][&home=<hq>][&shell=<sq>])
      * [GET /users/<uid>](#get-/users/<uid>)
      * [GET /users/<uid>/groups](#get-/users/<uid>/groups)
      * [GET /groups](#get-/groups)
      * [GET /groups/query[?name=<nq>][&gid=<gq>][&member=<mq1>[&member=<mq2>][&...]]](#get-/groups/query[?name=<nq>][&gid=<gq>][&member=<mq1>[&member=<mq2>][&...]])
      * [GET /groups/<gid>](#get-/groups/<gid>)
   * [Installation](#installation)
      * [Cloning the Git Repository](#cloning-the-git-repository)
      * [Setting Up Your Virtual Environment](#setting-up-your-virtual-environment-optional)
        * [Creating Your Virtual Environment](#creating-your-virtual-environment)
        * [Activating Your Virtual Environment](#activating-your-virtual-environment)
        * [Deactivating Your Virtual Environment](#deactivating-your-virtual-environment)
      * [Installing Dependencies](#installing-dependencies)
   * [Running the Service](#running-the-service)
   * [Testing](#testing)
<!--te-->

## Requirements
To use this project you will need the following prerequisites:
+ [Git](https://git-scm.com/downloads)
+ [Python 2.7.14 or newer](https://www.python.org/downloads/)

## API Resources

### GET /users
Returns a list of all users on the system, as defined in the /etc/passwd file.

**_Example Response:_**
```
[
  {“name”: “root”, “uid”: 0, “gid”: 0, “comment”: “root”, “home”: “/root”,“shell”: “/bin/bash”},
  {“name”: “dwoodlins”, “uid”: 1001, “gid”: 1001, “comment”: “”, “home”:“/home/dwoodlins”, “shell”: “/bin/false”}
]
```


### GET /users/query[?name=<nq>][&uid=<uq>][&gid=<gq>][&comment=<cq>][&home=<hq>][&shell=<sq>]
Returns a list of users matching all of the specified query fields. The bracket notation indicates that any of the
following query parameters may be supplied:
- name
- uid
- gid
- comment
- home
- shell
Only exact matches are supported.

**_Example Query:_**
```
GET /users/query?shell=%2Fbin%2Ffalse
```

**_Example Response:_**
```
[
  {“name”: “dwoodlins”, “uid”: 1001, “gid”: 1001, “comment”: “”, “home”:“/home/dwoodlins”, “shell”: “/bin/false”}
]
```

### GET /users/<uid>
Returns a single user with <uid>. Returns 404 if <uid> is not found.

**_Example Response:_**
```
{“name”: “dwoodlins”, “uid”: 1001, “gid”: 1001, “comment”: “”, “home”:“/home/dwoodlins”, “shell”: “/bin/false”}
```

### GET /users/<uid>/groups
Returns all the groups for a given user.

**_Example Response:_**
```
[
  {“name”: “docker”, “gid”: 1002, “members”: [“dwoodlins”]}
]
```

### GET /groups
Returns a list of all groups on the system, as defined by /etc/group.

**_Example Response:_**
```
[
  {“name”: “_analyticsusers”, “gid”: 250, “members”:[“_analyticsd’,”_networkd”,”_timed”]},
  {“name”: “docker”, “gid”: 1002, “members”: []}
]
```

### GET /groups/query[?name=<nq>][&gid=<gq>][&member=<mq1>[&member=<mq2>][&...]]
Returns a list of groups matching all of the specified query fields. The bracket notation indicates that any of the following query parameters may be supplied:
- name
- gid
- member (repeated)
Any group containing all the specified members are returned, i.e. when query members are a subset of group members.

**_Example Query:_**
```
GET /groups/query?member=_analyticsd&member=_networkd
```

**_Example Response:_**
```
[
  {“name”: “_analyticsusers”, “gid”: 250, “members”:[“_analyticsd’,”_networkd”,”_timed”]}
]
```

### GET /groups/<gid>
Returns a single group with <gid>. Return 404 if <gid> is not found.

**_Example Response:_**
```
{“name”: “docker”, “gid”: 1002, “members”: [“dwoodlins”]}
```

## Installation 
### Cloning the Git Repository
Once you have Git installed, clone this repository by running the following command:
```
sudo git clone https://github.com/SirMorde/passwd-backend
```

### Setting Up Your Virtual Environment (Optional)
For this project the Virtual Environment [**virtualenv**](https://virtualenv.pypa.io/en/stable/userguide/) was used. Refer to this [article](https://realpython.com/python-virtual-environments-a-primer/) on RealPython.com to learn more about what virtual environments are and why we should use them.

To install Virtualenv run the following command:
```
sudo pip install virtualenv 
```

#### Creating Your Virtual Environment
**Note:** Virtual environments for different operating systems are not compatible! This means that if you are using Windows or Mac, you will need to create a new virtual environment

Replace <YOUR_VENV_NAME> with your desired virtual environment name to create your virtual environment for the first time:
```
sudo virtualenv <YOUR_VENV_NAME> --always-copy
```
**_Example:_**
```
sudo virtualenv venv_linux --always-copy
```

#### Activating Your Virtual Environment 
**Note:** Activating your virtual environment will differ slightly for different operating systems. If you are having issues activating your virtual environment, refer to the [virtualenv user guide](https://virtualenv.pypa.io/en/stable/userguide/#activate-script)

To begin using your virtual environment and install Python packages in your virtual environment's location instead of your operating system's location, you first need to activate your virtual environment:
```
. <YOUR_VENV_NAME>/bin/activate
```

**_Example:_**
```
. venv_linux/bin/activate
```

#### Deactivating Your Virtual Environment 
To stop using your virtual environment, you can deactivate it by running:
```
deactivate
```

### Installing Dependencies
**Note: If you are using a virtual environment, make sure to activate it before running this command:**

Once you have Python 2.7 installed, simply run the following command inside your project directory to download all dependencies automatically. 
```
pip install -r requirements.txt
```

## Running the Service
**Note: If you are using a virtual environment, make sure to activate it before running this command.**

You can start the service by navigating to the project directory and running the following command:
```
python app.py
```
On Linux, simply running this command with no input parameters to the application will make use of the system's /etc/passwd and /etc/group files. On Windows and Mac, this application will default to the project directory's example /etc/passwd.txt and /etc/group.txt files.

Additionally the passwd and group files are configurable, meaning you can specify which passwd and group files you would like to use by passing them in as input parameters when calling the application. 
**Note: The first input argument will always indicate the passwd file and second input argument will always indicate the group file.**
```
python app.py <YOUR_PASSWD_FILE.TXT> <YOUR_GROUP_FILE.TXT>
```
**_Example using the project directory's example passwd and group files:_** 
```
python app.py ./etc/passwd.txt ./etc/group.txt

```

## Testing
**Note: Before running the unit tests, you will need to have an instance of the service running. You will want to start the service using the project's example passwd and group files as the unit test checks for particular values in the API response.**

Navigate to ...\passwd-backend\tests\unit and then run the following command:
```
pytest
```
The unit test will make GET requests to the service and display the results.
