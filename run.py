from flask import Flask, redirect, request, url_for, session
from database import db

#from controllers import usuario_controller
from controllers import paciente_controller
from controllers import medico_controller
from controllers import consulta_controller
from controllers import usuario_controller


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clinica.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.secret_key = 'clave_secreta_para_login' #ESTO ES NECESARIO PARA MANEJAR SESIONES EN FLASK, PERO EN UN ENTORNO DE PRODUCCIÓN DEBERÍA SER MÁS SEGURO Y NO ESTAR HARD-CODED


db.init_app(app)


#app.register_blueprint(usuario_controller.usuario_bp)
app.register_blueprint(paciente_controller.paciente_bp)
app.register_blueprint(medico_controller.medico_bp)
app.register_blueprint(consulta_controller.consulta_bp)
app.register_blueprint(usuario_controller.usuario_bp)


#El INTERCEPTOR DE SEGURIDAD BLOBAL\
@app.before_request
def restringir_acceso():
    #Peritiremos entrada libre unicamente al login y a archivos de estilo css y js estaticos
    if request.endpoint and 'usuario.login' not in request.endpoint and 'static' not in request.endpoint:
        if 'usuario_id' not in session:
            return redirect(url_for('usuario.login'))


#Funcion para mantener activo el nav var
@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path == path else ''
    return(dict(is_active = is_active))


@app.route("/")
def home():
    return redirect(url_for('paciente.index'))

    with app.app_context():
        db.create_all() #Pas4ra crear tablas de base de datos

        #SEEDER AUTOMATICO: Crear cuenta de prueba si la tabla esta vacia(en este caso si lo esta)
        from models.usuario_model import Usuario
        if not Usuario.query.first():
            cuenta_test = Usuario(nombre="Administrador General", username='admin',password='123',rol="Administrador")
            cuenta_test.save()
            print("===========================================================")
            print("CUENTA DE ACCESO CREADA: Usuario: admin | Contraseña: 123")
            print("===========================================================")
    #Mas adelante para el login


if __name__ == "__main__":
    app.run(debug=True)


