# presentation/app.py
from flask import Flask, render_template, g
import sqlite3
from data.adapter.mySqliteAdapter import MySqliteAdapter

def create_app():
  # indicamos dónde están los templates (según tu estructura)
  app = Flask(__name__)

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

  # Cada vez que se cierre el request, se cierra la conexión
  @app.teardown_appcontext
  def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
      db.close()

  # --- Rutas ---
  @app.route("/")
  def home():
    return render_template("index.html")

  return app


if __name__ == "__main__":
  app = create_app()
  # Evitá logs duplicados en dev (reloader) si te molestan:
  app.run(debug=True, use_reloader=False)
