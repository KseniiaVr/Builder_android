import pymysql
import pandas as pd
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
#from kivymd.uix.screen import Screen
from pymysql.cursors import DictCursor
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

class RowDetailsScreen(Screen):
    pass

class MainApp(MDApp):

    def build(self):
        connection = pymysql.connect(
            host="194.44.39.209",
            user="viewer2",
            password="~viewer2",
            port=3306,
            db="tmp_db3",
            cursorclass=DictCursor,
            charset="utf8"
        )
        cursor = connection.cursor()
        cursor.execute(
            "SELECT zakaz_materials.xCount, zakaz_materials.user_name, spr_1_materials_categories.material_category_name FROM zakaz_materials INNER JOIN spr_1_materials_categories ON zakaz_materials.id_material_category=spr_1_materials_categories.id_material_category WHERE zakaz_materials.status=3")
        names = cursor.fetchall()

        connection.close()

        screen = Screen()
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        data_table = MDDataTable(pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                 size_hint=(0.9, 0.9),
                                 use_pagination=True,
                                 background_color_header="#42c5f5",
                                 check=True,
                                 rows_num=10,
                                 column_data=[

                                     ("Назва", dp(60)),
                                     ("Кількість", dp(20)),
                                     ("Користувач", dp(50))

                                 ],
                                 row_data=[(d['material_category_name'], d['xCount'], d['user_name']) for d in names],
                                 on_row_press=self.on_row_press


                                 )
        data_table.bind(on_row_press=self.on_row_press)
        data_table.bind(on_check_press=self.on_check_press)
        screen.add_widget(data_table)
        #print( [(d['material_category_name'], d['user_name']) for d in names])

        return screen

    def on_row_press(self, instance_table, instance_row):
        self.clear_screen()
        # Get the data from the pressed row
        row_data = instance_row.text.split('\n')
        screen = Screen()

        # Create a new screen to display row details

        #row_details_screen.ids.details_label.text = f"Name: {row_data[0]}\nAge: {row_data[1]}\nCountry: {row_data[2]}"
        screen.add_widget(screen)
        return screen

    def clear_screen(self):
        # Clear previous instances of RowDetailsScreen
        for screen in screens:
            if screen.name == 'row_details_screen':
                sm.remove_widget(screen)

    #def on_row_press(self, instance_table, instance_row):
        #print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        print(instance_table, current_row)

if __name__ == '__main__':


    connection = pymysql.connect(
        host = "194.44.39.209",
        user="viewer2",
        password="~viewer2",
        port = 3306,
        db="tmp_db3",
        cursorclass=DictCursor,
        charset="utf8"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM zakaz_materials ")
    #cursor.execute("SELECT * FROM spr_1_materials_categories")
    #cursor.execute("SELECT spr_1_materials_categories.material_category_name FROM zakaz_materials INNER JOIN spr_1_materials_categories ON zakaz_materials.id_material_category=spr_1_materials_categories.id_material_category WHERE zakaz_materials.status=3")
    name=cursor.fetchall()
    print(name)


    #row in cursor.fetchall():



    MainApp().run()
    connection.close()




