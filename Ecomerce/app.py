from operator import indexOf
from flask import Flask , redirect , render_template, request, flash
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, func
from flask_login import LoginManager , UserMixin , login_required ,login_user, logout_user,current_user
from werkzeug.security import generate_password_hash as genph
from werkzeug.security import check_password_hash as checkph
from datetime import datetime




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/ecomerce.db'


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200))
    producto_id = db.Column(db.Integer, ForeignKey('producto.id'))
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))
    admin_id = db.Column(db.Integer, ForeignKey('admin.id'))
    super_id = db.Column(db.Integer, ForeignKey('super.id'))

class Calificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cuanto = db.Column(db.Integer)
    producto_id = db.Column(db.Integer, ForeignKey('producto.id'))
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))
    admin_id = db.Column(db.Integer, ForeignKey('admin.id'))
    super_id = db.Column(db.Integer, ForeignKey('super.id'))

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    precio = db.Column(db.String(200))
    caracteristicas = db.Column(db.String(500))
    imagen = db.Column(db.String(500))
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))
    admin_id = db.Column(db.Integer, ForeignKey('admin.id'))
    super_id = db.Column(db.Integer, ForeignKey('super.id'))


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    apellido = db.Column(db.String(200))
    correo = db.Column(db.String(200))
    contrasena = db.Column(db.String(200))

    def __repr__(self):
        return '<Usuario {}>'.format(self.correo)

    def def_clave(self, clave):
        self.contrasena = genph(clave)
    
    def verif_clave(self, clave):
        return checkph(self.contrasena, clave)

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    apellido = db.Column(db.String(200))
    correo = db.Column(db.String(200))
    contrasena = db.Column(db.String(200))

    def __repr__(self):
        return '<Admin {}>'.format(self.correo)

    def def_clave_admin(self, clave):
        self.contrasena = genph(clave)
    
    def verif_clave_admin(self, clave):
        return checkph(self.contrasena, clave)

