import flet as ft

def main(page: ft.Page):
    page.title = "App Bar Example"

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.PALETTE),
        leading_width=40,
        title=ft.Text("My Flet App"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.Icons.FILTER_VINTAGE),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(content="Item 1"),
                    ft.PopupMenuItem(content="Item 2"),
                ]
            ),
        ],
    )
    page.add(ft.Text("Body content goes here!"))

ft.app(target=main)