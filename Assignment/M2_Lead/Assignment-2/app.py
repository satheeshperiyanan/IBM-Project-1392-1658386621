from flask import Flask, render_template, flash,request, redirect,url_for, session
import sqlite3 




app = Flask(__name__)
app.secret_key="123"

con=sqlite3.connect("database.db")
con.execute("create table if not exists users(pid integer primary key,cname TEXT, cemail TEXT, cpassword TEXT, cconfirmpassword TEXT)")
con.close()

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/profile')
def profile():
   return render_template('profile.html')


@app.route('/about')
def about():
   return render_template('about.html')


@app.route('/customerlogin',methods=["GET","POST"])
def customerlogin():
   if request.method=='POST':
        cemail=request.form['cemail']
        cpassword=request.form['cpassword']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from users where cemail=? and cpassword=?",(cemail,cpassword))
        data=cur.fetchone()

        if data:
            session["cemail"]=data["cemail"]
            session["cpassword"]=data["cpassword"]
            return redirect("profile")
        else:
            flash("Username and Password Mismatch","danger")
            return redirect(url_for("index"))
   return render_template('customerlogin.html')

@app.route('/customerregister',methods = ['POST', 'GET'])
def customerregister():
   if request.method == 'POST':
      try:
         cname = request.form['cname']
         cemail = request.form['cemail']
         cpassword = request.form['cpassword']
         cconfirmpassword = request.form['cconfirmpassword']
         con=sqlite3.connect("database.db")
         cur = con.cursor()
         cur.execute("INSERT INTO users (cname,cemail,cpassword,cconfirmpassword) VALUES (?,?,?,?)",(cname,cemail,cpassword,cconfirmpassword))
         con.commit()
         flash("Register successfully","success")        
      except:
         flash("Error","danger")
      
      finally:
         return redirect(url_for("index"))
         con.close()
   return render_template('customerregister.html')



if __name__ == '__main__':
   app.run(debug = True)


