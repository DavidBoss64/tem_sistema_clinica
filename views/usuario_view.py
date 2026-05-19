from flask import render_template

def login():
    return render_template("usuarios/login.html")

def list(usuarios):
    return render_template("usuarios/index.html",usuarios=usuarios)

def create():
    return render_template("usuarios/create.html")


