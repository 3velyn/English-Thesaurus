from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App

import json, io, sys

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

Builder.load_file('design.kv')

class ThesaurusScreen(Screen):


    def get_description(self, phrase):
        dict = json.load(io.open('data.json', encoding='utf-8'))
        phrase = phrase.lower()

        if phrase in dict:
            description = ''
            for d in dict[phrase]:
                description += d + '\n'
            self.ids.description.text = description
        else:
            self.ids.description.text = 'Nemaaa'





class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MainApp().run()