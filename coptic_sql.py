#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Data access functions to read from and write to the SQLite backend.
"""

import sqlite3
from modules.rstweb_reader import *
import codecs
import os
import re


def setup_db():
    dbpath = os.path.dirname(os.path.realpath(__file__)) + os.sep +".."+os.sep+"coptic.db"
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    # Drop tables if they exist
    cur.execute("DROP TABLE IF EXISTS coptic_docs")
    cur.execute("DROP TABLE IF EXISTS users")
    conn.commit()
    
    # Create tables
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username text)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS coptic_docs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, status text,assignee_users_id INTEGER ,filename text, content text,FOREIGN KEY(assignee_users_id) REFERENCES users(id))''')

    
    conn.commit()
    conn.close()
    

def create_document(name,status,assigned_id,filename,content):
    content=content.replace('"',"'")
    dbpath = os.path.dirname(os.path.realpath(__file__)) + os.sep +".."+os.sep+"coptic.db"
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    cur.execute('''INSERT INTO {tn}(name,status,assignee_users_id,filename,content) VALUES({name},{status},{assigned},{filename},{content})'''.format(tn="coptic_docs",name='"'+name+'"',status='"'+status+'"',assigned='"'+assigned_id+'"',filename='"'+filename+'"',content='"'+content+'"'))
    conn.commit()
    conn.close()


def generic_query(sql,params):
    #generic_query("DELETE FROM rst_nodes WHERE doc=? and project=?",(doc,project))
    
    dbpath = os.path.dirname(os.path.realpath(__file__)) + os.sep +".."+os.sep+"coptic.db"
    conn = sqlite3.connect(dbpath)
    
    with conn:
        cur = conn.cursor()
        cur.execute(sql,params)
        
        rows = cur.fetchall()
        return rows






def save_changes(id,content):
    """save change from the editor"""
    generic_query("UPDATE coptic_docs SET content=? WHERE id=?",(content,id))


def update_assignee(id,assignee):
    generic_query("UPDATE coptic_docs SET assigned=? WHERE id=?",(assignee,id))

def update_status(id,status):
    generic_query("UPDATE coptic_docs SET status=? WHERE id=?",(status,id))

def update_docname(id,docname):
    generic_query("UPDATE coptic_docs SET name=? WHERE id=?",(docname,id))


def update_filename(id,filename):
    generic_query("UPDATE coptic_docs SET filename=? WHERE id=?",(filename,id))


def create_user(username):
    dbpath = os.path.dirname(os.path.realpath(__file__)) + os.sep +".."+os.sep+"coptic.db"
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    cur.execute('''INSERT INTO {tn}(username) VALUES({username})'''.format(tn="users",username='"'+username+'"'))
    conn.commit()
    conn.close()










