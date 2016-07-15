#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Import modules for CGI handling 
import cgi, cgitb 
import os
from modules.logintools import login
from modules.configobj import ConfigObj
from modules.pathutils import *
import urllib
from coptic_sql import *



def perform_action(text_content):
    f=open("hwak.txt","w")
    f.write(text_content)
    f.close()


def load_page(theform):
    max_id=generic_query("SELECT MAX(id) AS max_id FROM coptic_docs","")[0][0]
    if theform.getvalue('newdoc'):
        doc_id=theform.getvalue('id')
        perform_action(doc_id)
        doc_name="new document"
        file_name="document"
        assignee="user"
        status="new"
        text_content=""
        js="""<script> var docid = """ + str(doc_id)
        js+=""";localStorage.setItem("docid", docid);"""
        js+="""document.getElementById('zangsir').value = docid;</script>"""


    elif theform.getvalue('id'):

        doc_id=theform.getvalue('id')
        perform_action(doc_id)
        if int(doc_id)>int(max_id):
            doc_name="new document"
            file_name="doc.xml"
            status="new"
            assignee="user"
            
        else:
            text_content = generic_query("SELECT content FROM coptic_docs WHERE id=?",doc_id)[0][0]
            doc_name=generic_query("SELECT name FROM coptic_docs WHERE id=?",doc_id)[0][0]
            file_name=generic_query("SELECT filename FROM coptic_docs WHERE id=?",doc_id)[0][0]
            assignee=generic_query("SELECT assigned FROM coptic_docs WHERE id=?",doc_id)[0][0]
            status=generic_query("SELECT status FROM coptic_docs WHERE id=?",doc_id)[0][0]
            

        js="""<script> var docid = """ + str(doc_id)
        js+=""";localStorage.setItem("docid", docid);"""
        js+="""document.getElementById('zangsir').value = docid;</script>"""
    if theform.getvalue('code'):
        text_content = theform.getvalue('code')
        #max_id=generic_query("SELECT MAX(id) AS max_id FROM coptic_docs","")[0][0]
        if int(doc_id)>int(max_id):
            create_document(doc_name,status,assignee,file_name,text_content)
        else:
            save_changes(doc_id,text_content)

    page= "Content-type:text/html\r\n\r\n"
    page+= urllib.urlopen("editor_codemir.html").read()
    page=page.replace("**content**",text_content)
    page=page.replace("**docname**",doc_name+"("+file_name+")")
    page=page.replace("**assigned**",assignee)
    page=page.replace("**status**",status)
    page=page.replace("**js**",js)

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