from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
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

        if len(best_match) > 0 and best_match[0] in dict:
            description = 'Description for "%s": \n' % best_match[0].title()
            for d in dict[best_match[0]]:
                description += d + '\n'
            self.ids.description.text = description
        else:
            self.ids.description.text = "This word or phrase does't exist. Please double check it."





class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MainApp().run()