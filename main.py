import pymysql
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from kivy.uix.screenmanager import ScreenManager, Screen

from pymysql.cursors import DictCursor
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.lang import Builder

sm = ScreenManager()

class MainScreen(Screen):
    pass
class RowDetailsScreen(Screen):
    pass


# Load the KV language string
kv_string = '''


<RowDetailsScreen>:
    name: 'row_details_screen'
    BoxLayout:
        
        orientation: 'vertical'
        height: self.minimum_height
        padding: 50
        
        canvas.before:
            Color: 
                rgba: 0, 0, 1, 0.9
            Line:
                width: 10
                rectangle: self.x, self.y, self.width, self.height
        
         
'''

# Load the KV string
Builder.load_string(kv_string)

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
        cursor.execute("SELECT spr_1_units.unit_shotname, zakaz_materials.is_plan, zakaz_materials.date_zakaz_plan, zakaz_materials.id_unit, zakaz_materials.remark, zakaz_materials.xCount, zakaz_materials.user_name, spr_1_materials_categories.material_category_name FROM zakaz_materials INNER JOIN spr_1_units ON zakaz_materials.id_unit=spr_1_units.id_unit INNER JOIN spr_1_materials_categories ON zakaz_materials.id_material_category=spr_1_materials_categories.id_material_category WHERE zakaz_materials.status=3")
        names = cursor.fetchall()
        #print(names)


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
                                     ("Oдиниці виміру", dp(10)),
                                     ("Опис", dp(50)),
                                     ("Дата", dp(20)),
                                     ("Тип замовлення", dp(20)),
                                     ("Користувач", dp(50))

                                 ],
                                 row_data=[(d['material_category_name'], d['xCount'],  d["unit_shotname"], d["remark"], d["date_zakaz_plan"], d["is_plan"], d['user_name']) for d in names],
                                 on_row_press=self.on_row_press
                                 )
        data_table.bind(on_row_press=self.on_row_press)
        data_table.bind(on_check_press=self.on_check_press)
        screen = MainScreen()
        screen.add_widget(data_table)
        sm.add_widget(screen)

        return sm

    def on_row_press(self, instance_table, instance_row):

        self.clear_screen()
        ind = instance_row.index
        row_data = instance_table.row_data[ind]

        # Display the details in labels
        row_details_screen = RowDetailsScreen()
        main_layout=BoxLayout(orientation= 'vertical', padding= 50)

        button_material_category_name=Button(text=row_data[0], size_hint = (1,1), background_color=(0.5, 0.5, 0.5, 0.5), font_size='20', color=(0, 0, 0, 1))
        button_remark = Button(text=str(row_data[3]), background_color=(0.5, 0.5, 0.5, 0.5), color=(0, 0, 0, 1))
        layout1 = BoxLayout(orientation='horizontal')
        button_id_unit= Button(text=row_data[2], font_size='20', color=(0, 0, 0, 1), size_hint = (0.5,1),
                pos_hint=  {"left":0.1},
                background_color=(0.5, 0.5, 0.5, 0.5))
        button_xCount=Button(text=str(row_data[1]), font_size='20', color = (0, 0, 0, 1),size_hint= (0.5, 1),
                pos_hint = {"right": 1},
                background_color = (0.5, 0.5, 0.5, 0.5) )
        button_zakaz_plan= Button(text="На "+str(row_data[4]), font_size='20', color=(0, 0, 0, 1), size_hint = (1,1),
                background_color=  (0.5, 0.5, 0.5, 0.5))
        button_is_plan = Button(text="Плановий" if row_data[5]==1 else "Позаплановий" , font_size='20', color=(0, 0, 0, 1), size_hint = (1,1),
                background_color=  (0.5, 0.5, 0.5, 0.5))
        layout2 = BoxLayout(orientation='horizontal')
        button_status = Button(text="ОЧІКУЄ ПОГОДЖЕННЯ", font_size='20', color="red", size_hint=(0.5, 1),
                               pos_hint={"left": 1},
                               background_color=(0.5, 0.5, 0.5, 0.5))
        button_active = Button(text="ПОГОДИТИ", font_size='20', color=(0, 0, 0, 1), size_hint=(0.5, 1),
                                   background_color="blue")
        button_user_name = Button(text=row_data[6], font_size='20', color=(0, 0, 0, 1), size_hint=(1, 1),
                               background_color=(0.5, 0.5, 0.5, 0.5))



        row_details_screen.add_widget(main_layout)

        main_layout.add_widget(button_material_category_name)
        main_layout.add_widget(button_remark)
        main_layout.add_widget(layout1)
        layout1.add_widget(button_id_unit)
        layout1.add_widget(button_xCount)
        main_layout.add_widget(button_zakaz_plan)
        main_layout.add_widget(button_is_plan)
        main_layout.add_widget(layout2)
        layout2.add_widget(button_status)
        layout2.add_widget(button_active)
        main_layout.add_widget( button_user_name)
        sm.add_widget(row_details_screen)

    def clear_screen(self):
        # Clear previous instances of RowDetailsScreen
        for screen in sm.screens:
            sm.remove_widget(screen)

    def on_check_press(self, instance_table, current_row):
        print(instance_table, current_row)

if __name__ == '__main__':



    MainApp().run()
    connection.close()




