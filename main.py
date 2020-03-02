from flask import render_template, Flask, request, session, redirect ,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import numpy as np
import pymysql

pymysql.install_as_MySQLdb()#or  you can directly install MySQLdb using pip install MySQL-python
j=open("config.json","r")
p=json.load(j)

test=0
app=Flask(__name__)
app.secret_key='super-secret-hai'
if test==1:
    app.config['SQLALCHEMY_DATABASE_URI']=p["params"]["uri_for_sqlalchemy"]
if test==0:
        app.config['SQLALCHEMY_DATABASE_URI']=p["params"]["uri_for_sqlalchemy2"]

db=SQLAlchemy(app)

class Books(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=True)
    rollno=db.Column(db.String(15),nullable=True)
    book=db.Column(db.String(999),nullable=False)
    author=db.Column(db.String(63),nullable=True)
    more=db.Column(db.String(100),nullable=True)
    date=db.Column(db.String(12),nullable=True)
#===========================================================
class Booksv2(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=True)
    rollno=db.Column(db.String(15),nullable=True)
    author=db.Column(db.String(63),nullable=True)
    more=db.Column(db.String(100),nullable=True)
    date=db.Column(db.String(12),nullable=True)

class Books_in_lib(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    bookid=db.Column(db.String(15),nullable=False)
    bookname=db.Column(db.String(30),nullable=False)
    total_we_have=db.Column(db.String(15),nullable=False)
    remaining_books=db.Column(db.String(15),nullable=False)
    trade_code=db.Column(db.String(36),nullable=False)
    trade=db.Column(db.String(50),nullable=False)

class My_rel(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    foreignkey=db.Column(db.String(15),nullable=False)
    bookname=db.Column(db.String(30),nullable=False)
    book_id=db.Column(db.String(15),nullable=False)
#=================================================================

@app.route("/")
def landing_page():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")



#admin login--------------------------------------------
@app.route("/admin",methods=['GET','POST'])
def admin():
    try:
        data=Books_in_lib.query.all()
        data=list(data)
             
        if('user' in session and session['user']==p['params']['id']):
            return(render_template("libraryadmin.html",data=data))
            
        if(request.method=='POST'):
            admin_id=request.form.get('id')
            admin_pass=request.form.get('pass')
            sno=request.form.get('sno')
            if(admin_id==p['params']['id'] and admin_pass==p['params']['password']):
                session['user']=admin_id
                return(render_template('libraryadmin.html',data=data))
        return(render_template("login.html"))
    except:
        return render_template("404.html")
@app.route("/detail",methods=['POST','GET'])
def s_home():
    try:
        rollno=request.form.get('rollno')
        
        data=Booksv2.query.filter_by(rollno=rollno).first()
        
        z=to_show_only_books_from_db_to_form_box(data.sno)
        y=len(z)
        y=y-1
        return render_template("details.html",name=data.name,rollno=data.rollno,date=data.date,data2=z,y=y)
    except AttributeError:
        return render_template("error.html")


@app.route("/detail@admin",methods=['POST','GET'])
def a_home():
    try:
        rollno=request.form.get('rollno')
        
        data=Booksv2.query.filter_by(rollno=rollno).first()
        
        z=to_show_only_books_from_db_to_form_box(data.sno)
        y=len(z)
        y=y-1
        return render_template("details@admin.html",name=data.name,rollno=data.rollno,date=data.date,data2=z,y=y)
    except AttributeError:
        return render_template("404.html")


@app.route("/admin_home")
def admin_home():
    
    if 'user' in session and session['user']==p['params']['id']:
        data=Books_in_lib.query.filter_by().all()
        return render_template("libraryadmin.html",data=data)
    else:
        return render_template("login.html")


@app.route("/delete/<rollno>",methods=['POST','GET'])
def delete(rollno):
    if('user' in session and session['user']==p['params']['id']):   
        rollno=rollno
        data=Booksv2.query.filter_by(rollno=rollno).first()
        

        var=data.sno
        db2 = pymysql.connect(host='localhost',user='root',passwd='')
        cursor=db2.cursor()
        query = ("use lib_mgmt_test")
        query2="SELECT * FROM `my_rel` WHERE `foreignkey` = %s"
        cursor.execute(query)
        cursor.execute(query2,var)
        z=list(cursor)
        x=len(z)

        count=0
        bookid_prev=[]
        for i in z:
            bookid_prev.append(i[3])
            count=count+1

        bookid_prev=bookid_prev
        '''global data_for_bookid_prev
        data_for_bookid_prev=bookid_prev'''
        
        for i in bookid_prev:
            data2=Books_in_lib.query.filter_by(bookid=i).first()
            a=data2.remaining_books
            
            c=a+1
            data2.remaining_books=c
        
            db.session.commit()
        db.session.delete(data)
        db.session.commit()
        
        #---Till Here -----Till Here -------------------------

        
        return render_template('libraryadmin.html')
    else:
        return render_template('error.html')



@app.route('/logout')  
def logout():  
    if 'user' in session:  
        session.pop('user',None)  
        return render_template("index.html")


#///////////////////////////////student////////////////////////////////////////

@app.route("/student_have_books/<rollno>/<bookid>/<book>")#this routing tell about remaining books in library
def stubooks(rollno,bookid,book):
    dataprev=Booksv2.query.filter_by(rollno=rollno).first()
    foreignkey=dataprev.sno
    iterate_and_savebooks2(rollno,bookid)#functon i create for sorting more than one book in form input
    count_book_remaining(book,bookid)
    return render_template("new_entry.html")#before


def count_book_remaining(book,bookid):
    book=book.split(",")
    bookid=bookid.split(",")
    for x,j in zip(book, bookid):
        data=My_rel.query.filter_by(book_id=j).all()
        count=0
        for i in data:
            count+=1
        students_have=count
        data2=Books_in_lib.query.filter_by(bookid=j).first()
        total_books=data2.total_we_have#total books=a
        remaining=total_books-students_have#c=a-b
        data2.remaining_books=remaining
        db.session.commit()
    
        
#=adder=================v2


#========================================commpleted routing=======================================================




#This routing works for fetching data with using foreign key in table My_rel which have reduntant data
def to_show_only_books_from_db_to_form_box(var):#so it's geting little difficult to fetch using previous request.query.filter_by so i use cursor,pymysql with raw query
    import pymysql
    var=var
    db = pymysql.connect(host='localhost',user='root',passwd='')
    cursor=db.cursor()
    query = ("use lib_mgmt_test")
    query2="SELECT * FROM `my_rel` WHERE `foreignkey` = %s"
    cursor.execute(query)
    cursor.execute(query2,var)
    z=list(cursor)
    x=len(z)

    
    return z#from routing /test to now the work is for searching->fetching->and->showing in form now let's updatae 


############################################################
#updater===================================================v2
@app.route("/test6")
def test6():#>>-----------------------------------------+
    if 'user' in session and session['user']==p['params']['id']:

        return render_template("find.html")
    else:
        return render_template("error.html")
#                                                      |
@app.route("/data_fetch",methods=['GET','POST'])#      |
def data_fetchv2_1():#                                 |
    rollno=request.form.get('rollno')#<<<--------------+
    return redirect(url_for("uu2",rollno=rollno))
#                                              |
#                                              +->>---------+
#                                                           |
@app.route("/updaterv23/<rollno>",methods=['GET','POST'])#   |
def uu2(rollno): # 
    try:                
        #I use global  variable here because I take previous values from database show to user once user update that this function
        # calls again for updation and at that time I need values I stored previously in bookid_prev and for accessing 
        # I nedd to make it global scope :-D                      
        global bookid_prev
        if 'user' in session and session['user']==p['params']['id']:
            if(request.method=='POST'):
                
                name=request.form.get('name')
                rollno=request.form.get("rollno")
                book=request.form.get("book")
                #book_id = request.form.get("book_id")

                author=request.form.get("author")
                more=request.form.get("more_info")
                date=datetime.now()

                if book != "":
                    print(".....................................")
                    json_list = json_converter(p["books_ids"])
                    count = 0
                    count_prev = 0
                    book_Id = ""
                    book = str(book)
                    print("books is",book)
                    for i in book.split(","):
                        count = count + 1
                    count = count - 1
                    for i in book.split(","):
                        i_d = key_finder(json_list, i)
                        print("i is:::::::::::::::::::::::::::::::::",i)
                        print("key is : ....................................::::::::::::::::::",i_d)
                        if count_prev < count:
                            book_Id = book_Id + i_d[0] + ","
                        else:
                            book_Id = book_Id + i_d[0]
                        count_prev = count_prev + 1
                    book_id = book_Id

                else:
                    book_id = request.form.get("book_id")
                    count = 0
                    count_prev = 0
                    book = ""
                    print("book_id is is.......................",book_id)
                    for i in  book_id.split(","):
                        count = count + 1
                    count = count - 1
                    for i in book_id.split(","):
                        print("i is.........................",i)
                        data = Books_in_lib.query.filter_by(bookid=i).first()
                        

                        print("data is.............",data.bookid)
                        if count_prev < count:
                            book = book + data.bookname + ","
                        else:
                            book = book + data.bookname
                        count_prev = count_prev + 1
                    
                delete=Booksv2.query.filter_by(rollno=rollno).first()
                db.session.delete(delete)
                db.session.commit()
                
                
            
            #adding entry 
                entry_in_object=Booksv2(name=name, rollno=rollno,author=author,more=more,date=date)
                
                db.session.add(entry_in_object)
                db.session.commit()
                return redirect(url_for('stubooks2' ,rollno=rollno,bookid=book_id,book=book,bookid_prev=bookid_prev))
        
        data=Booksv2.query.filter_by(rollno=rollno).first()
        z=to_show_only_books_from_db_to_form_box(data.sno)
        y=len(z)
        y=y-1
        #------it's work is to get books id in a var -----------------
        
        var=data.sno
        db2 = pymysql.connect(host='localhost',user='root',passwd='')
        cursor=db2.cursor()
        query = ("use lib_mgmt_test")
        query2="SELECT * FROM `my_rel` WHERE `foreignkey` = %s"
        cursor.execute(query)
        cursor.execute(query2,var)
        z=list(cursor)
        
        x=len(z)

        count=0
        bookid_prev=[]
        for i in z:
            
            bookid_prev.append(i[3])
            count=count+1

        
        bookid_prev=bookid_prev
        #---Till Here -----Till Here -------------------------

        return render_template("update_form.html",data=data,data2=z,y=y)
    except:
        return render_template("404.html")

@app.route("/updater_for_books/<rollno>/<bookid>/<book>/<bookid_prev>",methods=['GET','POST'])#this routing tell about remaining books in library
def stubooks2(rollno,bookid,book,bookid_prev):
    dataprev=Booksv2.query.filter_by(rollno=rollno).first()
    foreignkey=dataprev.sno
    i=1
    while(i==1):
        data=My_rel.query.filter_by(foreignkey=foreignkey).first()
        if data==None:
            return redirect(url_for('zz',rollno=rollno,bookid=bookid,book=book,bookid_prev=bookid_prev))
            break
        
        db.session.delete(data)
        db.session.commit()

    
    
        
@app.route("/zz/<rollno>/<bookid>/<book>/<bookid_prev>")
def zz(rollno,bookid,book,bookid_prev):
    x=book
    y=bookid
    
    iterate_and_savebooks2(rollno,bookid)
    books_counting(y)
    
    books_counting_prev(bookid_prev)
    
    return render_template("find.html")






#searcher==================================================v2



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!testing a temporarily function!!!!!!!!!!!!!!!!!!!!
def books_counting(bookid):
    import pymysql
    
    if type(bookid)==list:
        
        var=bookid
    else:
        var=bookid.split(",")

    
    db = pymysql.connect(host='localhost',user='root',passwd='')
    cursor=db.cursor()
    query = ("use lib_mgmt_test")
    cursor.execute(query)

    for bookid in var:
        query2="SELECT * FROM `my_rel` WHERE `book_id` = %s"#vulernable use ? instead of %s !! THIS CAUSE SQL INJECTION !!
        
        cursor.execute(query2,bookid)
        z=list(cursor)

        
        count=0
        for i in z:
            count=count+1



        #UPDATE `books_in_lib` SET `remaining_books` = '156' WHERE `books_in_lib`.`sno` = 1;
        query="SELECT * FROM `books_in_lib` WHERE bookid=%s"
        cursor.execute(query,bookid)
        n=list(cursor)
        for j in n:
            x=j[3]# This loop works only ones
        c=x-count
    

        
        
        c=str(c)
        
        

      
        #query2="UPDATE `books_in_lib` SET `remaining_books` = {} WHERE `books_in_lib`.`bookid` =;{}".format(c,bookid)
        #query2="UPDATE `books_in_lib` SET `remaining_books` = %s WHERE `books_in_lib`.`bookid` = %s;"
        query2="UPDATE `books_in_lib` SET `remaining_books` ="+c+" WHERE `books_in_lib`.`bookid` ="+bookid+";"
        cursor.execute(query2)
        db.commit()



def books_counting_prev(bookid):
    import pymysql
    

    
    var=bookid
    '''var=bookid.strip('][').split(', ')'''
    type(var)

    import ast
    var= ast.literal_eval(bookid) 
    type(var)

    db = pymysql.connect(host='localhost',user='root',passwd='')
    cursor=db.cursor()
    query = ("use lib_mgmt_test")
    cursor.execute(query)


    
    '''var=var.split(",")
    var=list(var)
    var=int(var)'''

    for bookid in var:
        query2="SELECT * FROM `my_rel` WHERE `book_id` = %s"#vulernable use ? instead of %s !! THIS CAUSE SQL INJECTION !!
        
        cursor.execute(query2,bookid)
        z=list(cursor)

        count=0
        for i in z:
            count=count+1


        #UPDATE `books_in_lib` SET `remaining_books` = '156' WHERE `books_in_lib`.`sno` = 1;
        query="SELECT * FROM `books_in_lib` WHERE bookid=%s"
        cursor.execute(query,bookid)
        n=list(cursor)
        for j in n:
            l=j[3]# This loop works only ones

        c=l-count


        
        
        c=str(c)
        
        

      
        #query2="UPDATE `books_in_lib` SET `remaining_books` = {} WHERE `books_in_lib`.`bookid` =;{}".format(c,bookid)
        #query2="UPDATE `books_in_lib` SET `remaining_books` = %s WHERE `books_in_lib`.`bookid` = %s;"
        query2="UPDATE `books_in_lib` SET `remaining_books` ="+c+" WHERE `books_in_lib`.`bookid` ="+bookid+";"
        cursor.execute(query2)
        db.commit()




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1111
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$



@app.route("/new_entry",methods=['GET','POST'])
def mainv22():
    
    if 'user' in session and session['user']==p['params']['id']:
        if(request.method=='POST'):
            name=request.form.get('name')
            rollno=request.form.get("rollno")
            book=request.form.get("book")
            book_id=request.form.get("book_id")
            author=request.form.get("author")
            more=request.form.get("more_info")
            date=datetime.now()

            
            if book != "":
                print(".....................................")
                json_list = json_converter(p["books_ids"])
                count = 0
                count_prev = 0
                book_Id = ""
                book = str(book)
                print("books is",book)
                for i in book.split(","):
                    count = count + 1
                count = count - 1
                for i in book.split(","):
                    i_d = key_finder(json_list, i)
                    print("i is:::::::::::::::::::::::::::::::::",i)
                    print("key is : ....................................::::::::::::::::::",i_d)
                    if count_prev < count:
                        book_Id = book_Id + i_d[0] + ","
                    else:
                        book_Id = book_Id + i_d[0]
                    count_prev = count_prev + 1
                book_id = book_Id

            else:
                book_id = request.form.get("book_id")
                count = 0
                count_prev = 0
                book = ""
                print("book_id is is.......................",book_id)
                for i in  book_id.split(","):
                    count = count + 1
                count = count - 1
                for i in book_id.split(","):
                    print("i is.........................",i)
                    data = Books_in_lib.query.filter_by(bookid=i).first()
                    

                    print("data is.............",data.bookid)
                    if count_prev < count:
                        book = book + data.bookname + ","
                    else:
                        book = book + data.bookname
                    count_prev = count_prev + 1

            entry_in_object=Booksv2(name=name, rollno=rollno,author=author,more=more,date=date)
            db.session.add(entry_in_object)
            db.session.commit()
            return redirect(url_for('stubooksv2' ,rollno=rollno,bookid=book_id))
    else:
        return render_template("error.html")
    return render_template("new_entry.html")#before

@app.route("/student_have_booksv2/<rollno>/<bookid>")#this routing tell about remaining books in library
def stubooksv2(rollno,bookid):
    dataprev=Booksv2.query.filter_by(rollno=rollno).first()
    foreignkey=dataprev.sno
    iterate_and_savebooks2(rollno,bookid)#functon i create for sorting more than one book in form input
    
    return render_template("new_entry.html")#before'''


def func_test(bookid):
    bookid=bookid
    bookid=bookid.split(",")
    bookname=[]
    for i in bookid:
        data=Books_in_lib.query.filter_by(bookid=i).first()
        bookname.append(data.bookname)
    return bookname

def iterate_and_savebooks2(rollno,bookid):
    
    temp=func_test(bookid)
    bookid=bookid.split(",")
    
    book=temp
    dataprev=Booksv2.query.filter_by(rollno=rollno).first()
    foreignkey=dataprev.sno
    for i, j in zip(book, bookid):
        entry=My_rel(bookname=i,book_id=j ,foreignkey=foreignkey)
        db.session.add(entry)
        db.session.commit()
    count_book_remaining(book,bookid)
    return render_template("new_entry.html")#before

def count_book_remaining(book,bookid):
    book=book
    bookid=bookid
    for x,j in zip(book, bookid):
        data=My_rel.query.filter_by(book_id=j).all()
        count=0
        for i in data:
            count+=1
        students_have=count
        data2=Books_in_lib.query.filter_by(bookid=j).first()
        total_books=data2.total_we_have#total books=a
        remaining=total_books-students_have#c=a-b
        data2.remaining_books=remaining
        db.session.commit()
    
    



    
        
@app.route("/books_in_trade/<trade_code>")
def comp(trade_code):

    db= pymysql.connect(host='localhost',user='root',passwd='')
    cursor=db.cursor()
    query = ("use lib_mgmt_test")
    
    cursor.execute(query)
    cursor.execute("SELECT * from books_in_lib WHERE trade_code="+trade_code+";")
    data=[]
    for i in cursor:
        data.append(i)
    
    return render_template("semester_books.html",data=data)


@app.route("/admin-refresh")
def refresher():
    data=Books_in_lib.query.all()
    
    array=[]
    array2=[]
    for x in data:
        array.append(x.bookid)
        array2.append(x.bookname)
    count_book_remaining(array2,array)
    return redirect("/admin")


@app.route("/add_a_new_book_to_database", methods=['GET', 'POST'])
def book_adder():
    if request.method=='POST':
        book_id = request.form.get("book_id")
        book_name = request.form.get("book_name")
        total_no_of_books = request.form.get("total_no_of_books")
        remaining_no_of_books = request.form.get("remaining_no_of_books")
        trade_code = request.form.get("trade_code")
        trade = request.form.get("trade")

        book_adder_object = Books_in_lib(bookid=book_id, bookname=book_name, total_we_have=total_no_of_books, remaining_books=remaining_no_of_books, trade_code=trade_code, trade=trade)
        db.session.add(book_adder_object)
        db.session.commit()

    return render_template("new_book_adder.html")


@app.route("/iframe")
def iframe():
    data=Books_in_lib.query.all()
    return render_template("table.html", data=data)

@app.route("/test")
def test():
    return render_template("test.html")


#This function convert JSON as we need json for getting id's from name specified for books
def json_converter(j_son):
    y = dict(j_son)

    #this thing idk, but convert dictionary in list
    x =[(key, values) for key, values in y.items()]

    #creating list from dictionary
    z=[]
    for i in range(len(x)):
        for j in range(0,2):
            t=x[i][j]#it's same as x[i][j]
            t = str(t)
            q = t.split(",")
            z.append(q)
    return z

#finding value in list
def key_finder(z, value):
    value = str(value)
    prev_i=0
    for i in z:
        for j in i:
        
            if j == value:
                return prev_i
                break
        prev_i = i
    


if __name__ == "__main__":
    app.run(debug=True)

















