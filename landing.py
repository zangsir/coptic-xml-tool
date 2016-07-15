#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import modules for CGI handling 
# Import modules for CGI handling 
import cgi, cgitb 
import os
from modules.logintools import login
from modules.configobj import ConfigObj
from modules.pathutils import *
import urllib
from coptic_sql import *

def cell(text):
    return "\n    <td>" + str(text) + "</td>"

def load_landing():
    docs_list=generic_query("SELECT * FROM coptic_docs","")
    max_id=generic_query("SELECT MAX(id) AS max_id FROM coptic_docs","")[0][0]
    #for each doc in the doc list, just display doc[:-1], since last col is content

    table="""<table>
      <tr>
        <th>id</th>
        <th>doc name</th>
        <th>status</th>
        <th>assigned</th>
        <th>filename</th>
        <th>action</th>
      </tr>"""

    for doc in docs_list:
        row="\n <tr>"
        for item in doc[:-1]:
            
            row+=cell(item)

        button="""<form action=editor.py>"""
        button+="""<input type="hidden" name="id" value="""+str(doc[0])+">"


        button+="""<input type="submit" value="EDIT DOCUMENT">
        </form>
    """
        row+=cell(button)
        row+="\n </tr>"
        table+=row
        
    table+="\n</table>"

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
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
    }

    body{padding:10pt;}

    </style>
    </head>
    <body>

    <h1 >Coptic XML transcription editor</h1>
        <p style="border-bottom:groove;"><i>created by Shuo Zhang and Amir Zeldes</i></p>

    <h2>Welcome!</h2>


    """

    create_new = """\n\n\n<form action='editor.py'><input type="hidden" name="id" value="""+str(max_id+1)+">"  
    create_new+=""" <input type="hidden" name="newdoc" value='true'>    """
    #create_new+=""" <input type="hidden" name="maxid" value= """+str(max_id)+">"

    create_new+= """<input type="submit" value="create new document"> </form>"""

    page+=table
    page+="<br><br>"
    page+=create_new
    page+='\n</body>\n</html>'

    return page





def open_main_server():
    thisscript = os.environ.get('SCRIPT_NAME', '')
    action = None
    theform = cgi.FieldStorage()
    scriptpath = os.path.dirname(os.path.realpath(__file__)) + os.sep
    userdir = scriptpath + "users" + os.sep
    action, userconfig = login(theform, userdir, thisscript, action)
    print load_landing()


open_main_server()




