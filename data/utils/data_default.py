import sqlite3

def cargar_libros_default(connection):
    
    # Inserta los 10 libros por defecto usando la conexión activa.
    

    libros = [
        {
            "titulo": "The Women",
            "editorial": "St. Martin’s Press",
            "autor": "Kristin Hannah",
            "anio": 2024,
            "precio": 19990,
            "stock": 50
        },
        {
            "titulo": "Fourth Wing",
            "editorial": "Red Tower Books",
            "autor": "Rebecca Yarros",
            "anio": 2023,
            "precio": 18950,
            "stock": 80
        },
        {
            "titulo": "Iron Flame",
            "editorial": "Red Tower Books",
            "autor": "Rebecca Yarros",
            "anio": 2023,
            "precio": 21990,
            "stock": 70
        },
        {
            "titulo": "It Ends with Us",
            "editorial": "Atria Books",
            "autor": "Colleen Hoover",
            "anio": 2022,
            "precio": 15990,
            "stock": 100
        },
        {
            "titulo": "Verity",
            "editorial": "Grand Central Publishing",
            "autor": "Colleen Hoover",
            "anio": 2021,
            "precio": 15990,
            "stock": 90
        },
        {
            "titulo": "Lessons in Chemistry",
            "editorial": "Doubleday",
            "autor": "Bonnie Garmus",
            "anio": 2022,
            "precio": 17500,
            "stock": 60
        },
        {
            "titulo": "Tomorrow, and Tomorrow, and Tomorrow",
            "editorial": "Knopf",
            "autor": "Gabrielle Zevin",
            "anio": 2022,
            "precio": 18990,
            "stock": 65
        },
        {
            "titulo": "The Housemaid",
            "editorial": "Poisoned Pen Press",
            "autor": "Freida McFadden",
            "anio": 2023,
            "precio": 14990,
            "stock": 85
        },
        {
            "titulo": "Happy Place",
            "editorial": "Berkley",
            "autor": "Emily Henry",
            "anio": 2023,
            "precio": 17990,
            "stock": 75
        },
        {
            "titulo": "Spare",
            "editorial": "Penguin Random House",
            "autor": "Prince Harry",
            "anio": 2023,
            "precio": 22000,
            "stock": 55
        }
    ]

    if connection is None:
        print("Error: conexión a base de datos no válida.")
        return

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM libro;")
        cantidad = cursor.fetchone()[0]

        if cantidad == 0:
            for libro in libros:
                cursor.execute("""
                    INSERT INTO libro (titulo, editorial, autor, anio, precio, stock)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    libro["titulo"],
                    libro["editorial"],
                    libro["autor"],
                    libro["anio"],
                    libro["precio"],
                    libro["stock"]
                ))
            connection.commit()
            print("Libros por defecto cargados correctamente.")
        else:
            print("La tabla 'libro' ya contiene registros. No se insertaron datos por defecto.")

    except sqlite3.Error as e:
        print(f"Error al insertar los libros por defecto: {e}")