class Super(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    apellido = db.Column(db.String(200))
    correo = db.Column(db.String(200))
    contrasena = db.Column(db.String(200))

    def __repr__(self):
        return '<Super {}>'.format(self.correo)

    def def_clave_super(self, clave):
        self.contrasena = genph(clave)
    
    def verif_clave_super(self, clave):
        return checkph(self.contrasena, clave)

@login_manager.user_loader
def get(id):
    return Usuario.query.get(id) or Super.query.get(id) or Admin.query.get(id)


@app.route('/',methods=['GET'])
def get_home():
    return render_template('index.html')
    
@app.route('/contacts',methods=['GET'])
def get_contactos():
    return render_template('contactos.html')

@app.route('/preguntas',methods=['GET'])
def get_preguntas():
    return render_template('p_Frecuentes.html')
    
@app.route('/singnup',methods=['GET'])
def get_singnup():
    return render_template('registro_Persona.html')
    
#logins
@app.route('/login',methods=['GET'])
def get_login():
    if current_user.is_authenticated:
        return redirect(url_for('get_menulogin'))
    return render_template('logins/login_Persona.html')

@app.route('/loginAd',methods=['GET'])
def get_loginad():
    if current_user.is_authenticated:
        return redirect(url_for('get_menuadmin'))
    return render_template('logins/login_Persona_admin.html')

@app.route('/loginSu',methods=['GET'])
def get_loginsu():
    if current_user.is_authenticated:
        return redirect(url_for('get_menusuper'))
    return render_template('logins/login_Persona_super.html')

#productos
@app.route('/productosIn',methods=['GET'])
def get_productosin():
    productos = Producto.query.all()
    return render_template('productos/productos_invitado.html', productos=productos)

@app.route('/productslog',methods=['GET'])
@login_required
def get_prodlog():
    productos = Producto.query.all()
    return render_template('productos/productos_login.html', productos=productos)

@app.route('/productsadmin',methods=['GET'])
@login_required
def get_prodadmin():
    productos = Producto.query.all()
    return render_template('productos/productos_admin.html', productos=productos)

@app.route('/productssuper',methods=['GET'])
@login_required
def get_prodsuper():
    productos = Producto.query.all()
    return render_template('productos/productos_super.html', productos=productos)

@app.route('/detalleproductolog/<id>',methods=['GET'])
@login_required
def get_detprodlog(id):
    sums = db.session.query(func.sum(Calificacion.cuanto)).group_by(Calificacion.producto_id) 
    average = db.session.query(func.avg(sums.subquery())).scalar() 
    usuario = db.session.query(Calificacion).filter( Calificacion.producto_id == id).count()
    average = average/usuario
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    producto = Producto.query.get(id)
    calificaciones = Calificacion.query.all()
    comentarios = Comentario.query.all()
    return render_template('productos/detalle_Productos_login.html', comentarios = comentarios, calificaciones = calificaciones, producto = producto, formatted_now = formatted_now, average = average)

@app.route('/detalleproductoadmin/<id>',methods=['GET'])
@login_required
def get_detproddadmin(id):
    sums = db.session.query(func.sum(Calificacion.cuanto)).group_by(Calificacion.producto_id) 
    average = db.session.query(func.avg(sums.subquery())).scalar() 
    usuario = db.session.query(Calificacion).filter( Calificacion.producto_id == id).count()
    average = average/usuario
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    producto = Producto.query.get(id)
    calificaciones = Calificacion.query.all()
    comentarios = Comentario.query.all()
    return render_template('productos/detalle_Productos_admin.html', comentarios = comentarios, calificaciones = calificaciones, producto = producto, formatted_now = formatted_now, average = average)

@app.route('/detalleproductosuper/<id>', methods=['GET'])
@login_required
def get_detprodsuper(id):
    sums = db.session.query(func.sum(Calificacion.cuanto)).group_by(Calificacion.producto_id) 
    average = db.session.query(func.avg(sums.subquery())).scalar() 
    usuario = db.session.query(Calificacion).filter( Calificacion.producto_id == id).count()
    average = average/usuario
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    producto = Producto.query.get(id)
    calificaciones = Calificacion.query.all()
    comentarios = Comentario.query.all()
    return render_template('productos/detalle_Productos_super.html', comentarios = comentarios, calificaciones = calificaciones, producto = producto, formatted_now = formatted_now, average = average)

#menus
@app.route('/menuadmin',methods=['GET'])
@login_required
def get_menuadmin():
    return render_template('menus/menu_admin.html')

@app.route('/menusuper',methods=['GET'])
@login_required
def get_menusuper():
    return render_template('menus/menu_super.html')

@app.route('/menulogin',methods=['GET'])
@login_required
def get_menulogin():
    return render_template('menus/menu_login.html')

@app.route('/contactslog',methods=['GET'])
@login_required
def get_contactoslog():
    return render_template('menus/contactos_login.html')

@app.route('/contactssuper',methods=['GET'])
@login_required
def get_contactossuper():
    return render_template('menus/contactos_super.html')

@app.route('/preguntaslog',methods=['GET'])
@login_required
def get_preguntaslog():
    return render_template('menus/p_Frecuentes_login.html')

@app.route('/preguntassuper',methods=['GET'])
@login_required
def get_preguntassuper():
    return render_template('menus/p_Frecuentes_super.html')

@app.route('/lista_personas',methods=['GET'])
@login_required
def lista_personas():
    usuarios = Usuario.query.all()
    return render_template('gestor_Personas/listar_Persona.html', usuarios=usuarios)

@app.route('/agregar_persona',methods=['GET'])
@login_required
def agregar_persona():
    return render_template('gestor_Personas/agregar_Persona.html')

@app.route('/lista_personas_admin',methods=['GET'])
@login_required
def lista_personas_admin():
    usuarios = Usuario.query.all()
    return render_template('gestor_Personas/listar_Persona_admin.html', usuarios=usuarios)

@app.route('/agregar_persona_admin',methods=['GET'])
@login_required
def agregar_persona_admin():
    return render_template('gestor_Personas/agregar_Persona_admin.html')

@app.route('/editar_persona/<int:id>',methods=['GET'])
@login_required
def editar_persona(id):
    usuario = Usuario.query.get(id)
    return render_template('gestor_Personas/editar_Persona.html', usuario=usuario)

@app.route('/editar_persona_admin/<id>',methods=['GET'])
@login_required
def editar_persona_admin(id):
    usuario = Usuario.query.get(id)
    return render_template('gestor_Personas/editar_Persona_admin.html', usuario=usuario)

@app.route('/lista_productos',methods=['GET'])
@login_required
def lista_productos():
    productos = Producto.query.all()
    return render_template('gestor_Productos/listar_Producto.html', productos=productos)

@app.route('/agregar_producto',methods=['GET'])
@login_required
def agregar_producto():
    return render_template('gestor_Productos/agregar_Producto.html')

@app.route('/lista_productos_admin',methods=['GET'])
@login_required
def lista_productos_admin():
    productos = Producto.query.all()
    return render_template('gestor_Productos/listar_Producto_admin.html', productos=productos)

@app.route('/editar_producto/<int:id>',methods=['GET'])
@login_required
def editar_producto(id):
    producto = Producto.query.get(id)
    return render_template('gestor_Productos/editar_Producto.html', producto=producto)

@app.route('/editar_comentario/<int:id>',methods=['GET'])
@login_required
def editar_comentario(id):
    comentario = Comentario.query.get(id)
    return render_template('gestor_Comentarios/editar_Comentario.html', comentario=comentario)

@app.route('/agregar_producto_admin',methods=['GET'])
@login_required
def agregar_producto_admin():
    return render_template('gestor_Productos/agregar_Producto_admin.html')

@app.route('/lista_deseos/<int:id>',methods=['GET'])
@login_required
def lista_deseos(id):
    usuario = Usuario.query.get(id)
    productos = Producto.query.all()
    return render_template('gestor_Deseos/listar_Deseo.html', usuario=usuario, productos=productos, id = id)

#comentarios login
@app.route('/comentar/<id>')
@login_required
def comentar(id):
    producto = Producto.query.get(id)
    comentarios = Comentario.query.all()
    return render_template('gestor_Comentarios/agregar_Comentario.html', comentarios = comentarios, producto = producto, id = id)

@app.route('/create_comentario/<id>', methods=['POST'])
@login_required
def create_comentario(id):
    new_comentario = Comentario(descripcion=request.form['descripcion'], producto_id=id)
    db.session.add(new_comentario)
    db.session.commit()
    return redirect(url_for('get_detprodlog', id = id))

#calificar login
@app.route('/calificar/<id>')
@login_required
def calificar(id):
    producto = Producto.query.get(id)
    calificaciones = Calificacion.query.all()
    return render_template('gestor_Calificaciones/agregar_Calificacion.html', calificaciones = calificaciones, producto = producto, id = id)

@app.route('/create_calificacion/<id>', methods=['POST'])
@login_required
def create_calificacion(id):
    new_calificacion = Calificacion(cuanto=request.form['cuanto'], producto_id=id)
    db.session.add(new_calificacion)
    db.session.commit()
    return redirect(url_for('get_detprodlog', id = id))

#comentarios super
@app.route('/comentar_super/<id>')
@login_required
def comentar_super(id):
    producto = Producto.query.get(id)
    comentarios = Comentario.query.all()
    return render_template('gestor_Comentarios/agregar_Comentario_super.html', comentarios = comentarios, producto = producto, id = id)

@app.route('/create_comentario_super/<id>', methods=['POST'])
@login_required
def create_comentario_super(id):
    new_comentario = Comentario(descripcion=request.form['descripcion'], producto_id=id)
    db.session.add(new_comentario)
    db.session.commit()
    return redirect(url_for('get_detprodsuper', id = id))

@app.route('/editar_comentario_super/<id>', methods=['GET', 'POST'])
@login_required
def edit_comentario_super(id):
    comentario = db.session.query(Comentario).filter(Comentario.id == id).first()
    comentario.descripcion = request.form['descripcion']
    db.session.add(comentario)
    db.session.commit()
    return redirect(url_for('get_detprodsuper', id = id))

@app.route('/delete_comentario_super/<id>')
@login_required
def delete_comentario_super(id):
    Comentario.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('get_detprodsuper', id = id))

