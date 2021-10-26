from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.app import App

from difflib import get_close_matches

import json, io, sys

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

Builder.load_file('design.kv')

class ThesaurusScreen(Screen):

    def get_description(self, phrase):
        dict = json.load(io.open('data.json', encoding='utf-8'))
        best_match = get_close_matches(phrase.lower(), dict.keys())

        if phrase.lower() in dict:
            description = 'Description for "%s": \n' % phrase.title()
            count = 1

            for d in dict[phrase.lower()]:
                description += '%s. %s\n' % (str(count), d)
                count += 1

            self.ids.description.text = description

        elif len(best_match) > 0:
            Popups.show_popup(self, best_match[0])

        else:
            self.ids.description.text = "This word or phrase does't exist. Please double check it."

class Popups(FloatLayout):

    def show_popup(self, phrase):
        layout = Popups()
        layout.ids.popup_label.text = 'Did you mean "%s" instead?' % phrase.title()
    
        popup_window = Popup(title='Did you mean..?', 
            content=layout, size_hint=(None, None), size=(400, 300))
        popup_window.open()

        layout.ids.yes_btn.bind(on_press=lambda x: ThesaurusScreen.get_description(self, phrase))
        layout.ids.yes_btn.bind(on_press=popup_window.dismiss)
        layout.ids.close_btn.bind(on_press=popup_window.dismiss)
        

class RootWidget(ScreenManager): pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MainApp().run()