import flet as ft

# Example of a declarative MenuBar in Flet
@ft.component
def MenuApp():
    # Defines the menu structure within the component
    return ft.MenuBar(
        expand=True,
        controls=[
            ft.SubmenuButton(
                content=ft.Text("File"),
                controls=[
                    ft.MenuItemButton(content=ft.Text("Open"), on_click=lambda e: print("Open")),
                    ft.MenuItemButton(content=ft.Text("Save"), on_click=lambda e: print("Save")),
                ],
            ),
        ],
    )

ft.run(lambda page: page.render(MenuApp))