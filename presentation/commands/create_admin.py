import click
from werkzeug.security import generate_password_hash
from data.repositories.user_repository import UserRepository

def register_commands(app):
  @app.cli.command("create-admin")
  @click.option("--email", required=True, help="Email del admin")
  @click.option("--nombre", default="admin", help="Nombre del admin")
  @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
  def create_admin(email, nombre, password):
    # Crea un usuario ADMIN si no existe; si existe, no hace nada.
    with app.app_context():
      repo = UserRepository()
      exists = repo.get_one(email=email)
      if exists:
        click.echo(f"Ya existe un admin con email {email}")
        return
      data = {
        "nombre": nombre,
        "email": email,
        "rol": "ADMIN",
        "password": generate_password_hash(password),
      }
      repo.create(data)
      click.echo(f"✅ Admin creado: {email}")
