from flask import Flask, render_template
from flask import Flask, redirect, url_for, request
import sqlite3

app = Flask(__name__)

@app.route('/view', methods = ['POST'])
def view():
    if request.method == 'POST':
        title=request.form['title']
        content=request.form['content']
        dict = {title:content}

        con = sqlite3.connect("message.db", isolation_level=None) 
        con.row_factory = sqlite3.Row
        cur = con.cursor() 
        cur.execute("select * from comments where VIEW=0 and TITLE='%s'"%(title))
        coms = cur.fetchall()
        return render_template("view.html",result = dict,comResult=coms)

@app.route('/delete', methods = ['POST'])
def delete():
    if request.method == 'POST':
        title=request.form['title']
        con = sqlite3.connect("message.db", isolation_level=None) 
        cur = con.cursor() 
        cur.execute("update messages set VIEW=1 where TITLE= '%s'"%(title))
        con.row_factory = sqlite3.Row
        cur = con.cursor() 
        cur.execute("select * from messages where VIEW=0")
        rows = cur.fetchall()
        return render_template("main.html",row = rows)

@app.route('/addComment', methods = ['POST'])
def addComment():
    title=request.form['title']
    content=request.form['content']
    dict = {title:content} 

    #comment 추가
    comment = request.form['comment'] 
    con = sqlite3.connect("message.db", isolation_level=None) 
    cur = con.cursor() 
    cur.execute("INSERT INTO comments(TITLE, COMMENT, VIEW) VALUES(?,?,?)",(title,comment,0))

    #view 데이터 불러오기
    con = sqlite3.connect("message.db", isolation_level=None) 
    con.row_factory = sqlite3.Row
    cur = con.cursor() 
    cur.execute("select * from comments where VIEW=0 and TITLE='%s'"%(title))
    coms = cur.fetchall()
    return render_template("view.html",result = dict,comResult=coms)

@app.route('/deleteComment', methods = ['POST'])
def deleteComment():
    if request.method == 'POST':
        title=request.form['title']
        comment=request.form['comment']

        con = sqlite3.connect("message.db", isolation_level=None) 
        cur = con.cursor() 
        cur.execute("update comments set VIEW=1 where COMMENT='%s'"%(comment))

        con = sqlite3.connect("message.db", isolation_level=None) 
        con.row_factory = sqlite3.Row
        cur = con.cursor() 
        cur.execute("select * from messages where VIEW=0")
        rows = cur.fetchall()
        return render_template("main.html",row = rows)
 


@app.route('/editClick', methods = ['POST'])
def editClick():
    if request.method == 'POST':
        title=request.form['title']
        dict = {'title':title}
        return render_template("edit.html",result = dict)

@app.route('/edit', methods = ['POST'])
def edit():
    if request.method == 'POST':
        title=request.form['title']
        newcontent=request.form['newcontent']
        con = sqlite3.connect("message.db", isolation_level=None) 
        cur = con.cursor() 
        cur.execute("update messages set CONTENT='%s' where TITLE= '%s'"%(newcontent,title))
        # con.close
        # return render_template("main.html",msg = "check") 
        con.row_factory = sqlite3.Row
        cur = con.cursor() 
        cur.execute("select * from messages where VIEW=0")
        rows = cur.fetchall()
        return render_template("main.html",row = rows)

@app.route('/main') 
def listUpdate():
    con = sqlite3.connect("message.db", isolation_level=None) 
    con.row_factory = sqlite3.Row
    cur = con.cursor() 
    cur.execute("select * from messages")
    rows = cur.fetchall()
    return render_template("main.html",row = rows)

@app.route('/',methods = ['POST']) 
def addnew():
    if request.method == 'POST':
        title = request.form['title'] 
        content = request.form['content'] 
            #check = 0
        con = sqlite3.connect("message.db", isolation_level=None) 
        cur = con.cursor() 
        cur.execute("INSERT INTO messages(TITLE, CONTENT, VIEW) VALUES(?,?,?)",(title,content,0))
        # con.close
        # return render_template("main.html",msg = "check") 
        con.row_factory = sqlite3.Row
        cur = con.cursor() 
        cur.execute("select * from messages where VIEW=0")
        rows = cur.fetchall()
        return render_template("main.html",row = rows)
            

@app.route('/post',methods = ['POST']) 
def score():
    if request.method == 'POST':
        score = request.form
        return render_template("post.html",score=score)

@app.route('/') 
def list():
    con = sqlite3.connect("message.db", isolation_level=None) 
    con.row_factory = sqlite3.Row
    cur = con.cursor() 
    cur.execute("select * from messages where VIEW=0")
    rows = cur.fetchall()
    return render_template("main.html",row = rows)

if __name__ == '__main__':
        app.run(debug = True)