#calificar super
@app.route('/calificar_super/<id>')
@login_required
def calificar_super(id):
    producto = Producto.query.get(id)
    calificaciones = Calificacion.query.all()
    return render_template('gestor_Calificaciones/agregar_Calificacion_super.html', calificaciones = calificaciones, producto = producto, id = id)

@app.route('/create_calificacion_super/<id>', methods=['POST'])
@login_required
def create_calificacion_super(id):
    new_calificacion = Calificacion(cuanto=request.form['cuanto'], producto_id=id)
    db.session.add(new_calificacion)
    db.session.commit()
    return redirect(url_for('get_detprodsuper', id = id))

@app.route('/delete_calificacion_super/<id>')
@login_required
def delete_calificacion_super(id):
    Calificacion.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('get_detprodsuper', id= id))

#comentarios admin

@app.route('/comentar_admin/<id>')
@login_required
def comentar_admin(id):
    producto = Producto.query.get(id)
    comentarios = Comentario.query.all()
    return render_template('gestor_Comentarios/agregar_Comentario_admin.html', comentarios = comentarios, producto = producto, id = id)

@app.route('/create_comentario_admin/<id>', methods=['POST'])
@login_required
def create_comentario_admin(id):
    new_comentario = Comentario(descripcion=request.form['descripcion'], producto_id=id)
    db.session.add(new_comentario)
    db.session.commit()
    return redirect(url_for('get_detprodsuper', id = id))

