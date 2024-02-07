import sqlite3 as sql
from datetime import date
import os

def createDB():
    conn = sql.connect("albums.db")
    conn.commit()
    conn.close()

def createTable():
    conn = sql.connect("albums.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE albums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        album_name text,
        artist text,
        genre text,
        release_year integer,
        score integer,
        timestamp date
        )
        """)
    conn.commit()
    conn.close()

def getFields():
    conn = sql.connect("albums.db")
    cursor = conn.cursor()
    instruccion = "PRAGMA table_info(albums)"
    #instruccion = f"UPDATE albums SET {column}={newValue} WHERE id={albumId}"
    cursor.execute(instruccion)
    datos = cursor.fetchall()

    fields = {}
    index = 1
    for field in datos:
        if field[1] not in fields.values():
            #fields.append(field[1])
            fields[index] = field[1]
            index = index + 1

    conn.commit()
    conn.close()

    return fields

def insertRow(album_name, artist, genre, release_year, score, timestamp):
    conn = sql.connect("albums.db")
    cursor = conn.cursor()
    instruccion = "INSERT INTO albums (album_name, artist, genre, release_year, score, timestamp) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(instruccion, (album_name, artist, genre, release_year, score, timestamp))
    conn.commit()
    conn.close()

def readRows():
    conn = sql.connect("albums.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM albums"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    for album in datos:
        print(album)

def insertRows(albumsList):
    conn = sql.connect("albums.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO albums VALUES (?, ?, ?, ?, ?)"
    cursor.executemany(instruccion, albumsList)
    conn.commit()
    conn.close()

def readOrdered(field):
    conn = sql.connect("albums.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM albums ORDER BY {field} DESC"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    print(datos)

def searchByName(artist_name):
    conn = sql.connect("albums.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM albums WHERE artist LIKE '{artist_name}%'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    print(datos)

def modifyAlbum(column, newValue, albumId):
    conn = sql.connect("albums.db")
    cursor = conn.cursor()
    instruccion = f"UPDATE albums SET {getFields()[column]}=? WHERE id=?"
    cursor.execute(instruccion, (newValue, albumId))
    conn.commit()
    conn.close()

def deleteRows(artist_id):
    conn = sql.connect("albums.db")
    cursor = conn.cursor()
    instruccion = f"DELETE FROM albums WHERE id = {artist_id}"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def deleteAllRows():
    conn = sql.connect("albums.db")
    cursor = conn.cursor()
    instruccion = f"DELETE FROM albums"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def verificar_input(prompt):
    input_usuario = input(prompt)
    
    while input_usuario.strip() == '':
        print("Ingrese un valor válido")
        input_usuario = input(prompt)
    
    return input_usuario

def verificar_input_int(prompt):
    while True:
        try:
            input_usuario = int(input(prompt))
            return input_usuario
        except ValueError:
            print("Ingrese un valor válido")

if __name__ == "__main__":
    
    if os.path.exists("albums.db"):
        pass
    else:
        createDB()
        createTable()

    print("Bienvenido a Listify")
    while True:
        
        print("\n1- Agregar álbum\n2- Ver Biblioteca\n3- Borrar álbum \n4- Borrar toda la biblioteca (test) \n5- Modificar album \n0- Salir\n")

        election = int(input("Ingresa la opcion: "))

        if election == 0:
            break

        elif election == 1:

            album_name = verificar_input("Ingresa el nombre del álbum: ")
            artist = verificar_input("Ingresa el nombre del artista: ")
            genre = verificar_input("Ingresa el género: ")
            year = verificar_input_int("Ingresa el año de lanzamiento: ")
            score = verificar_input_int("Ingresa tu valoración: ")
            timestamp = date.today()

            insertRow(album_name, artist, genre, year, score, timestamp)

        elif election == 2:
            readRows()

        elif election == 3:
            readRows()
            album_to_delete = verificar_input_int("Ingrese el ID: ")
            deleteRows(album_to_delete)
        
        elif election == 4:
            deleteAllRows()

        elif election == 5:

            for i, j in getFields().items():
                print(f"{i} - {j}")
            select_field = verificar_input_int("Ingrese la columna a modificar: ")

            readRows()
            select_id = verificar_input_int("Ingrese el id del album a modificar: ")

            if select_field in [1, 5, 6]:
                new_value = verificar_input_int("Ingrese el nuevo valor: ")
            
            else:
                new_value = verificar_input("Ingrese el nuevo valor: ")

            modifyAlbum(select_field, new_value, select_id)
