from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.pie import Pie
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/createPie")
def addRecipe(): 
    return render_template("createPie.html")


@app.route("/create", methods=["POST"])
def create(): 
    data ={
        "name" : request.form['name'],
        "user_id": session['user_id'],
        "filling" : request.form['filling'],
        "crust" : request.form['crust'],
        "vote": 0
    }
    if not Pie.validate_pie(data):
        return redirect("/dashboard")
    res = Pie.create(data)
    print(res)
    return redirect("/dashboard")

@app.route("/edit/<int:id>")
def editRecipe(id): 
    data = {
        "id": id
        }
    pie= Pie.getOnePie(data)[0]
    return render_template("edit.html", pie =pie)

@app.route("/update/<int:id>", methods=["POST"])
def updateRecipe(id): 
    data = {
        "id": id,
        "name": request.form['name'],
        "filling": request.form['filling'],
        "crust": request.form['crust'],
        }
    if not Pie.validate_pie(data):
        return redirect(f"/edit/{data['id']}")
    Pie.updatePie(data)
    return redirect("/dashboard")



@app.route("/delete/<int:id>")
def delete(id): 
    print('here')
    data ={
        "id": id
    }
    res = Pie.deletePie(data)
    return redirect("/dashboard")

@app.route("/pies")
def allPies():
    pies = Pie.getAllpies()
    return render_template("pies.html", pies=pies)

@app.route("/showPie/<int:id>")
def showPie(id): 
    print('here')
    data ={
        "id": id
    }
    pie = Pie.getPieWithUser(data)[0]

    return render_template("show.html", pie=pie)

@app.route("/updateVotes/<int:id>", methods=["POST"])
def updateVotes(id): 
    print('here')
    data ={
        "id": id
    }
    pie = Pie.getOnePie(data)
    updated = pie[0]['vote']+1

    new_data={
        "id": id,
        "vote": updated
    }
    res = Pie.updateVotes(new_data)
    print(res)
    # print("RESULT!!!!")
   
    return redirect("/pies")