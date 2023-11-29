#!/usr/bin/env python3

from nicegui import ui

from mylib.common.component.menu import set_menu


class RecruitListView:
    def __init__(self):
        # TODO :  DB Sync
        self.__columns = [
            {"name": "name", "label": "이름", "field": "name", "required": True},
            {"name": "current_people", "label": "현재 인원수", "field": "current_people", "required": True},
            {"name": "max_people", "label": "최대 인원수", "field": "max_people", "required": True},
        ]
        self.__rows = [
            {"id": 0, "name": "기상 스터디", "current_people": 0, "max_people": 10},
            {"id": 1, "name": "클라이밍", "current_people": 4, "max_people": 5},
        ]

    def __call__(self):
        @ui.page("/groups/recruits")
        async def page():
            await set_menu()
            await self.set_group(title="모집글", data=self.__rows),

        return page

    async def set_group(self, title: str, data: list):
        with ui.table(
            title=title,
            columns=self.__columns,
            rows=data,
            pagination=10,
            selection="single",
            on_select=lambda e: ui.open(f"/group/{e.selection[0]['id']}/recruit"),
        ).classes("w-96") as table:
            with table.add_slot("top-right"):
                with ui.input(placeholder="Search").props("type=search").bind_value(table, "filter").add_slot("append"):
                    ui.icon("search")


recruit_list = RecruitListView()()
