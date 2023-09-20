from flask import Flask, flash, redirect, render_template, request
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config["MYSQL_HOST"] = "172.18.0.3"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "egargo_crud"

mysql = MySQL(app)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO paste(title, content) VALUES(%s,%s)", (title, content)
        )
        mysql.connection.commit()
        cursor.close()

        return redirect("/")

    return render_template("create.html")


@app.route("/", methods=["GET"])
def read():
    cursor = mysql.connection.cursor()

    pastes = cursor.execute("SELECT * FROM paste")

    if pastes > 0:
        pastes = cursor.fetchall()

        return render_template("pastes.html", pastes=pastes)
    return render_template("create.html")


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE paste SET title = %s, content = %s WHERE id = %s",
            (title, content, id),
        )
        mysql.connection.commit()
        cursor.close()
        return redirect("/")
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM paste WHERE id = %s", (id,))
        paste = cursor.fetchone()
        cursor.close()
        return render_template("update.html", paste=paste)


@app.route("/delete/<int:id>")
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM paste WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect("/")


if __name__ == "__main__":
    app.run()
