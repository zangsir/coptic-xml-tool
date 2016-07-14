#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import modules for CGI handling 
import cgi, cgitb 
import os
from modules.logintools import login
from modules.configobj import ConfigObj
from modules.pathutils import *
import urllib

#this action will be performed upon receiving the data from the xml editor, such as saving the file, or write to db
def perform_action(text_content):
    f=open("hwak.txt","w")
    f.write(text_content)
    f.close()


    

def load_page(theform): 
    # Create instance of FieldStorage 
    #form = cgi.FieldStorage() 
    if theform.getvalue('code'):
        text_content = theform.getvalue('code')
        perform_action(text_content)
    else:
       text_content = ""
    page= "Content-type:text/html\r\n\r\n"
    page+= urllib.urlopen("try2.html").read()
    page=page.replace("**content**",text_content)
    return page




def open_main_server():
    thisscript = os.environ.get('SCRIPT_NAME', '')
    action = None
    theform = cgi.FieldStorage()
    scriptpath = os.path.dirname(os.path.realpath(__file__)) + os.sep
    userdir = scriptpath + "users" + os.sep
    action, userconfig = login(theform, userdir, thisscript, action)
    print load_page(theform)


open_main_server()