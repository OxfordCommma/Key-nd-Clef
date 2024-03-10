import sqlite3
from tkinter import messagebox

class Albumes:

    def __init__(self):
        self.miConexion = sqlite3.connect("Albumes")

        try:
            miCursor = self.miConexion.cursor()
            miCursor.execute("""
                CREATE TABLE IF NOT EXISTS ALBUMES_MUSICALES (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ALBUM VARCHAR(50),
                ARTISTA VARCHAR(50),
                ANIO INT(10),
                GENERO VARCHAR(50),
                VALORACION INT(10),
                COMENTARIO VARCHAR(255))
            """)
            self.miConexion.commit()

        except Exception as e:
            messagebox.showwarning("Atención!", f"Error al crear la BBDD: {e}")

    def __str__(self):
        datos = self.consulta_albumes()
        aux = ""
        for row in datos:
            aux = aux + str(row) + "\n"
        return aux

    def consulta_albumes(self):
        miCursor = self.miConexion.cursor()
        miCursor.execute("SELECT * FROM ALBUMES_MUSICALES")
        datos = miCursor.fetchall()
        miCursor.close()    
        return datos
    
    def buscar_album(self, Id):
        miCursor = self.miConexion.cursor()
        sql = "SELECT * FROM ALBUMES_MUSICALES WHERE ID = {}".format(Id)
        miCursor.execute(sql)
        datos = miCursor.fetchone()
        miCursor.close()    
        return datos
    
    def inserta_album(self,Album, Artista, Anio, Genero, Valoracion, Comentario):
        miCursor = self.miConexion.cursor()
        sql='''INSERT INTO ALBUMES_MUSICALES (ALBUM, ARTISTA, ANIO, GENERO, VALORACION, COMENTARIO) 
        VALUES('{}', '{}', '{}', '{}', '{}', '{}')'''.format(Album, Artista, Anio, Genero, Valoracion, Comentario)
        miCursor.execute(sql)
        n = miCursor.rowcount
        self.miConexion.commit()    
        miCursor.close()
        return n  
    
    def elimina_album(self,Id):
        miCursor = self.miConexion.cursor()
        sql='''DELETE FROM ALBUMES_MUSICALES WHERE ID = {}'''.format(Id)
        miCursor.execute(sql)
        n = miCursor.rowcount
        self.miConexion.commit()    
        miCursor.close()
        return n  
    
    def modifica_album(self,Id, Album, Artista, Anio, Genero, Valoracion, Comentario):
        miCursor = self.miConexion.cursor()
        sql='''UPDATE ALBUMES_MUSICALES SET ALBUM='{}', ARTISTA='{}', ANIO='{}', GENERO='{}',
        VALORACION='{}', COMENTARIO='{}' WHERE ID={}'''.format(Album, Artista, Anio, Genero, Valoracion, Comentario, Id)
        miCursor.execute(sql)
        n = miCursor.rowcount
        self.miConexion.commit()    
        miCursor.close()
        return n 

    
