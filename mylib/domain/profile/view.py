#!/usr/bin/env python3
from asyncio import gather

from nicegui import ui


class ProfileView:
    def __init__(self):
        # TODO :  DB Sync
        self.__columns = [
            {"name": "name", "label": "이름", "field": "name", "required": True},
            {"name": "completed_tasks", "label": "완료한 활동 수", "field": "completed_tasks", "required": True},
            {"name": "total_tasks", "label": "총 활동 수", "field": "total_tasks", "required": True},
            {
                "name": "completed_ratio",
                "label": "완료한 활동 비율",
                ":field": "row => (row.completed_tasks / row.total_tasks).toFixed(1)",
            },
        ]
        self.__participant_rows = [
            {"id": 0, "name": "기상 스터디", "completed_tasks": 0, "total_tasks": 18},
            {"id": 1, "name": "클라이밍 소모임", "completed_tasks": 3, "total_tasks": 15},
        ]

        self.__managed_rows = [
            {"id": 0, "name": "등산 소모임", "completed_tasks": 5, "total_tasks": 6},
        ]

    def __call__(self):
        @ui.page("/profile")
        async def page():
            await gather(
                self.set_info(title="이용자 정보"),
                self.set_group(title="가입한 소모임", data=self.__participant_rows),
                self.set_group(title="운영중인 소모임", data=self.__managed_rows),
            )

        return page

    async def set_group(self, title: str, data: list):
        with ui.table(title=title, columns=self.__columns, rows=data, pagination=10).classes("w-96") as table:
            with table.add_slot("top-right"):
                with ui.input(placeholder="Search").props("type=search").bind_value(table, "filter").add_slot("append"):
                    ui.icon("search")

    async def set_info(self, title: str):
        columns = [
            {"name": "name", "label": "이름", "field": "name", "required": True},
            {"name": "region", "label": "지역", "field": "region", "required": True},
            {"name": "user_id", "label": "아이디", "field": "user_id", "required": True},
            {"name": "point", "label": "포인트", "field": "point", "required": True},
            {"name": "completed_tasks", "label": "완료한 활동 수", "field": "completed_tasks", "required": True},
            {"name": "total_tasks", "label": "총 활동 수", "field": "total_tasks", "required": True},
            {
                "name": "completed_ratio",
                "label": "완료한 활동 비율",
                ":field": "row => (row.completed_tasks / row.total_tasks).toFixed(1)",
            },
        ]
        # TODO : DB Sync
        data = [
            {
                "id": 0,
                "name": "관리자",
                "region": "서울",
                "user_id": "admin",
                "point": 20,
                "total_tasks": 10,
                "completed_tasks": 2,
            },
        ]
        with ui.table(title=title, columns=columns, rows=data).classes("w-96") as table:
            pass


profile = ProfileView()()
