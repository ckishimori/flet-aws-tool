import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Row(
            controls=[
                # First Column: Aligned to the top (START)
                ft.Column(
                    controls=[
                        ft.Container(ft.Text("Top Item 1"), bgcolor=ft.Colors.BLUE_100),
                        ft.Container(ft.Text("Top Item 2"), bgcolor=ft.Colors.BLUE_200),
                    ],
                    alignment=ft.MainAxisAlignment.START, # Vertical alignment for the column
                    height=200, # Providing height gives space to align within
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Horizontal alignment
                ),
                
                # Second Column: Aligned to the bottom (END)
                ft.Column(
                    controls=[
                        ft.Container(ft.Text("Bottom Item 1"), bgcolor=ft.Colors.GREEN_100),
                        ft.Container(ft.Text("Bottom Item 2"), bgcolor=ft.Colors.GREEN_200),
                    ],
                    alignment=ft.MainAxisAlignment.END, # Vertical alignment for the column
                    height=200, # Providing height gives space to align within
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Horizontal alignment
                ),
            ],
            # Row alignment controls horizontal positioning of the columns
            alignment=ft.MainAxisAlignment.CENTER, 
            vertical_alignment=ft.CrossAxisAlignment.START, # Row vertical alignment
            spacing=20,
        )
    )

ft.app(target=main)
