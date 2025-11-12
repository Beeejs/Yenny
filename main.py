from data.adapter.mySqliteAdapter import MySqliteAdapter

# py main.py

# crea la base de datos
if __name__ == "__main__":
  adapter = MySqliteAdapter()
  adapter.setup_database()
  
  print("Base creada correctamente.")