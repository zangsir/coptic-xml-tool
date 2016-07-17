# coptic-xml-tool

coptic scriptorium xml editor/transcription tool for coptic text, incorporating CodeMirror(https://codemirror.net). 

To configure on server or localhost, simply download the files, and make sure

(1) you have added handlers for python for the directory in the main Apache config file, like:

<code>
<Directory "/Applications/MAMP/htdocs/coptic-xml-tool-repo">
    Options +ExecCGI
    AddHandler cgi-script .py
</Directory>
</code>

(2) you have given executable permission the python scripts.

To start the app, run landing.py and log in with admin or your credentials. 
