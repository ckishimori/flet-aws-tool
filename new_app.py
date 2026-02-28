import flet as ft
import asyncio
from aws_auth import AWSAuthManager

async def main(page: ft.Page):
    page.title = "AWS SSO Login Tool"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 450
    page.window_height = 700
    
    auth_manager = AWSAuthManager()

    # Input Fields
    url_input = ft.TextField(
        label="AWS SSO Start URL", 
        hint_text="https://d-xxxx.awsapps.com",
        value=""
    )
    region_input = ft.TextField(
        label="AWS Region", 
        value="us-east-1",
        width=200
    )

    # Display Elements
    status_msg = ft.Text("Enter your details to begin", color="grey")
    code_display = ft.Text("", size=40, weight="bold", color="blue")
    progress_bar = ft.ProgressBar(visible=False)
    
    # Buttons
    copy_code_btn = ft.ElevatedButton("Copy Code", icon=ft.Icons.COPY, visible=False)
    copy_url_btn = ft.ElevatedButton("Copy URL", icon=ft.Icons.LINK, visible=False)
    copy_urlpluscode_btn = ft.ElevatedButton("Copy URL+Code", icon=ft.Icons.LINK, visible=False)

    async def start_login_flow(e):
        if not url_input.value or not region_input.value:
            status_msg.value = "⚠️ Please fill in both fields!"
            status_msg.color = "red"
            page.update()
            return

        # Prepare UI
        status_msg.value = "Contacting AWS..."
        status_msg.color = "blue"
        progress_bar.visible = True
        login_button.disabled = True
        page.update()

        try:
            # 1. Start Auth with user provided inputs
            auth_data, client_info = auth_manager.initiate_sso(
                url_input.value, 
                region_input.value
            )

            # 2. Update UI with results
            code_display.value = auth_data['userCode']
            status_msg.value = "Please authorize this device in your browser:"
            
            async def set_clipboard_code():
                await ft.Clipboard().set(value=auth_data['userCode'])

            async def set_clipboard_url():
                await ft.Clipboard().set(value=auth_data['verificationUri'])

            async def set_clipboard_urlpluscode():
                await ft.Clipboard().set(value=auth_data['verificationUriComplete'])

            copy_code_btn.visible = True
            copy_url_btn.visible = True
            copy_urlpluscode_btn.visible = True
            copy_code_btn.on_click = set_clipboard_code 
            copy_url_btn.on_click = set_clipboard_url
            copy_url_btnpluscode_btn.on_click = set_clipboard_urlpluscode
            
            page.update()

            # 3. Poll for token (Asynchronous)
            token = await auth_manager.poll_for_token_async(auth_data, client_info)
            
            status_msg.value = "✅ Success! Token received."
            status_msg.color = "green"
            progress_bar.visible = False
            print(f"Access Token: {token}")

        except Exception as ex:
            status_msg.value = f"Error: {str(ex)}"
            status_msg.color = "red"
        
        login_button.disabled = False
        page.update()

    login_button = ft.FilledButton("Generate Login Code", on_click=start_login_flow)

    # Layout Construction
    page.add(
        ft.Column([
            ft.Text("AWS SSO Configuration", size=20, weight="bold"),
            url_input,
            region_input,
            ft.Divider(height=20),
            login_button,
            ft.Divider(height=20),
            status_msg,
            progress_bar,
            ft.Container(
                content=ft.Column([
                    code_display,
                    ft.Row([copy_code_btn, copy_url_btn,copy_urlpluscode_btn], alignment="center")
                ], horizontal_alignment="center"),
                padding=20,
                bgcolor=ft.Colors.GREY_100,
                border_radius=10
            )
        ], horizontal_alignment="center", spacing=15)
    )

ft.app(target=main)
