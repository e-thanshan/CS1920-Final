#! /usr/bin/python
print('Content-type: text/html\n')

print("hello world!")

import os

def render_template(parameter_list, **kwargs):
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
        if type(i) == type('This is A String'):
            myFile.replace('{{' + key + '}}', value)
        else:
            print('This Arg is not acceptable')
            raise(ValueError('This Arg is not acceptable'))
    print(myFile)
    
