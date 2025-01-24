from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from datetime import datetime, timedelta
import threading
import time
import random

# Sample Hadiths
hadiths = [
    "The best among you are those who have the best manners and character. - Prophet Muhammad (PBUH)",
    "Actions are judged by intentions, so each person will get what they intended. - Prophet Muhammad (PBUH)",
    "The seeking of knowledge is obligatory for every Muslim. - Prophet Muhammad (PBUH)",
    "The strongest among you is the one who controls his anger. - Prophet Muhammad (PBUH)",
    "None of you truly believes until he loves for his brother what he loves for himself. - Prophet Muhammad (PBUH)"
]

KV = '''
ScreenManager:
    MainScreen:

<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        MDCard:
            orientation: 'vertical'
            size_hint: (1, None)
            height: '200dp'
            padding: 10
            MDLabel:
                text: "Hadith of the Day"
                halign: "center"
                theme_text_color: "Primary"
                font_style: "H5"
            MDLabel:
                id: hadith_label
                text: ""
                halign: "center"
                theme_text_color: "Secondary"
                font_style: "Body1"

        MDRaisedButton:
            text: "Show Random Hadith"
            pos_hint: {"center_x": .5}
            on_release: app.show_random_hadith()

        MDRaisedButton:
            text: "Start Prayer Notification"
            pos_hint: {"center_x": .5}
            on_release: app.schedule_prayer_notification()

        MDLabel:
            id: prayer_time_label
            text: ""
            halign: "center"
            theme_text_color: "Secondary"
            font_style: "Body1"

        MDLabel:
            id: prayer_history_label
            text: "Prayer History:\n"
            halign: "left"
            theme_text_color: "Secondary"
            font_style: "Body1"
'''

class MainScreen(Screen):
    pass

class IslamicApp(MDApp):
    def build(self):
        self.hadith_label = ""
        self.prayer_history = []
        return Builder.load_string(KV)

    def show_random_hadith(self):
        self.hadith_label = random.choice(hadiths)
        self.root.ids.hadith_label.text = self.hadith_label

    def schedule_prayer_notification(self):
        # Schedule prayer notification for 5 minutes from now
        self.prayer_time = datetime.now() + timedelta(minutes=5)
        self.root.ids.prayer_time_label.text = f"Next prayer time: {self.prayer_time.strftime('%H:%M:%S')}"
        threading.Thread(target=self.start_countdown).start()

    def start_countdown(self):
        # Countdown for 5 minutes
        for remaining in range(300, 0, -1):
            time.sleep(1)
            if remaining == 1:
                self.show_prayer_notification()

    def show_prayer_notification(self):
        # Show a dialog notification
        Clock.schedule_once(lambda dt: self.show_dialog("It's time to pray!"), 0)
        self.log_prayer()

    def log_prayer(self):
        # Log the prayer in history
        prayer_time = datetime.now().strftime('%H:%M:%S')
        self.prayer_history.append(prayer_time)
        self.update_prayer_history()

    def update_prayer_history(self):
        history_text = "Prayer History:\n" + "\n".join(self.prayer_history)
        self.root.ids.prayer_history_label.text = history_text

    def show_dialog(self, message):
        dialog = MDDialog(title="Prayer Notification", text=message, size_hint=(0.8, 1))
        dialog.open()

if __name__ == '__main__':
    IslamicApp().run()