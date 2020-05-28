#! /usr/bin/python
print('Content-type: text/html\n')

import os

root = '/home/students/2022/jjiang20/public_html/CS1920-Final/'

from pymongo import MongoClient

import cgi

import cgitb
cgitb.enable(display=0, logdir='./logdir')

#db ---------------------------------------
client = pymongo.MongoClient("mongodb://probeyond:QNRezCY6P31hNCI6@cluster0-shard-00-00-zptan.mongodb.net:27017,cluster0-shard-00-01-zptan.mongodb.net:27017,cluster0-shard-00-02-zptan.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client['ProductivityApp']
users = db['Users']
groups = db['Groups']

#functions -------------------------------
def render_template(filename, **kwargs): #root = root
    #given filename in this directory
    #print('Where are we: ' + str(os.getcwd()))
    os.chdir(root + '/templates')
    #print('How About Now: ' + str(os.getcwd()))
    try:
        f = open(filename, 'r')
        myFile = f.read()
        f.close()
    except:
        print('filename '+ filename + ' not found in ' + os.getcwd())
        raise ValueError('filename '+ filename + ' not found in ' + os.getcwd())
    for key, value in kwargs.items():
        print(key,value)
        if type(key) == type('This is A String'):
            myFile = myFile.replace('{{' + key + '}}', str(value))
        else:
            print('404 Known Internal Server Error')
            raise(ValueError('Key value pair for templates must be strings'))

    #includes for first level embedded templates
    while True:
        if '{{include' in myFile:
            Before, throw, save = myFile.partition('{{include')
            save, throw, After = save.partition('}}')
            save = save.strip(" '") 
            # print(save)
            try:
                f = open(save, 'r')
                include = f.read()
                f.close()
            except:
                print('includes:' + 'filename '+ save + ' not found in ' + os.getcwd())
                raise ValueError('includes:' + 'filename '+ save + ' not found in ' + os.getcwd())
            myFile = Before + include + After
        else:
            break
            
    print(myFile)

def getInput(FieldStorage, *args): #returns the value of a bunch of key value pair, if not found, returns empty string//
    inputs = []
    eles = FieldStorage
    for i in args:
        inputs.append(str(eles.getfirst(i,'')))
    return inputs
data = cgi.FieldStorage()
# app routes --------------------------------------------------------------------------------


#original DB
# import pickle

# def GetDB(): #get info from DB / makes the DB + return empty dict
#     #{username: {email: blahblah, pwd: blahblah}}

#     os.chdir('/home/students/2022/jjiang20')
#     if os.path.exists('IntroFinalDB.p'):
#         f = open('IntroFinalDB.p', 'rb')
#         masterDB = pickle.load(f)
#         f.close()
#     else:
#         masterDB = {}
#         f = open('IntroFinalDB.p', 'wb+')
#         pickle.dump(masterDB, f)
#         f.close()
#     return masterDB
#idk if its needed
# def GetEmails(): #get list of emails that are linked with accounts
#     os.chdir('/home/students/2022/jjiang20')
#     if os.path.exists('IntroFinalEmailDB.p'):
#         f = open('IntroFinalDB.p', 'rb')
#         emailDB = pickle.load(f)
#         f.close()
#     else:
#         emailDB = []
#         f = open('IntroFinalEmailDB.p', 'wb+')
#         pickle.dump(emailDB, f)
#         f.close()
#     return emailDB


#figuring out the requested path 
# ~/jjiang20@moe.stuy.edu/main.py?path=login/game



# steps = path.split('/')
# for i in steps: #going down the path
#     if i == 'login':
#         render_template('login.html')
# if there is a path
if 'PATH_INFO' in os.environ.keys():
   path = str(os.environ['PATH_INFO'])
   #print(path.split('/')[1:])
   pathParts = path.split('/')[1:]
   
   if pathParts[0] == 'login':
       render_template('login.html')
else:
    render_template('home.html')


#get login info --------------- // change to match mangodb
[whichForm] = getInput(data, 'whichForm')
if whichForm != '':
    if whichForm == 'Login':
        [username, passward] = getInput(data, 'username', 'pwd')
         #check if its in the DB
        if (users.count_documents({'username':username, 'password': password}) > 0):
            #success
            print('success')
        else:
            #fail
            print('theses Credientials don\'t match our records\nplease try again')

    elif whichForm == 'NewUsers':
        [email, username, passward, cpassward] = getInput(data, 'email', 'username', 'pwd', 'cpwd')
        if passward != cpassward:
            print('Bad Login/Signup Request, passwards don\'t match')
            ValueError('Passwards dont match, wasn\'t stopped by JS')
        else:
            if not (users.count_documents({'username':username}) > 0): #is username taken
                if not (users.count_documents({'email':email}) > 0): #is email taken
                    users.insert_one({
                        'username':username,
                        'password':password,
                        'email':email,
                        'groups':[]
                        })
                    print('success')
                else:
                    #fail
                    print('this email has been taken\nplease try again')
            else:
                #fail
                print('this username has been taken\nplease try again')
    else:
        print('Bad Login/Signup Request')
        ValueError('Bad Login/Signup Request')
   

 # testing for vals of keys
for param in os.environ.keys():
    print("<b>%20s</b>: %s<\br>" % (param, os.environ[param]))






