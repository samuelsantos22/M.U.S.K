import sqlite3
import time



class database():

    conn = sqlite3.connect('todo.db') # cria se necessario a base da dados
    c = conn.cursor() # gera o cursor da db

    # gera se necessario a tabela do db
    def create_table():
        c.execute("CREATE TABLE IF NOT EXISTS Todo(id INTEGER, title TEXT, start DATETIME, complete NUMERIC)")


    #Teste de entrada de dados na tabela
    def data_entry():
        c.execute("INSERT INTO Todo VALUES(145, 'ujadssakd' ,'2016-01-11 13:53:39', 1)")
        conn.commit()
        c.close()
        conn.close()


    #Lê na tabela determinada coluna - nesse caso a title -
    def read_from_db():

        c.execute('SELECT title FROM Todo WHERE complete = 1 ')
        data = c.fetchall()

        return data

    #transforma o read_from_db em string e elimina os caracteres SQL
    def read_string_db():


        data = read_from_db()
        len_data = len(data)
        data_str = data

        for i in range(len_data):
            var1 = str(data[i])
            len_data_str = len(var1)
            var1 = var1[2:(len_data_str-4)] # recorta string https://pt.stackoverflow.com/questions/272561/como-remover-caracteres-de-posi%C3%A7%C3%A3o-espec%C3%ADfica-de-uma-string
            data_str[i] = var1

        return data_str