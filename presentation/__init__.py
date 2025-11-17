# presentation/app.py
import os
from flask import Flask, g, render_template
from flask_cors import CORS 
import sqlite3
from data.adapter.mySqliteAdapter import MySqliteAdapter
from presentation.middlewares.web.login_required import login_required


def create_app():
  root_dir = os.path.dirname(__file__)
  # Indicamos donde están los templates
  template_dir = os.path.join(root_dir, 'templates')
  static_dir   = os.path.join(template_dir, 'static')

  # indicamos dónde están los templates (según tu estructura)
  app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

  # Configuración de entorno
  ENV = os.environ.get('FLASK_ENV', 'development')

  # Configuración de sesión
  app.secret_key = os.environ.get("SECRET_KEY", "fallback_secret_for_dev")
  app.config["SESSION_COOKIE_NAME"] = "session"
  app.config["SESSION_COOKIE_HTTPONLY"] = True
  app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
  app.config["SESSION_COOKIE_SECURE"] = ENV == 'production'  # HTTPS

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

  # --- Rutas Web ---
  @app.route("/")
  @login_required
  def home():
    return render_template("index.html")

  # Auth
  from .routes.web.auth import web_auth_bp
  app.register_blueprint(web_auth_bp)

  # Libros
  from .routes.web.book import web_book_bp
  app.register_blueprint(web_book_bp)

  # Ventas
  from .routes.web.sale import web_sale_bp
  app.register_blueprint(web_sale_bp)

  # Reportes
  from .routes.web.report import web_report_bp
  app.register_blueprint(web_report_bp)

  # Categorías
  from .routes.web.category import web_category_bp
  app.register_blueprint(web_category_bp)

  
  # --- Rutas Api ---
  from .routes.api.auth import auth_bp
  app.register_blueprint(auth_bp, url_prefix="/api")

  from .routes.api.book import book_bp
  app.register_blueprint(book_bp, url_prefix="/api/book")

  from .routes.api.category import category_bp
  app.register_blueprint(category_bp, url_prefix="/api/category")

  from .routes.api.sale import sale_bp
  app.register_blueprint(sale_bp, url_prefix="/api/sale")

  from .routes.api.user import user_bp
  app.register_blueprint(user_bp, url_prefix="/api/user")

  # --- Registro de comandos CLI ---
  from .commands.create_admin_manager import register_commands
  register_commands(app)

  return app