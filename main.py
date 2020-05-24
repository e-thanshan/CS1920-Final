#! /usr/bin/python
print('Content-type: text/html\n')

print("hello world!")

import os

def render_template(filename, **kwargs):
    #given filename in this directory
    print('Where are we: ' + str(os.getcwd())
    os.chdir('templates')
    print('How About Now: ' + str(os.getcwd())
    try:
        f = open(filename, 'r')
        myFile = f.read()
    except:
        print ValueError('filename '+ filename + ' not found in ' + os.getcwd())
        raise ValueError('filename '+ filename + ' not found in ' + os.getcwd())
    for key, value in kwargs.items():
        if type(key) == type('This is A String'):
            myFile = myFile.replace('{{' + key + '}}', str(value))
        else:
            print('404 Known Internal Server Error')
            raise(ValueError('Key value pair for templates must be strings'))
    print(myFile)

# app routes
import cgi
import cgitb
cgitb.enable(display=0, logdir='./logdir')

def getInput(*args): #returns the value of a bunch of key value pair, if not found, returns empty string//
    inputs = []
    eles = cgi.FieldStorage()
    for i in args:
        inputs.append(str(eles.getfirst(i,'')))
    return inputs

#figuring out the requested path // WIP
# ~/jjiang20@moe.stuy.edu/main.py?path=home/xxx/xxx

path = getInput('path') 

if path == '': # just main.py -> homepage
    print(render_template('home.html'))

steps = path.split('/')
for i in steps: #going down the path
    if i == home
         







