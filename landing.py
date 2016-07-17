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
from modules.coptic_sql import *


def cell(text):
    return "\n    <td>" + str(text) + "</td>"

def get_max_id():
    #get current max of existing records in the db
    current_max=generic_query("SELECT MAX(id) AS max_id FROM coptic_docs",())[0][0]
    #set the max key for auto_increment of id to that value
    generic_query("UPDATE sqlite_sequence SET seq=? WHERE name=?",(current_max,"coptic_docs"))
    return current_max




def load_landing(theform):
    if theform.getvalue('deletedoc'):
        docid=theform.getvalue('id')
        delete_doc(docid)

    #docs_list=generic_query("SELECT * FROM coptic_docs","")
    docs_list=generic_query("SELECT coptic_docs.id,name,status,username,filename FROM coptic_docs JOIN users ON coptic_docs.assignee_users_id=users.id",())

    max_id=get_max_id()
    
    #for each doc in the doc list, just display doc[:-1], since last col is content

    table="""<table>
      <tr>
        <th>id</th>
        <th>doc name</th>
        <th>status</th>
        <th>assigned</th>
        <th>filename</th>
        <th>editing</th>
        <th>deletion</th>
      </tr>"""

    for doc in docs_list:
        row="\n <tr>"
        for item in doc:
            
            row+=cell(item)
        id=str(doc[0])
        #edit document
        button_edit="""<form action=editor.py method="post">"""
        id_code="""<input type="hidden" name="id"  value="""+id+">"
        button_edit+=id_code
        button_edit+="""<input type="submit" value="EDIT DOCUMENT"></form>    """

        #delete document
        button_delete="""<form action=landing.py method="post">"""
        button_delete+=id_code
        button_delete+="""<input type='submit' name='deletedoc'  value='DELETE DOCUMENT'></form>"""

        row+=cell(button_edit)
        row+=cell(button_delete)
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

    create_new_doc = """\n\n\n<form action='editor.py'><input type="hidden" name="id" value="""+str(max_id+1)+">"  
    create_new_doc+=""" <input type="hidden" name="newdoc" value='true'>    """
    create_new_doc+= """<input type="submit" value="create new document"> </form>"""


    page+=table
    page+="<br><br>"
    page+=create_new_doc
    page+='\n</body>\n</html>'
    
    return page





def open_main_server():
    thisscript = os.environ.get('SCRIPT_NAME', '')
    action = None
    theform = cgi.FieldStorage()
    scriptpath = os.path.dirname(os.path.realpath(__file__)) + os.sep
    userdir = scriptpath + "users" + os.sep
    action, userconfig = login(theform, userdir, thisscript, action)
    print load_landing(theform)




open_main_server()




