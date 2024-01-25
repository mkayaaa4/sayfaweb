import sqlite3
from flask import Flask, redirect, render_template, request, url_for



app = Flask(__name__)


data = []


def veriAl():
    global data
    with sqlite3.connect('book.db') as con:
        cur = con.cursor()
        cur.execute("select * from tblBook")
        data = cur.fetchall()
        for i in data:
            print(i)


def veriEkle(title, author, year):
    with sqlite3.connect('book.db') as con:
        cur = con.cursor()
        cur.execute("insert into tblBook (booktitle, bookauthor, bookyear) values (?,?,?)", (title, author, year))
        con.commit()
        print("veriler eklendi")



def veriSil(id):
    with sqlite3.connect('book.db') as con:
        cur = con.cursor()
        cur.execute("delete from tblBook where id=?", (id))
        print("veriler silindi")



def veriGuncelle(id, title, author, year):
    with sqlite3.connect('book.db') as con:
        cur = con.cursor()
        cur.execute("uptade tblBook set booktitle = ? , bookauthor = ? , bookyear = ? where id = ? ", (title, author, year, id))
        con.commit()
        print("veriler guncellendi")

@app.route("/index")
def index():
    books =[]
    return render_template("index.html", books = books)

@app.route("/proje")
def proje():
    print("proje")
    veriAl()
    return render_template("proje.html" , veri = data)


@app.route("/contact")
def contact():
    print("contact")
    return render_template("contact.html")

@app.route("/about")
def about():
    print("about")
    return render_template("about.html")



@app.route("/projeekle", methods=['GET', 'POST'])
def projeekle():
    print("projeekle")
    if request.method == "POST":
        bookTitle = request.form['bookTitle']
        bookAuthor = request.form['bookAuthor']
        bookYear = request.form['bookYear']
        veriEkle(bookTitle, bookAuthor, bookYear)
    return render_template("projeekle.html")



@app.route("/projesil/<string:id>")
def projesil(id):
    print("projesil silinecek id", id)
    veriSil(id)
    return redirect(url_for("proje"))


@app.route("/projeguncelle/<string:id>",  methods=['GET', 'POST'])
def projeguncelle(id):
    if request.method == 'GET':
        print("guncellenecek id", id)
        guncellenecekVeri = []
        for d in data:
            if str(d[0]) == id:
                guncellenecekVeri = list(d)
        return render_template("projeguncelle.html", veri = guncellenecekVeri)
    else:
        bookID = request.form['bookID']
        bookTitle = request.form['bookTitle']
        bookAuthor = request.form['bookAuthor']
        bookYear = request.form['bookYear']
        veriGuncelle(bookID, bookTitle, bookAuthor, bookYear)
        return redirect(url_for("proje"))
    
    
@app.route("/projedetay/<string:id>")
def projedetay(id):
    detayVeri = []
    for d in data:
        if str(d[0]) == id:
            guncellenecekVeri = list(d)
    return redirect(url_for("proje"))



if __name__ == "__main__":
    app.run(debug = True)

