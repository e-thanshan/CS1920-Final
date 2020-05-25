#! /usr/bin/python
print('Content-type: text/html\n')

# print("hello world!")

import os

def render_template(filename, **kwargs):
    #given filename in this directory
    #print('Where are we: ' + str(os.getcwd()))
    os.chdir('templates')
    #print('How About Now: ' + str(os.getcwd()))
    try:
        f = open(filename, 'r')
        myFile = f.read()
        f.close()
    except:
        print('filename '+ filename + ' not found in ' + os.getcwd())
        raise ValueError('filename '+ filename + ' not found in ' + os.getcwd())
    for key, value in kwargs.items():
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

# app routes
import cgi

import cgitb
cgitb.enable(display=0, logdir='./logdir')

def GetDB(): #get info from DB / makes the DB + return empty dict
    import pickle
    os.chdir('/home/students/2022/jjiang20')
    if os.path.exists('IntroFinalDB.p'):
        f = open('IntroFinalDB.p', 'rb')
        masterDB = pickle.load(f)
        f.close()
    else:
        masterDB = {}
        f = open('IntroFinalDB.p', 'wb+')
        pickle.dump(masterDB, f)
        f.close()
    return masterDB

def getInput(FieldStorage, *args): #returns the value of a bunch of key value pair, if not found, returns empty string//
    inputs = []
    eles = FieldStorage
    for i in args:
        inputs.append(str(eles.getfirst(i,'')))
    return inputs

#figuring out the requested path // WIP
# ~/jjiang20@moe.stuy.edu/main.py?path=login/game
data = cgi.FieldStorage()
[path] = getInput(data, 'path') 

if path == '': # just main.py -> homepage
    render_template('home.html')

# steps = path.split('/')
# for i in steps: #going down the path
#     if i == 'login':
#         render_template('login.html')
# if there is a path
if 'PATH_INFO' in os.environ.keys():
   print('starting')
   path = str(os.environ['PATH_INFO'])
   print(path.split('/')[1:])
   pathParts = path.split('/')[1:]
   if pathParts[0] == 'login':
       render_template('login.html')
   print('done')


#get login info
[whichForm] = getInput(data, 'whichForm')
if whichForm != '':
    if whichForm == 'Login':
        [username, passward] = getInput(data, 'username', 'pwd')
    elif whichForm == 'NewUsers':
        pass
    else:
        ValueError('Bad Login/Signup Request')
    #check if its in the DB
    masterDB = GetDB()
    if masterDB[username] == passward:
        #success
        print('success')
    else:
        #fail
        print('theses Credientials don\'t match our records\nplease try again')


# # testing for vals of keys
# for param in os.environ.keys():
#    print("<b>%20s</b>: %s<\br>" % (param, os.environ[param]))






