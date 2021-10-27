from kivy.lang import Builder
from kivy.uix.button import Button
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
        dict = json.load(io.open('data.json'))
        best_matches = get_close_matches(phrase, dict.keys())
        description = ''
        
        count = 1
        if best_matches[0] == phrase and best_matches[0] in dict:
            description = 'Description for "%s": \n' % best_matches[0]
            for d in dict[best_matches[0]]:
                description += '%s. %s\n' % (str(count), d)
                count += 1

        elif len(best_matches) > 0:
            self.show_popup(best_matches)

        else:
            description = "This word or phrase does't exist. Please double check it."

        self.ids.description.text = description

    def show_popup(self, best_matches):
        box = Popups()
    
        self.popup_window = Popup(title='Did you mean..?', 
            content=box, size_hint=(None, None), size=(400, 300))
        self.popup_window.open()

        y = 0.75
        for match in best_matches:
            self.add_button(match, y)
            y -= 0.22

        box.ids.close_btn.bind(on_press=self.popup_window.dismiss)

    def add_button(self, match, y):
        btn = Button(text=match, size_hint=(0.8, 0.2), pos_hint={'x': 0.1, 'y': y})
        btn.bind(on_press=lambda x: self.get_description(match))
        btn.bind(on_release=self.popup_window.dismiss)
        self.popup_window.content.add_widget(btn)

class Popups(FloatLayout): pass
        
class RootWidget(ScreenManager): pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MainApp().run()