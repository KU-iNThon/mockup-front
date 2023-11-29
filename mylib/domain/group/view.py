#!/usr/bin/env python3
from typing import List

from nicegui import ui
from nicegui.elements.table import Table
from nicegui.events import GenericEventArguments

from mylib.common.component.menu import set_menu


class GroupView:
    def __init__(self):
        pass

    def __call__(self):
        @ui.page("/group/{group_id}")
        async def page(group_id: int):
            await set_menu()
            await self.set_notices()
            await self.set_tasks()
            # await self.set_alarms()

        return page

    async def set_notices(self):
        columns = [
            {"name": "id", "label": "공지번호", "field": "id", "required": True},
            {"name": "title", "label": "제목", "field": "title", "required": True},
        ]
        rows = [
            {"id": 0, "title": "환영합니다."},
            {"id": 1, "title": "필수 확인!"},
        ]
        with ui.table(title="공지 목록", columns=columns, rows=rows, row_key="id").classes("w-60") as table:
            table.add_slot(
                "header",
                """
                 <q-tr :props="props">
                    <q-th auto-width />
                    <q-th auto-width>
                        공지번호
                    </q-th>
                    <q-th auto-width>
                        제목
                    </q-th>
                </q-tr>
                """,
            )
            table.add_slot(
                "body",
                """
                <q-tr :props="props">
                    <q-td auto-width >
                        <q-btn size="sm" color="warning" round dense icon="delete"
                            @click="() => $parent.$emit('delete', props.row)"
                        />
                    </q-td>
                    <q-td key="id" :props="props">
                        {{ props.row.id }}
                    </q-td>
                    <q-td key="title" :props="props">
                        {{ props.row.title }}
                    </q-td>
                </q-tr>
                """,
            )
            with table.add_slot("bottom-row"):
                with table.cell().props("colspan=3"):
                    ui.button(
                        "작성하기",
                        icon="add",
                        color="accent",
                        on_click=lambda: self.add_row(table=table, rows=rows, msg="새로운 공지를 등록했습니다."),
                    ).classes("w-full")
            table.on("delete", lambda e: self.delete(table=table, e=e, rows=rows, msg=f'공지 {e.args["id"]}번을 삭제했습니다.'))

    async def set_tasks(self):
        columns = [
            {"name": "id", "label": "활동번호", "field": "id", "required": True},
            {"name": "title", "label": "활동명", "field": "title", "required": True},
        ]
        rows = [
            {"id": 0, "title": "인사하기"},
            {"id": 1, "title": "활동하기"},
        ]
        with ui.table(title="활동 목록", columns=columns, rows=rows, row_key="id").classes("w-60") as table:
            table.add_slot(
                "header",
                """
                 <q-tr :props="props">
                    <q-th auto-width>
                        활동번호
                    </q-th>
                    <q-th auto-width>
                        활동명
                    </q-th>
                </q-tr>
                """,
            )
            table.add_slot(
                "body",
                """
                <q-tr :props="props">
                    <q-td key="id" :props="props">
                        {{ props.row.id }}
                    </q-td>
                    <q-td key="title" :props="props">
                        {{ props.row.title }}
                    </q-td>
                </q-tr>
                """,
            )
            with table.add_slot("bottom-row"):
                with table.cell().props("colspan=3"):
                    ui.button(
                        "작성하기",
                        icon="add",
                        color="accent",
                        on_click=lambda: self.add_row(table=table, rows=rows, msg="새로운 활동을 등록했습니다."),
                    ).classes("w-full")

    def add_row(self, table: Table, rows: List[dict], msg: str) -> None:
        new_id = max(dx["id"] for dx in rows) + 1 if rows else 0
        rows.append({"id": new_id, "title": "새로운 공지"})
        ui.notify(msg)
        table.update()

    def delete(self, table: Table, e: GenericEventArguments, rows: List[dict], msg: str) -> None:
        rows[:] = [row for row in rows if row["id"] != e.args["id"]]
        ui.notify(msg)
        table.update()


group = GroupView()()
