from datetime import datetime # Módulo que accede al tiempo

# Función que abre el archivo y retorna una lista con c/linea como elemento
def leer_lista_list(): 
    with open("favorite_albums_list.txt", "r") as my_file:
        lineas = my_file.readlines()
    return lineas

print("Bienvenido a Favolist, biblioteca de tus álbumes preferidos")

#Inicio del programa
while True:

    print("\n1- Agregar álbum\n2- Ver Biblioteca\n3- Borrar álbum \n0- Salir\n")
    
    election = int(input("Ingresa la opcion: "))

    # Elección 0 Sale del programa
    if election == 0:
        break

    # Elección 1 Agrega contenido (album y detalle) al archivo
    elif election == 1:

        album_name = input("Ingresa el nombre del álbum: ")
        artist = input("Ingresa el nombre del artista: ")
        year = input("Ingresa el año de lanzamiento: ")

        # Se consulta por el género principal, y también si el álbum cuenta con otro/s
        # se guardan los resultados en una lista y luego se concatenan en una cadena
        genres = []
        while True:
            genre = input("Ingresa el género: ")
            genres.append(genre.title())

            new_genre = input("¿El álbum se considera de otro género más? S/N: ")
            new_genre = new_genre.upper()
            if new_genre == "N":
                break
            else:
                pass
        
        genres_str = ", ".join(genres)

        valoracion = input("Ingresa tu valoración: ")

        # Hace la prueba de verificar si hay un id (si hay id, hay un album registrado)
        # Si hay, el proximo registro será el id del registro anterior + 1
        # Si no lo hay, entonces es el primer registro (el id será 0)
        try:
            if isinstance(int(leer_lista_list()[-8]), int):
                id = int(leer_lista_list()[-8]) + 1
        except (IndexError, ValueError):
            id = 0

        # Escribe cada uno de los registros (8 en total contando la línea separadora)
        with open("favorite_albums_list.txt", "a+") as my_file:
            my_file.write(f"\n{str(id)}\n")
            my_file.write(f"Álbum: {album_name}\n")
            my_file.write(f"Artista: {artist}\n")
            my_file.write(f"Año: {year}\n")
            my_file.write(f"Genero/s: {genres_str}\n")
            my_file.write(f"Valoración: {valoracion}\n")
            my_file.write(f"Registrado en: {str(datetime.now())}\n")
            my_file.write("----------------------------------")
            
        # A su vez, el artista es guardado en otro archivo externo (si ya está registrado, no se escribe nuevamente)
        if f"Artist: {artist}" not in leer_lista_list():
            with open("artists_dicc.txt", "a+") as artist_file:
                artist_file.write(f"\nArtist: {artist}\n")

        else:
            pass

    # Elección 2 imprime todo el texto del archivo 
    elif election == 2:
        with open("favorite_albums_list.txt", "r") as my_file:
            content = my_file.read()
        print(content)

    # Elección 3 Borra un registro (album y detalles) específico
    elif election == 3:

        album_a_borrar = input("Elija el álbum a borrar: ")

        contador = 0
        new_file = []

        with open("favorite_albums_list.txt", "r") as my_file:
            lineas = my_file.readlines()

        # Se vuelven a guardar todos los registros, menos el que se quiere borrar
        # Es decir, dicho registro se ignora en la reescritura del archivo 
        for linea in lineas:

            if contador > 0:
                contador -= 1
                continue

            if album_a_borrar in linea:
                contador = 7

            else:
                new_file.append(linea)
                       
        with open("favorite_albums_list.txt", "w") as my_file:
            for linea in new_file:
                my_file.write(linea)

# https://blog.finxter.com/how-to-delete-a-line-from-a-file-in-python/ Para borrar una línea de texto