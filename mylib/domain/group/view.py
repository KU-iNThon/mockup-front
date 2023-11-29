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
            ui.html("<h1>소모임 이름</h1>")
            ui.html("<p>소모임 설명</p>")
            await self.set_notices()
            await self.set_tasks()
            await self.set_new_participant_alarm()
            await self.set_task_completed_alarm()

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
                                <q-th auto-width />
                                <q-th auto-width>
                                    활동번호
                                </q-th>
                                <q-th auto-width>
                                    활동명
                                </q-th>
                                <q-th auto-width />
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
                                <q-td auto-width >
                                    <q-btn size="sm" color="warning" round dense icon="check"
                                        @click="() => $parent.$emit('complete_task', props.row)"
                                    />
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
            table.on("delete", lambda e: self.delete(table=table, e=e, rows=rows, msg=f'활동 {e.args["id"]}번을 삭제했습니다.'))
            table.on("complete_task", lambda e: self.complete_task(table=table, e=e))

    async def set_new_participant_alarm(self):
        columns = [
            {"name": "id", "label": "신청자 ID", "field": "id", "required": True},
            {"name": "nickname", "label": "신청자", "field": "nickname", "required": True},
        ]
        rows = [
            {"id": "test@com", "nickname": "신규회원1"},
        ]
        with ui.table(title="신규 신청", columns=columns, rows=rows, row_key="id").classes("w-60") as table:
            table.add_slot(
                "header",
                """
                             <q-tr :props="props">
                                <q-th auto-width />
                                <q-th auto-width>
                                    신청자 ID
                                </q-th>
                                <q-th auto-width>
                                    신청자
                                </q-th>
                                <q-th auto-width />
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
                                <q-td key="nickname" :props="props">
                                    {{ props.row.nickname }}
                                </q-td>
                                <q-td auto-width >
                                    <q-btn size="sm" color="info" round dense icon="check"
                                        @click="() => $parent.$emit('accept_participant', props.row)"
                                    />
                                </q-td>
                            </q-tr>
                            """,
            )
            table.on("delete", lambda e: self.delete(table=table, e=e, rows=rows, msg=f'{e.args["id"]}의 신청을 취소했습니다.'))
            table.on("accept_participant", lambda e: self.accept_participant(table=table, e=e, rows=rows))

    async def set_task_completed_alarm(self):
        columns = [
            {"name": "id", "label": "신청자 ID", "field": "id", "required": True},
            {"name": "nickname", "label": "신청자", "field": "nickname", "required": True},
            {"name": "task_id", "label": "활동 ID", "field": "task_id", "required": True},
            {"name": "task_name", "label": "활동명", "field": "task_name", "required": True},
        ]
        rows = [
            {"id": "test@com", "nickname": "회원1", "task_id": 1, "task_name": "인사하기"},
        ]
        with ui.table(title="활동 완료 요청", columns=columns, rows=rows, row_key="id").classes("w-60") as table:
            table.add_slot(
                "header",
                """
                             <q-tr :props="props">
                                <q-th auto-width />
                                <q-th auto-width>
                                    신청자 ID
                                </q-th>
                                <q-th auto-width>
                                    신청자
                                </q-th>
                                <q-th auto-width>
                                    활동 ID
                                </q-th>
                                <q-th auto-width>
                                    활동명
                                </q-th>
                                <q-th auto-width />
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
                                <q-td key="nickname" :props="props">
                                    {{ props.row.nickname }}
                                </q-td>
                                <q-td key="task_id" :props="props">
                                    {{ props.row.task_id }}
                                </q-td>
                                <q-td key="task_name" :props="props">
                                    {{ props.row.task_name }}
                                </q-td>
                                <q-td auto-width >
                                    <q-btn size="sm" color="info" round dense icon="check"
                                        @click="() => $parent.$emit('accept_task', props.row)"
                                    />
                                </q-td>
                            </q-tr>
                            """,
            )
            table.on("delete", lambda e: self.delete(table=table, e=e, rows=rows, msg=f'{e.args["id"]}의 요청을 취소했습니다.'))
            table.on("accept_task", lambda e: self.accept_task(table=table, e=e, rows=rows))

    def add_row(self, table: Table, rows: List[dict], msg: str) -> None:
        new_id = max(dx["id"] for dx in rows) + 1 if rows else 0
        rows.append({"id": new_id, "title": "새로운 공지"})
        ui.notify(msg)
        table.update()

    def delete(self, table: Table, e: GenericEventArguments, rows: List[dict], msg: str) -> None:
        rows[:] = [row for row in rows if row["id"] != e.args["id"]]
        ui.notify(msg)
        table.update()

    def accept_participant(self, table: Table, e: GenericEventArguments, rows: List[dict]) -> None:
        ui.notify(f"{e.args['id']}의 신청을 수락했습니다.")
        rows[:] = [row for row in rows if row["id"] != e.args["id"]]
        table.update()

    def accept_task(self, table: Table, e: GenericEventArguments, rows: List[dict]) -> None:
        ui.notify(f"{e.args['id']}의 요청을 수락했습니다.")
        rows[:] = [row for row in rows if row["id"] != e.args["id"]]
        table.update()

    def complete_task(self, table: Table, e: GenericEventArguments) -> None:
        ui.notify(f"{e.args['title']}를 완료했습니다.")


group = GroupView()()
