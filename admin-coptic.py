#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi, cgitb 
import os
from os.path import isfile, join
from os import listdir
from modules.logintools import login
from modules.configobj import ConfigObj
from modules.pathutils import *
import urllib
from modules.coptic_sql import *



def perform_action(text_content, logging=True):
    #this is used to write information into a text file to serve as a debugging tool and log
    #change logging=True to start logging
    if logging:
        f=open("hwak.txt","a")
        f.write('\n')
        f.write(text_content)
        f.close()

def write_user_file(username,password):
    #this is used to write information into a text file to serve as a debugging tool and log
    #change logging=True to start logging
    userdir="users/"
    f=open(userdir+username+'.ini',"w")
    f.write('username='+username)
    f.write('password='+password)

    f.close()

def load_admin(theform):

    if theform.getvalue('user_delete'):
        userdir='users/'
        user_del_file=theform.getvalue('user_delete')
        user_del=user_del_file.split('.ini')[0]
        perform_action(user_del)
        delete_user(user_del)
        #need to also delete the user.ini file
        os.remove(userdir+user_del_file)

    if theform.getvalue('create_user'):
        perform_action('create user')
        username=theform.getvalue('username')
        password=theform.getvalue('password')
        #create user in database
        create_user(username)
        #need to write a user file for login tools
        write_user_file(username,password)

    if theform.getvalue('init_db'):
        perform_action('init db')

    page= "Content-type:text/html\r\n\r\n"
    page+="""

    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width:400pt;
    }

    td, th {
        
        text-align: left;
        padding: 8px;
    }

    body{padding:10pt;}

    </style>
    </head>
    <body>

    <h1 >Coptic XML transcription editor</h1> 
        <p style="border-bottom:groove;"><i>administration and user management</i> | <a href="landing.py">back to document list</a> </p>
    
    
    

    """
    page+="""<form action="admin-coptic.py" method='post'>"""

    #page+="""<h2> User Management </h2>"""

    #a list of all users
    page += '''<h2>User Management</h2>
    
    
    <p><b>Select users to delete:</b></p>
    <select id="userlist_select" name='user_delete' class="doclist">
    '''
    scriptpath = os.path.dirname(os.path.realpath(__file__)) + os.sep
    userdir = scriptpath + "users" + os.sep

    userfiles = [ f for f in listdir(userdir) if isfile(join(userdir,f)) ]
    for userfile in sorted(userfiles):
        if userfile != "config.ini" and userfile != "default.ini" and userfile != "admin.ini" and userfile.endswith(".ini"):
            userfile = userfile.replace(".ini","")
            page += '<option value="' + userfile + '.ini">'+userfile+'</option>'
    
    page+="</select>"

    
    page+="""</br></br><input type="submit" value='delete user'>
    </form>"""

    #add user

    page+="""</br><b>Enter user info to create new user:</b></br><form action='admin-coptic.py' method='post'>
    username <input type='text' name='username'> </br>
    password <input type='text' name='password'> 
    </br></br><input type='hidden' name='create_user' value='true'><input type='submit' value='create user'></form>"""



    

    page+="<br><br><h2>Database management</h2>"
    #init database, setup_db, wipe all documents

    page+="""<form action='admin-coptic.py' method='post'>
    warning: this will wipe the database!
    <br><input type='hidden' name='init_db' value='true'><input type='submit' value='init database'></form>"""



    page+="</body></html>"
 

    return page



def open_main_server():
    thisscript = os.environ.get('SCRIPT_NAME', '')
    action = None
    theform = cgi.FieldStorage()
    scriptpath = os.path.dirname(os.path.realpath(__file__)) + os.sep
    userdir = scriptpath + "users" + os.sep
    action, userconfig = login(theform, userdir, thisscript, action)
    print load_admin(theform)




open_main_server()



