from nicegui import app, ui


async def set_menu():
    with ui.row().classes("w-full items-center"):
        result = ui.label().classes("mr-auto")
        with ui.button(icon="menu"):
            with ui.menu() as menu:
                ui.menu_item("프로필", lambda: ui.open("/profile"))
                ui.menu_item("모집중", lambda: ui.open("/groups/recruits"))
                ui.menu_item("로그아웃", lambda: (app.storage.user.clear(), ui.open("/login")))
                ui.separator()
                ui.menu_item("닫기", on_click=menu.close)