#calificar admin

@app.route('/calificar_admin/<id>')
@login_required
def calificar_admin(id):
    producto = Producto.query.get(id)
    calificaciones = Calificacion.query.all()
    return render_template('gestor_Calificaciones/agregar_Calificacion_admin.html', calificaciones = calificaciones, producto = producto, id = id)

@app.route('/create_calificacion_admin/<id>', methods=['POST'])
@login_required
def create_calificacion_admin(id):
    new_calificacion = Calificacion(cuanto=request.form['cuanto'], producto_id=id)
    db.session.add(new_calificacion)
    db.session.commit()
    return redirect(url_for('get_detprodsuper', id = id))

#gestor personas super
@app.route('/registro_super', methods=['POST'])
@login_required
def registro_super():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    usuario = Usuario(nombre=nombre,apellido=apellido, correo=correo)
    usuario.def_clave(request.form['contrasena'])
    db.session.add(usuario)
    db.session.commit()
    usuario = Usuario.query.filter_by(correo=correo).first()
    return redirect('lista_personas')

@app.route('/editar_usuario_super/<id>', methods=['GET', 'POST'])
@login_required
def edit_usuario_super(id):
    usuario = db.session.query(Usuario).filter(Usuario.id == id).first()
    usuario.nombre = request.form['nombre']
    usuario.apellido = request.form['apellido']
    usuario.correo = request.form['correo']
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('lista_personas'))


@app.route('/delete_usuario_super/<id>')
@login_required
def delete_usuario_super(id):
    Usuario.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('lista_personas'))

#gestor productos super
@app.route('/registro_producto_super', methods=['POST'])
@login_required
def registro_producto_super():
    nombre = request.form['nombre']
    precio = request.form['precio']
    caracteristicas = request.form['caracteristicas']
    imagen = request.form['imagen']
    producto = Producto(nombre=nombre, precio=precio, caracteristicas=caracteristicas, imagen = imagen)
    db.session.add(producto)
    db.session.commit()
    return redirect('lista_productos')


