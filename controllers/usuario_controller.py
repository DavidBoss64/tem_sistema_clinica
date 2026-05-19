from flask import request,redirect,url_for,Blueprint,session,flash
from models.usuario_model import Usuario
from views import usuario_view

usuario_bp = Blueprint("usuario",__name__,url_prefix="/auth")

@usuario_bp.route("/login",methods=['GET','POST'])
def login():
    #Si el user ya inicio sesion redirigir al inicio
    if 'usuario_id' in session:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        #Buscar el usuario por username
        usuario = Usuario.query.filter_by(username=username).first()


        #Verificar la ezxixstencia y validad contra hash
        if usuario and usuario.verify_password(password):
            #Guardamos las variables de identidad en la session
            session['usuario_id']=usuario.id
            session['usuario_nombre']=usuario.nombre
            session['usuario_rol']=usuario.rol
            return redirect(url_for("home"))
        else:
            #Enviamos un mensaje de error que capturará el HTML
            flash("Nombre de usuario o contraseña incorrectos.","danger")

    return usuario_view.login()
    
@usuario_bp.route("/logout")
def logout():
    session.clear() #Destruye todas las cariables de sesión
    return redirect(url_for("usuario.login"))

#CRUD Opcional de administracion de usuarios
@usuario_bp.route("/usuarios")
def index():
    usuarios = Usuario.get_all()
    return usuario_view.list(usuarios)

@usuario_bp.route("/usuarios/create",methods=['GET','POST'])
def create():
    if request.method == "POST":
        nombre = request.form['nombre']
        username = request.form['username']
        password = request.form['password']
        rol = request.form['rol']

        usuario = Usuario(nombre=nombre, username=username, password=password, rol=rol)
        usuario.save()

        return redirect(url_for("usuario.index"))
    
    return usuario_view.create()

