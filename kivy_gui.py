# -*- coding: utf-8 -*-

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from datetime import datetime
import sqlite3
import time
import os
import commands
#import schedule
# ----- CONFIG KIVY -----
kivy.require('1.8.0')

# You can create your kv code in the Python file
Builder.load_string("""

<ScreenOne@Button>:

    background_color: 0,0,0,1
    
    
    on_press:
        root.manager.current = 'screen_two'
    Image:
        source: 'skull1.jpg'
        y: self.parent.y + self.parent.height - 600
        x: self.parent.x + 0
        size: 35,35
        allow_stretch: True
    Label:
        text: "M.U.S.K"
        font_size:'40sp'
        bold: True


<ScreenTwo@Button>:

    background_color: 0,0,0,1

    on_press: 
        root.manager.current = 'screen_three'

    Button:
        background_color: 0,0,0,1
        text: root.registrador_umid_e_temp
        size: 150,50
        font_size: 36
        pos_hint: {"center_x": .5, "center_y": .65}
        

""")

conn = sqlite3.connect('todo.db') # cria se necessario a base da dados
c = conn.cursor() # gera o cursor da db

# ----- KIVY -----
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

class ScreenOne(Screen, Button):

    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)
        # Clock.schedule_interval(self.callback, 3) #Chama a callback depois de um tempo

    def callback(self, dt):
        # print('In Callback')  # Test - The timer is actually calling this funcition
        screen_manager.transition = NoTransition()
        screen_manager.current = 'screen_two'


class ScreenTwo(Screen, Button):
    umid = 9
    umid = "Umidade: " + str(umid)  + " g/Kg \n"

    temp = 10
    temp = "Temperatura: " + str(temp) + "°C \n"

    now = datetime.now()
    date = "\n" + "\n" + "\n" + "Hoje:  " + str(now.day) + "/" + str(now.month) + "/" + str(now.year)  + " \n"
    time = "Horas:  " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)

    registrador_umid_e_temp = ObjectProperty(None)
    registrador_umid_e_temp = temp + umid + date + time

    def __init__(self, **kwargs):
        super(ScreenTwo, self).__init__(**kwargs)
        # Clock.schedule_interval(self.callback, 4)

    def callback(self, dt):
        # print('In Callback') # Test - The timer is actually calling this funcition
        screen_manager.transition = NoTransition()
        screen_manager.current = 'screen_one'


class ScreenThree(Screen):
    def __init__(self, **kwargs):
        super(ScreenThree, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", size_hint_y=None)
#        layout.bind(minimum_height=layout.setter('height'))
#	grid.bind(minimum_height=grid.setter('height')) # only changed var name

        title = read_string_db()
        len_title = len(title)

        ''' Explicação ( e Consertar/Melhorar Samuel Santos !!!!!!): data apresenta a coluna da base de dados
            ela é retornada (como um vetor de vetores????) e medida para que não dê out of range
            e então é apresentada passo por passo

            o row não varia de acordo com um vetor

            Procurar descobrir ou como usar o row[0] ou tirar a descrição sql de data  

        '''

        for i in range(len_title):
            btn = Button(text="Button " + str(title[i]),

                         size=(810, 50),
                         size_hint=(None, None),
                         background_color = (0,0,0,1),
                         font_size =(36),
                         on_press=self.Press_auth)  # <<<<<<<<<<<<<<<<

            layout.add_widget(btn)

        btn_volta = Button(text="Volta",
                         pos_hint = ({"left": 1, "bottom": 1}),
                         size=(810, 700),
                         size_hint=(None, None),
                         background_color=(0, 0, 0, 1),
                         font_size=(36),
                         on_press=self.Press_auth)  # <<<<<<<<<<<<<<<<

        layout.add_widget(btn_volta)

        root = ScrollView()
        root.add_widget(layout)
        self.add_widget(root)

    def Press_auth(self, instance):
        screen_manager.transition = NoTransition()
        screen_manager.current = 'screen_one'
        print(str(instance))


# The ScreenManager controls moving between screens
screen_manager = ScreenManager()

# Add the screens to the manager and then supply a name
# that is used to switch screens
screen_manager.add_widget(ScreenOne(name="screen_one"))
screen_manager.add_widget(ScreenTwo(name="screen_two"))
screen_manager.add_widget(ScreenThree(name="screen_three"))



class KivyTut2App(App):

    def build(self):
        return screen_manager


if __name__ == '__main__':
	 KivyTut2App().run()



