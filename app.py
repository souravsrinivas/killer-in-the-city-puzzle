from flask import Flask, render_template, request,redirect, url_for
import sqlite3 as sql

app = Flask(__name__)

correct_pin = "059271"
locked_key = True

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def new_user():
   return render_template('signup.html')

@app.route('/enterold')
def old_user():
   return render_template('login.html')

@app.route('/index')
def index():
   return render_template('index.html',locked=locked_key)

@app.route("/unlock", methods=["GET", "POST"])
def unlock():
    
    if request.method == "POST":
        # Get the pin entered by the user
        pin = request.form["pin"]
        
        if pin == correct_pin:
            # Unlock the locker if the correct pin is entered
            locked = False
            return redirect(url_for("msg2"))
        
        else:
            # Lock the locker if the incorrect pin is entered
            locked = True
            return redirect(url_for("index"))
        
    else:
        # Render the HTML template with the current state of the locker
        return render_template("index.html", locked=locked)

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         unm = request.form['unm']
         eml = request.form['email']
         pwd = request.form['pwd']
         
         with sql.connect("tb.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO users (username,email,password) VALUES (?,?,?)",
               (unm,eml,pwd))
            
            con.commit()
            msg = "signup done successfully"
      except:
         con.rollback()
         msg = "error in signingup"
      
      finally:
         return render_template("added.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("tb.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select username,email from users")
   
   rows = cur.fetchall()
   return render_template("dashboard.html",rows = rows)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            pwd = request.form['pwd']
            
            with sql.connect("tb.db") as con:
                cur = con.cursor()
                
                # Check if username and password match a row in the users table
                cur.execute("SELECT COUNT(*) FROM users WHERE Email=? AND password=?",
                            (email, pwd))
                result = cur.fetchone()
               #  print(result)
                if result[0] == 1:
                   return redirect(url_for("msg1"))
                else:
                    return render_template("signup.html")
        
        except:
            con.rollback()
            return render_template("login.html")
        
        
        finally:
         con.close()
    
    # If the request method is GET, render the login page
    else:
        return render_template("login.html")

@app.route('/msg1')
def msg1():
   return render_template('message1.html')

@app.route('/msg2')
def msg2():
   return render_template('message2.html')

@app.route('/msg3')
def msg3():
   return render_template('message3.html')

@app.route('/msg4')
def msg4():
   return render_template('message4.html')

@app.route('/msg5')
def msg5():
   return render_template('message5.html')

@app.route('/slidep')
def slidep():
   return render_template('slidep.html')

@app.route('/slidepf', methods=['POST', 'GET'])
def slidepf():
    if request.method == "POST":
        code=request.form["code"]
        if code == 'CODE' or code=='Code' or code == 'code':
           return redirect(url_for('msg3'))
        else:
           return redirect(url_for('de2'))
    else:
        return render_template('slidep.html')

@app.route('/riddle2')
def riddle2():
   return render_template('riddle2.html')

@app.route('/riddle2f', methods=['POST', 'GET'])
def riddle2f():
    if request.method == "POST":
        ans=request.form["ans"]
        if ans == 'SWATHI' or ans=='Swathi' or ans == 'swathi':
           return redirect(url_for('msg4'))
        else:
           return redirect(url_for('de'))
    else:
        return render_template('riddle2.html')
    
@app.route('/de')
def de():
   return render_template('deadend.html')

@app.route('/de0', methods=['POST', 'GET'])
def de0():
    if request.method == "POST":
        ans=request.form["ans"]
        if ans == 'LEFT' or ans=='Left' or ans == 'left':
           return redirect(url_for('err404'))
        else:
           return redirect(url_for('de'))
    else:
        return render_template('deadend.html')

@app.route('/404e')
def err404():
   return render_template('err404.html')

@app.route('/de2')
def de2():
   return render_template('deadend2.html')

@app.route('/de2', methods=['POST', 'GET'])
def de2f():
    if request.method == "POST":
        ans=request.form["ans"]
        if ans == 'THE MATH TEACHER':
           return redirect(url_for('err404'))
        else:
           return redirect(url_for('de2'))
    else:
        return render_template('deadend.html')

@app.route('/endpuz')
def endpuz():
   return render_template('endpuz.html')

@app.route('/endpuzf', methods=['POST', 'GET'])
def endpuzf():
    if request.method == "POST":
        code=request.form["code"]
        if code == 'EVIDENCE' or code=='Evidence' or code == 'evidence':
           return redirect(url_for('msg5'))
        else:
           return redirect(url_for('endpuz.html'))
    else:
        return render_template('endpuz.html')

if __name__ == '__main__':
   app.run(debug = True,port=8000)