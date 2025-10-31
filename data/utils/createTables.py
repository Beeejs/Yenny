from sqlite3 import Error

# Tablas
SQL_TABLAS = {
  "usuario": """
      CREATE TABLE IF NOT EXISTS usuario (
          id_usuario INTEGER PRIMARY KEY,
          email TEXT NOT NULL UNIQUE,
          nombre TEXT NOT NULL,
          rol TEXT NOT NULL,
          password TEXT NOT NULL
      );
  """,
  "categoria": """
      CREATE TABLE IF NOT EXISTS categoria (
          id_categoria INTEGER PRIMARY KEY,
          nombre TEXT NOT NULL,
          descripcion TEXT
      );
  """,
  "libro": """
      CREATE TABLE IF NOT EXISTS libro (
          id_libro INTEGER PRIMARY KEY,
          titulo TEXT NOT NULL,
          editorial TEXT,
          autor TEXT,
          anio INTEGER,
          precio REAL NOT NULL,
          stock INTEGER NOT NULL
      );
  """,
  "libro_categoria": """
      CREATE TABLE IF NOT EXISTS libro_categoria (
          id_libro INTEGER NOT NULL,
          id_categoria INTEGER NOT NULL,
          PRIMARY KEY (id_libro, id_categoria),
          FOREIGN KEY (id_libro) REFERENCES libro(id_libro) ON DELETE CASCADE,
          FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria) ON DELETE CASCADE
      );
  """,
  "venta": """
      CREATE TABLE IF NOT EXISTS venta (
          id_venta INTEGER PRIMARY KEY,
          id_usuario INTEGER NOT NULL,
          fecha DATETIME NOT NULL,
          metodo_pago TEXT NOT NULL,
          estado TEXT NOT NULL,
          FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
      );
  """,
  "venta_detalle": """
      CREATE TABLE IF NOT EXISTS venta_detalle (
          id_detalle INTEGER PRIMARY KEY,
          id_libro INTEGER NOT NULL,
          id_venta INTEGER NOT NULL,
          cantidad INTEGER NOT NULL,
          precio_unitario REAL NOT NULL,
          subtotal REAL NOT NULL,
          FOREIGN KEY (id_libro) REFERENCES libro(id_libro),
          FOREIGN KEY (id_venta) REFERENCES venta(id_venta) ON DELETE CASCADE
      );
  """,
  "popularidad_libro_diaria": """
      CREATE TABLE IF NOT EXISTS popularidad_libro_diaria (
          id_popularidad INTEGER PRIMARY KEY,
          id_libro INTEGER NOT NULL,
          dia DATE NOT NULL,
          unidades INTEGER,
          ingresos REAL,
          FOREIGN KEY (id_libro) REFERENCES libro(id_libro)
      );
  """,
  "reporte_venta_diaria": """
      CREATE TABLE IF NOT EXISTS reporte_venta_diaria (
          id_reporte INTEGER PRIMARY KEY,
          id_usuario INTEGER NOT NULL,
          dia DATE NOT NULL,
          ventas INTEGER,
          unidades INTEGER,
          monto REAL,
          FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
      );
  """
}


def createTables(connection):
    
  if connection is None:
    print("Error: No se proporcionó una conexión activa a la base de datos.")
    return

  cursor = connection.cursor()

  # Definimos el orden de cración
  orden_tablas = [
    "usuario", "categoria", "libro",
    "venta",
    "libro_categoria", "venta_detalle",
    "popularidad_libro_diaria", "reporte_venta_diaria"
  ]
  
  # Creamos las tablas
  for table_name in orden_tablas:
    sql_statement = SQL_TABLAS.get(table_name)
    if sql_statement:
        try:
          cursor.execute(sql_statement)
          print(f"Tabla '{table_name}' creada o ya existente.")
        except Error as e:
          print(f"Error al crear la tabla '{table_name}': {e}")
          # Si falla una creación, deshacemos todos los cambios
          connection.rollback()
          return 
    else:
      print(f"Sentencia SQL no encontrada para la tabla '{table_name}'.")

  # Confirmar los cambios de forma permanente
  connection.commit()
  print("✅ Creación de todas las tablas completada y confirmada.")