from flask import render_template

def list(consultas):
    return render_template("consultas/index.html",consultas=consultas)

def create(medicos,pacientes):
    #Pasaremos la lista de medicos y pacientes para llenar los SELECRTS
    return render_template("consultas/create.html",medicos=medicos,pacientes=pacientes)

def edit(consulta,medicos,pacientes):
    return render_template("consultas/edit.html",consulta=consulta,medicos=medicos,pacientes=pacientes)


    