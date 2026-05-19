from flask import request, redirect, url_for, Blueprint, render_template
from datetime import datetime
from models.consulta_model import Consulta
from models.medico_model import Medico
from models.paciente_model import Paciente
from views import consulta_view

consulta_bp = Blueprint("consulta",__name__, url_prefix="/consultas")

@consulta_bp.route("/")
def index():
    #EL EXTRA 1: FILTRO DE CONSULTAS POR FECHA
    fecha_busqueda = request.args.get('fecha')

    if fecha_busqueda:
        try:
            #convertimos la fecha del formulario en string a objeto date de python
            fecha_val = datetime.strptime(fecha_busqueda,'%Y-m%-d%').date()
            #Filtramos directamente usando SQLALCHEMY
            consultas = Consulta.query.filter_by(fecha=fecha_val).all()
        except ValueError:
            consultas =Consulta.get_all()
    else:
        consultas = Consulta.get_all()
    return consulta_view.list(consultas=consultas)

@consulta_bp.route("/create",methods = ['GET','POST'])
def create():
    if request.method == "POST":
        medico_id = request.form['medico_id']
        paciente_id = request.form['paciente_id']
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamiento']
        fecha_str = request.form['fecha']

        # Formateamos la fecha correctamente
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

        consulta = Consulta(fecha=fecha, diagnostico=diagnostico, tratamiento=tratamiento, medico_id=medico_id, paciente_id=paciente_id)
        consulta.save()

        return redirect(url_for("consulta.index"))
    
    # Necesitamos todos los médicos y pacientes registrados para los selectores del formulario
    medicos = Medico.get_all()
    pacientes = Paciente.get_all()
    return consulta_view.create(medicos=medicos, pacientes=pacientes)

@consulta_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    consulta = Consulta.get_by_id(id)
    if request.method == 'POST':
        medico_id = request.form['medico_id']
        paciente_id = request.form['paciente_id']
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamiento']
        fecha_str = request.form['fecha']

        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        
        consulta.update(fecha=fecha, diagnostico=diagnostico, tratamiento=tratamiento, medico_id=medico_id, paciente_id=paciente_id)
        return redirect(url_for("consulta.index"))
    
    medicos = Medico.get_all()
    pacientes = Paciente.get_all()
    return consulta_view.edit(consulta=consulta, medicos=medicos, pacientes=pacientes)


@consulta_bp.route("/delete/<int:id>", methods=['POST', 'GET'])
def delete(id):
    consulta = Consulta.get_by_id(id)
    if consulta:
        consulta.delete()
    return redirect(url_for("consulta.index"))

# EXTRA 2: Historial Médico del Paciente
@consulta_bp.route("/historial/<int:paciente_id>")
def historial(paciente_id):
    paciente = Paciente.get_by_id(paciente_id)
    # Recuperamos únicamente las consultas que pertenecen a este paciente específico
    consultas = Consulta.query.filter_by(paciente_id=paciente_id).order_by(Consulta.fecha.desc()).all()
    return render_template("consultas/historial.html", paciente=paciente, consultas=consultas)