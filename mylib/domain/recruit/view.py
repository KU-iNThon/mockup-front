#!/usr/bin/env python3
from fastapi import HTTPException
from nicegui import ui

from mylib.common.component.menu import set_menu


class RecruitView:
    def __init__(self):
        self.__data1 = {
            "id": 1,
            "name": "클라이밍 소모임",
            "description": "초보자도 환영합니다",
            "current_people": 3,
            "max_people": 5,
        }
        self.__data0 = {"id": 0, "name": "기상 스터디", "description": "해피 기상!", "current_people": 0, "max_people": 10}

    def __call__(self):
        @ui.page("/group/{group_id}/recruit")
        async def page(group_id: int):
            await set_menu()
            if group_id == 0:
                await self.set_detail(data=self.__data0),
            elif group_id == 1:
                await self.set_detail(data=self.__data1),
            else:
                raise HTTPException(status_code=404, detail="모집글을 찾을 수 없습니다.")

        return page

    async def set_detail(self, data: dict):
        ui.html(f"<h1>{data['name']}</h1>")
        ui.html(f"<p>{data['description']}</p>")
        with ui.row():
            ui.label(f"정원: {data['current_people']}/{data['max_people']}")
        ui.button("지원하기", on_click=lambda: ui.notify(f"{data['name']}에 지원했습니다."))


recruit = RecruitView()()
