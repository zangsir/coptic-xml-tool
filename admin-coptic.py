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

def load_admin(theform):
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
    

    #page+="""<h2> User Management </h2>"""

    #a list of all users
    page += '''<h2>User Management</h2>
    <table id="doc_assign">
    <tr>
    <td><p>Users:</p>
    <select id="userlist_select" multiple="multiple" size="10" class="doclist">
    '''
    scriptpath = os.path.dirname(os.path.realpath(__file__)) + os.sep
    userdir = scriptpath + "users" + os.sep

    userfiles = [ f for f in listdir(userdir) if isfile(join(userdir,f)) ]
    for userfile in sorted(userfiles):
        if userfile != "config.ini" and userfile != "default.ini" and userfile != "admin.ini" and userfile.endswith(".ini"):
            userfile = userfile.replace(".ini","")
            page += '<option value="' + userfile + '.ini">'+userfile+'</option>'
    
    page+="</select></td></tr></table>"



    #add user
    #delete users

    page+="<h2>Database management</h2>"
    #init database, setup_db, wipe all documents




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



