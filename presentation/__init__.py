# presentation/app.py
from flask import Flask, g
from flask_cors import CORS 
import sqlite3
from data.adapter.mySqliteAdapter import MySqliteAdapter

def create_app():
  # indicamos dónde están los templates (según tu estructura)
  app = Flask(__name__)

  # Configuración de sesión
  app.secret_key = "clave-super-secreta"  # se peude cambiar
  app.config["SESSION_COOKIE_NAME"] = "session"
  app.config["SESSION_COOKIE_HTTPONLY"] = True
  app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
  app.config["SESSION_COOKIE_SECURE"] = False  # HTTPS

  # Habilitar CORS con cookies
  CORS(app, supports_credentials=True, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

  # Adapter solo para conocer la ruta de la DB y crear tablas cuando haga falta
  adapter = MySqliteAdapter()
  app.config["DB_PATH"] = adapter.db_path

  # --- Conexión por request ---
  def get_db():
    if "db" not in g:
      g.db = sqlite3.connect(app.config["DB_PATH"])
      g.db.row_factory = sqlite3.Row
      g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db
  
  # Inyección de la conexión para utilizarlo en las rutas (current_app.get_db())
  app.get_db = get_db

  # Cada vez que se cierre el request, se cierra la conexión
  @app.teardown_appcontext
  def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
      db.close()
  
  # --- Rutas ---
  from .routes.auth import auth_bp
  app.register_blueprint(auth_bp, url_prefix="/api")

  from .routes.book import book_bp
  app.register_blueprint(book_bp, url_prefix="/api/book")

  from .routes.category import category_bp
  app.register_blueprint(category_bp, url_prefix="/api/category")

  from .routes.sale import sale_bp
  app.register_blueprint(sale_bp, url_prefix="/api/sale")

  from .routes.user import user_bp
  app.register_blueprint(user_bp, url_prefix="/api/user")

  # --- Registro de comandos CLI ---
  from .commands.create_admin import register_commands
  register_commands(app)

  return app