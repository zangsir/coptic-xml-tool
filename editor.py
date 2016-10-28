#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Import modules for CGI handling 
import cgi, cgitb 
import os
from os import listdir
from modules.logintools import login
from modules.configobj import ConfigObj
from modules.pathutils import *
import urllib
from modules.coptic_sql import *
from os.path import isfile, join
from modules.dataenc import pass_dec, pass_enc




def make_options(**kwargs):
    if "file" in kwargs:
        names = open(kwargs["file"],'r').read().replace("\r","").split("\n")
        #print len(names)
        names = list(name[:name.find("\t")] for name in names)
    elif "names" in kwargs:
        names = kwargs[names]
    selected = kwargs["selected"] if "selected" in kwargs else None
    options=""
    for name in names:
        if name!='':
            options+='<option value=%s>\n' %name
    return options


def cell(text):
    return "\n    <td>" + str(text) + "</td>"


def perform_action(text_content, logging=True):
    #this is used to write information into a text file to serve as a debugging tool and log
    #change logging=True to start logging
    if logging:
        f=open("hwak.txt","a")
        f.write('\n')
        f.write(text_content.encode("utf8"))
        f.close()


def print_meta(doc_id):
    meta = generic_query("SELECT * FROM metadata WHERE docid=?",(doc_id,))
    #docid,metaid,key,value - four cols
    table="""<table>"""
    for item in meta:
        #each item appears in one row of the table
        row="\n <tr>"
        metaid=str(item[1])
        id=str(doc_id)
        for i in item[2:]:
            row+=cell(i)

    #delete meta
        metaid_code="""<button type="hidden" name="metaid"  value="""+metaid+"> delete </button>"
        #id_code="""<input type="hidden" name="id"  value="""+id+">"
        perform_action(metaid_code)

        button_delete=""
        button_delete+=metaid_code
        #button_delete+=id_code
        #button_delete+="""<input type='submit' name='deletemeta'  value='DELETE'>"""
        row+=cell(button_delete)
        row+="\n </tr>"
        table+=row
    table+="\n</table>"
    return table


def push_to_git(username,password,path,account,repo,message):
    import github3
    files_to_upload = [path]
    gh = github3.login(username=username, password=password)
    repository = gh.repository(account, repo)
    for file_info in files_to_upload:
        with open(file_info, 'rb') as fd:
            contents = fd.read()
        push_status = repository.create_file(
            path=file_info,
            message=message.format(file_info),
            content=contents,
        )
    return type(push_status)!=github3.null.NullObject


def serialize_file(text_content,file_name):
    f=open(file_name,'w')
    f.write(text_content.encode("utf8"))
    f.close()



def get_git_credentials(user,admin):
    if admin==0:
        return
    scriptpath = os.path.dirname(os.path.realpath(__file__)) + os.sep
    userdir = scriptpath + "users" + os.sep
    userfile = userdir + user + '.ini'
    perform_action(userfile,True)
    f=open(userfile,'r').read().split('\n')
    user_dict={}
    for line in f:
        if line!='':
            l=line.split(' = ')
            user_dict[l[0]]=l[1]
    git_username=user_dict['git_username']
    git_password=pass_dec(user_dict['git_password'])
    perform_action(git_password[0],True)
    return git_username,git_password[0]


