import flet as ft

def main(page: ft.Page):
    page.title = "flet aws tool"

    top_row = ft.Row(
        controls=
            [
                ft.Text("flet aws tool", size=30)
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START
    )

    page.add(top_row)

if __name__ == "__main__":
    ft.app(target=main)