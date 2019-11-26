import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from randstrip import createStrip

class strip_Layout(App):
	img = Image(source="./android.png")
	
	def build(self):
		layout = BoxLayout(orientation="vertical")
		newStrip_Button = Button(text="New Strip", size_hint=(1,.3))
		newStrip_Button.bind(on_press=self.newStrip)
		layout.add_widget(self.img)
		layout.add_widget(newStrip_Button)
		return layout
	
	def newStrip(self,instance):
		createStrip("android.png",30)
		self.img.reload()

if __name__=="__main__":
	app = strip_Layout()
	app.run()
