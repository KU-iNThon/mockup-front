from nicegui import app, ui

from mylib.common.middleware.auth import AuthMiddleware


@ui.page("/")
def main_page() -> None:
    with ui.column().classes("absolute-center items-center"):
        ui.label(f'Hello {app.storage.user["username"]}!').classes("text-2xl")
        ui.button(on_click=lambda: (app.storage.user.clear(), ui.open("/login")), icon="logout").props("outline round")


if __name__ in {"__main__", "__mp_main__"}:
    # import pages
    from mylib.domain.login.view import login
    from mylib.domain.profile.view import profile
    from mylib.domain.recruit.view import recruit

    views = [login, profile, recruit]

    app.add_middleware(AuthMiddleware)
    ui.run(storage_secret="happy development!!")