@app.route('/editar_producto_super/<id>', methods=['GET', 'POST'])
@login_required
def edit_producto_super(id):
    producto = db.session.query(Producto).filter(Producto.id == id).first()
    producto.nombre = request.form['nombre']
    producto.precio = request.form['precio']
    producto.caracteristicas = request.form['caracteristicas']
    producto.imagen = request.form['imagen']
    db.session.add(producto)
    db.session.commit()
    return redirect(url_for('lista_productos'))

@app.route('/delete_producto_super/<id>')
@login_required
def delete_producto_super(id):
    Producto.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('lista_productos'))

#gestor personas admin
@app.route('/registro_admin', methods=['POST'])
@login_required
def registro_admin():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    usuario = Usuario(nombre=nombre,apellido=apellido, correo=correo)
    usuario.def_clave(request.form['contrasena'])
    db.session.add(usuario)
    db.session.commit()
    usuario = Usuario.query.filter_by(correo=correo).first()
    return redirect('lista_personas_admin')

@app.route('/editar_usuario_admin/<id>', methods=['GET', 'POST'])
@login_required
def edit_usuario_admin(id):
    usuario = db.session.query(Usuario).filter(Usuario.id == id).first()
    usuario.nombre = request.form['nombre']
    usuario.apellido = request.form['apellido']
    usuario.correo = request.form['correo']
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('lista_personas_admin'))

@app.route('/delete_usuario_admin/<id>')
@login_required
def delete_usuario_admin(id):
    Usuario.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('lista_personas_admin'))

#gestor productos admin
@app.route('/registro_producto_admin', methods=['POST'])
@login_required
def registro_producto_admin():
    nombre = request.form['nombre']
    precio = request.form['precio']
    caracteristicas = request.form['caracteristicas']
    imagen = request.form['imagen']
    producto = Producto(nombre=nombre, precio=precio, caracteristicas=caracteristicas, imagen=imagen)
    db.session.add(producto)
    db.session.commit()
    return redirect('lista_productos_admin')

#gestor deseos

#logins y registro

#usuario
@app.route('/signup',methods=['POST'])
def signup():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    usuario = Usuario(nombre=nombre,apellido=apellido, correo=correo)
    usuario.def_clave(request.form['contrasena'])
    db.session.add(usuario)
    db.session.commit()
    usuario = Usuario.query.filter_by(correo=correo).first()
    return redirect('login')

@app.route('/login_usuario',methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'correo' in request.form and 'contrasena' in request.form:
        correo = request.form['correo']
        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario:
            if usuario.verif_clave(request.form['contrasena']):
                login_user(usuario)
                return redirect(url_for('get_menulogin'))
            else:
                flash("Usuario o contraseña inválido")
                return redirect(url_for('login'))
        else:
            flash("Usuario o contraseña inválido")
            return redirect(url_for('login'))

    return render_template('logins/login_Persona.html')

#admin
@app.route('/login_admin',methods=['POST'])
def login_admin():
    if request.method == 'POST' and 'correo' in request.form and 'contrasena' in request.form:
        correo = request.form['correo']
        admin = Admin.query.filter_by(correo=correo).first()
        if admin:
            if admin.verif_clave_admin(request.form['contrasena']):
                login_user(admin)
                return redirect(url_for('get_menuadmin'))
            else:
                flash('Usuario o contraseña inválido')
                return redirect(url_for('get_loginad'))
        else:
            flash('Usuario o contraseña inválido')
            return redirect(url_for('get_loginad'))
    return render_template('logins/login_admin.html')

#super
@app.route('/login_super',methods=['POST'])
def login_super():
    if request.method == 'POST' and 'correo' in request.form and 'contrasena' in request.form:
        correo = request.form['correo']
        super = Super.query.filter_by(correo=correo).first()
        if super:
            if super.verif_clave_super(request.form['contrasena']):
                login_user(super)
                return redirect(url_for('get_menusuper'))
            else:
                flash('Usuario o contraseña inválido')
                return redirect(url_for('get_loginsu'))
        else:
            flash('Usuario o contraseña inválido')
            return redirect(url_for('get_loginsu'))

    return render_template('logins/login_super.html')

#cerrar sesion
@app.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()


    