import flet as ft
from shared import *
from aws import *

@ft.control
class aws_app(ft.Column):

    def init(self):
        self.starturl = ft.TextField(ref=aws_starturl, label="Start URL", hint_text="Start URL", width=400)
        self.region = ft.TextField(ref=aws_region, label="Region", hint_text="Region", width=200)
        self.devicecodeurl = ft.TextField(ref=aws_devicecodeurl, label="Device Code URL", hint_text="Device Code URL", width=400)
        self.controls = [
            self.starturl,
            self.region,
            ft.Button(content="Get Login URL", on_click=self.get_login_url_clicked),
            self.devicecodeurl
        ]

    def get_login_url_clicked(e):
        set_login_url()
   
def main(page: ft.Page):
    page.title = "flet aws tool"
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.update()    

    app = aws_app()
    page.add(app)
    

if __name__ == "__main__":
    ft.run(main)