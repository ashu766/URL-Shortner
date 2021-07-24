from flask import Flask, render_template, request, redirect, session
from mysql.connector import connect
import string
import random
from flask_mail import Mail, Message
app1 = Flask(__name__)

app1.config.update(
 MAIL_SERVER='smtp.gmail.com',
 MAIL_PORT=465,
 MAIL_USE_SSL=True,
 MAIL_USERNAME='maheshwariashutosh76@gmail.com',
 MAIL_PASSWORD='mukeshgupta@123'
)


app1.secret_key="ashashuu123"

mail=Mail(app1)



@app1.route('/')
def hello():
    return render_template('index1.html')


@app1.route('/mailbhejo')
def mailbhejo():
    msg=Message(subject='mail sender',sender='maheshwariashutosh76@gmail.com', recipients=['maheshwariashutosh76@gmail.com'],body="this is my first email")
    mail.send(msg)
    return 'MAIL SENT!!!!'



@app1.route('/<url>')
def dunamicUrl(url):
    print(url)
    connection = connect(host='localhost', port='3307', database='app', user='root', password='ashu@123')
    cur = connection.cursor()
    query1 = "select * from urlinfo where encryptedurl='{}'".format(url)
    cur.execute(query1)
    originalurl = cur.fetchone()
    if originalurl == None:
        return render_template('index1.html')
    else:
        print(originalurl[1])
        return redirect(originalurl[1])


@app1.route('/urlshortner')
def urlshortner():
    url = request.args.get('link')
    custom = request.args.get('custom')

    connection = connect(host='localhost', port='3307', database='app', user='root', password='ashu@123')
    cur = connection.cursor()
    encryptedurl = ''
    if custom == '':
        while True:
            encryptedurl = createEncryptedUrl()
            query1 = "select * from urlinfo where encryptedurl='{}'".format(encryptedurl)
            cur.execute(query1)
            xyz = cur.fetchone()
            if xyz == None:
                break
        print(encryptedurl)
        if 'userid' in session:
            id=session['userid']
            query = "insert into urlinfo(originalurl,encryptedurl,is_active,created_by) values('{}','{}',1,{})".format(url, encryptedurl,id)
        else:
            query = "insert into urlinfo(originalurl,encryptedurl,is_active) values('{}','{}',1)".format(url,encryptedurl)

        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        finalencryptedurl = 'sd.in/' + encryptedurl
    else:
        query1 = "select * from urlinfo where encryptedurl='{}'".format(custom)
        cur.execute(query1)
        xyz = cur.fetchone()
        if xyz == None:
            if 'userid' in session:
                id=session['userid']
                query = "insert into urlinfo(originalurl,encryptedurl,is_active,created_by) values('{}','{}',1,{})".format(url, custom,id)
            else:
                query = "insert into urlinfo(originalurl,encryptedurl,is_active) values('{}','{}',1)".format(url, custom)
            cur = connection.cursor()
            cur.execute(query)
            connection.commit()
            finalencryptedurl = 'sd.in/' + custom

        else:
            return "url already exists"
    if 'userid' in session:
        return redirect('/home')
    else:
        return render_template('index1.html', finalencryptedurl=finalencryptedurl, url=url)


def createEncryptedUrl():
    letter = string.ascii_letters + string.digits
    encryptedurl = ''
    for i in range(6):
        encryptedurl = encryptedurl + ''.join(random.choice(letter))
    print(encryptedurl)
    return encryptedurl

@app1.route('/signup')
def signup():
    return render_template('signup.html')


@app1.route('/register')
def register():
    email=request.args.get('email')
    username=request.args.get('uname')
    password=request.args.get('pwd')
    confirompassword=request.args.get('cpwd')
    connection = connect(host='localhost', port='3307', database='app', user='root', password='ashu@123')
    cur = connection.cursor()
    query1 = "select * from users_details where emailid='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    if xyz == None:
        query = "insert into users_details(emailid,username,password,is_active,is_verified) values('{}','{}','{}',1,1)".format(email,username,password,confirompassword)
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        return 'you have sucessfully regestired'
    else:
        return 'already regestired'


@app1.route('/GoogleSign')
def signin():
    return  render_template('google.html')
@app1.route('/login')
def login():
    return  render_template('login.html')

@app1.route('/checklogin')
def checklogin():
    email=request.args.get('email')
    password=request.args.get('pwd')
    connection = connect(host='localhost', port='3307', database='app', user='root', password='ashu@123')
    cur = connection.cursor()
    query1 = "select * from users_details where emailid='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    print(xyz)
    if xyz == None:
        return render_template('login.html',xyz="you are not regestired")

    else:
        if password==xyz[3]:
            session['email']= email
            session['userid'] = xyz[0]
            return redirect('/home')
        else:
            return render_template('login.html', xyz="your password is not correct")


@app1.route('/home')
def home():
    if 'userid' in session:
        email = session['email']
        id = session['userid']
        print(id)
        connection = connect(host='localhost', port='3307', database='app', user='root', password='ashu@123')
        cur = connection.cursor()
        query1 = "select * from urlinfo where created_by={}".format(id)
        cur.execute(query1)
        data = cur.fetchall()
        print(data)
        return render_template("updateurl.html",data=data)
    return render_template("login.html")


@app1.route('/editUrl',methods=['post'])
def editUrl():
    if 'userid' in session:
        email = session['email']
        id = session['userid']
        print(id)
        id=request.form.get('id')
        url=request.form.get('orignalurl')
        encrypted=request.form.get('encrypted')
        return render_template("editUrl.html",url=url,encrypted=encrypted,id=id)
    return render_template("login.html")



@app1.route('/updateUrl',methods=['post'])
def updateUrl():
    if 'userid' in session:
        email = session['email']
        id = session['userid']
        print(id)
        id=request.form.get('id')
        url=request.form.get('orignalurl')
        encrypted=request.form.get('encrypted')
        connection = connect(host='localhost', port='3307', database='app', user='root', password='ashu@123')
        cur = connection.cursor()
        query1 = "select * from urlinfo where encryptedUrl='{}'and pk_urlId!={}".format(encrypted,id)
        cur.execute(query1)
        xyz = cur.fetchone()
        if xyz == None:
            query = "update urlinfo set originalUrl ='{}', encryptedUrl ='{}' where pk_urlId={}".format(url,encrypted,id)
            cur = connection.cursor()
            cur.execute(query)
            connection.commit()
            return redirect('/home')
        else:
            return render_template("editUrl.html",url=url,encrypted=encrypted,id=id,error='Short Url Already Exists')
        print(url)
        print(id)
        print(encrypted)
        return encrypted
    return render_template("login.html")
    #return render_template("editUrl.html",url=url,encrypted=encrypted,id=id)




@app1.route('/deleteUrl',methods=['post'])
def deleteUrl():
    if 'userid' in session:
        email = session['email']
        id = session['userid']
        print(id)
        id = request.form.get('id')
        connection = connect(host='localhost', port='3307', database='app', user='root', password='ashu@123')
        cur = connection.cursor()
        query1 = "delete from urlinfo where pk_urlId="+id
        cur.execute(query1)
        connection.commit()
        return redirect('/home')
    return render_template("login.html")


@app1.route('/logout')
def logout():
    session.pop('userid',None)
    return render_template("login.html")





if __name__ == '__main__':
    app1.run()