def load_page(user,admin,theform):
    perform_action('===========new=============')
    max_id=generic_query("SELECT MAX(id) AS max_id FROM coptic_docs","")[0][0]
    text_content=""
    if theform.getvalue('newdoc'):
        #when creating new document from landing page, a new id as max_id+1 is passed
        doc_id=theform.getvalue('id')
        perform_action(doc_id)
        doc_name="new document"
        file_name="new_document.xml"
        assignee="default_user"
        status="editing"
        text_content=""
        js="""<script> var docid = """ + str(doc_id)
        js+=""";localStorage.setItem("docid", docid);"""
        js+="""document.getElementById('zangsir').value = docid;</script>"""

    
    elif theform.getvalue('id'):
        #this should come from either creating new doc or 'editing doc' in landing page
        doc_id=theform.getvalue('id')
        perform_action(doc_id)

        create_doc=0
        #creating new doc case, assign some default values
        if int(doc_id)>int(max_id):
            doc_name="new document"
            file_name="new_document.xml"
            status="editing"
            assignee="default_user"
            text_content=""
            doc_saved=False
            #if one of the four forms is edited, then we create the doc, otherwise nothing happens(user cannot fill in nothing and create the doc)
            if theform.getvalue('edit_docname'):
                docname=theform.getvalue('edit_docname')
                if docname!='new document':
                    perform_action('edit docname new'+docname)
                    create_document(doc_name,status,assignee,file_name,text_content)
                    update_docname(doc_id,docname)
                    doc_saved=True

            if theform.getvalue('edit_filename'):
                filename=theform.getvalue('edit_filename')
                if filename!='new_document.xml':
                    perform_action('edit filename new'+filename)
                    create_document(doc_name,status,assignee,file_name,text_content)
                    update_filename(doc_id,filename)
                    doc_saved=True
                

            if theform.getvalue('edit_status'):
                #if not (theform.getvalue('edit_docname') or theform.getvalue('edit_filename')):
                newstatus=theform.getvalue('edit_status')
                if newstatus!='editing':
                    perform_action('edit status new '+newstatus)
                    create_document(doc_name,status,assignee,file_name,text_content)
                    update_status(doc_id,newstatus)
                    doc_saved=True
                
            if theform.getvalue('edit_assignee'):
                #if not (theform.getvalue('edit_docname') or theform.getvalue('edit_filename')):
                newassignee_username=theform.getvalue('edit_assignee')
                if newassignee_username!="default_user":
                    create_document(doc_name,status,assignee,file_name,text_content)
                    perform_action('edit ass new '+str(newassignee_username))
                    update_assignee(doc_id,newassignee_username)
                    doc_saved=True
            if doc_saved==True:        
                text_content = generic_query("SELECT content FROM coptic_docs WHERE id=?",(doc_id,))[0][0]
                doc_name=generic_query("SELECT name FROM coptic_docs WHERE id=?",(doc_id,))[0][0]
                file_name=generic_query("SELECT filename FROM coptic_docs WHERE id=?",(doc_id,))[0][0]
                assignee=generic_query("SELECT assignee_username FROM coptic_docs WHERE id=?",(doc_id,))[0][0]
                status=generic_query("SELECT status FROM coptic_docs WHERE id=?",(doc_id,))[0][0]
                
        #after clicking edit in landing page, editing existing doc case, get the values from the db. pull the content from db to be displayed in the editor window.
        else:
            if theform.getvalue('edit_docname'):
                docname=theform.getvalue('edit_docname')
                perform_action('edit docname existing')
                update_docname(doc_id,docname)
            if theform.getvalue('edit_filename'):
                filename=theform.getvalue('edit_filename')
                perform_action('edit filename existing')
                update_filename(doc_id,filename)
            if theform.getvalue('edit_status'):
                newstatus=theform.getvalue('edit_status')
                perform_action('edit status existing')
                update_status(doc_id,newstatus)
            if theform.getvalue('edit_assignee'):
                newassignee_username=theform.getvalue('edit_assignee')
                perform_action('edit ass exsiting')
                update_assignee(doc_id,newassignee_username)
            text_content = generic_query("SELECT content FROM coptic_docs WHERE id=?",(doc_id,))[0][0]
            doc_name=generic_query("SELECT name FROM coptic_docs WHERE id=?",(doc_id,))[0][0]
            file_name=generic_query("SELECT filename FROM coptic_docs WHERE id=?",(doc_id,))[0][0]
            assignee=generic_query("SELECT assignee_username FROM coptic_docs WHERE id=?",(doc_id,))[0][0]
            status=generic_query("SELECT status FROM coptic_docs WHERE id=?",(doc_id,))[0][0]
            

        js="""<script> var docid = """ + str(doc_id)
        js+=""";localStorage.setItem("docid", docid);"""
        js+="""document.getElementById('zangsir').value = docid;</script>"""
    #in the case of reloading after hitting 'save', either create new doc into db, or update db
    #codemirror sends the form with its code content in it before 'save' so we just display it again
    if theform.getvalue('code'):
        text_content = theform.getvalue('code')
        text_content = text_content.replace("\r","")
        text_content = unicode(text_content.decode("utf8"))
        perform_action("<start content>")
        perform_action(text_content)
        perform_action('<end content>')
        #max_id=generic_query("SELECT MAX(id) AS max_id FROM coptic_docs","")[0][0]
        if int(doc_id)>int(max_id):
            perform_action('create doc existing')
            create_document(doc_name,status,assignee,file_name,text_content)
        else:
            save_changes(doc_id,text_content)

    git_status=False
    if theform.getvalue('push_git'):
        perform_action('push',True)
        text_content = generic_query("SELECT content FROM coptic_docs WHERE id=?", (doc_id,))[0][0]
        file_name = generic_query("SELECT filename FROM coptic_docs WHERE id=?", (doc_id,))[0][0]
        perform_action(file_name,True)
        serialize_file (text_content,file_name)
        git_account='zangsir'
        git_repo='coptic-xml-tool'
        git_username,git_password=get_git_credentials(user,admin)
        file_path="uploaded_commits/"
        message="try commit random file"

        git_status=push_to_git(git_username,git_password,file_name,git_account,git_repo,message)
        perform_action(str(git_status),True)


    #editing options
    #docname
    edit_docname = """<input type='text' name='edit_docname' value='%s'> <input type='submit' value='change'>""" %doc_name
    #filename
    edit_filename = """<input type='text' name='edit_filename' value='%s'> <input type='submit' value='change'>""" %file_name
    #push_git = """<input type='hidden' name='push_git' value='yes'> <input type='submit' value='Push'>"""
    push_git = """<button type="hidden" name="push_git"  value=None> Push </button>"""
    if git_status == True:
        push_git+="""<p style='color:red;'>pushed to remote repo successfully</p>"""
    #status
    #which one is selected?
    sel_edit=""
    sel_review=""
    if status=="editing":
        sel_edit="selected"
    elif status=="review":
        sel_review="selected"

    edit_status="""<select name="edit_status">  
    <option value="editing" %s>editing</option>
    <option value='review' %s> review </option></select>    
    <input type='submit' value='change'>""" %(sel_edit,sel_review)
    
    #assignee
    
    #user_list=generic_query("SELECT * FROM users","")
    

    #get user_list from the logintools instead
    user_list=[]
    scriptpath = os.path.dirname(os.path.realpath(__file__)) + os.sep
    userdir = scriptpath + "users" + os.sep

    userfiles = [ f for f in listdir(userdir) if isfile(join(userdir,f)) ]
    for userfile in sorted(userfiles):
        if userfile != "config.ini" and userfile != "default.ini" and userfile != "admin.ini" and userfile.endswith(".ini"):
            userfile = userfile.replace(".ini","")
            user_list.append(userfile)
    perform_action(str(user_list))


    edit_assignee="""<select name="edit_assignee">"""
    for user in user_list:
        assignee_select=""
        user_name=user
        if user_name==assignee:
            assignee_select="selected"
        edit_assignee+="""<option value='""" + user_name + "' %s>" + user_name + """</option>""" 
        edit_assignee=edit_assignee%assignee_select
    edit_assignee+="</select><input type='submit' value='change'>"

    #meta data
    if theform.getvalue('metakey'):
        metakey=theform.getvalue('metakey')
        metavalue=theform.getvalue('metavalue')
        perform_action(metakey)
        perform_action(metavalue)
        save_meta(doc_id,metakey,metavalue)
    if theform.getvalue('metaid'):
        perform_action('========delete meta')
        metaid=theform.getvalue('metaid')
        perform_action(metaid)
        delete_meta(metaid)
    metadata=print_meta(doc_id)



    page= "Content-type:text/html\r\n\r\n"
    page+= urllib.urlopen("editor_codemir.html").read()
    page=page.replace("**content**",text_content)
    #page=page.replace("**docname**",doc_name)
    #page=page.replace("**filename**",file_name)
    #page=page.replace("**assigned**",assignee)
    #page=page.replace("**status**",status)
    page=page.replace("**editdocname**",edit_docname)
    page=page.replace("**editstatus**",edit_status)
    page=page.replace("**editfilename**",edit_filename)
    page=page.replace("**editassignee**",edit_assignee)
    page=page.replace("**metadata**",metadata)
    if int(admin)>0:
        page=page.replace("**github**",push_git)
    else:
        page = page.replace("**github**", '')
    page=page.replace("**js**",js)

    return page




def open_main_server():
    thisscript = os.environ.get('SCRIPT_NAME', '')
    action = None
    theform = cgi.FieldStorage()
    scriptpath = os.path.dirname(os.path.realpath(__file__)) + os.sep
    userdir = scriptpath + "users" + os.sep
    action, userconfig = login(theform, userdir, thisscript, action)
    user = userconfig["username"]
    admin = userconfig["admin"]
    print load_page(user,admin,theform).encode("utf8")


open_main_server()