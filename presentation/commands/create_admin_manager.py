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
  
    # Comando para crear gerente
  @app.cli.command("create-manager")
  @click.option("--email", required=True, help="Email del gerente")
  @click.option("--nombre", default="gerente", help="Nombre del gerente")
  @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
  def create_manager(email, nombre, password):
    with app.app_context():
      repo = UserRepository()
      exists = repo.get_one(email=email)
      if exists:
          click.echo(f"Ya existe un usuario con email {email}")
          return
      data = {
        "nombre": nombre,
        "email": email,
        "rol": "GERENTE",
        "password": generate_password_hash(password),
      }
      repo.create(data)
      click.echo(f"✅ Gerente creado: {email}")
