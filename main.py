from db import main_db
import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Todo List"

    task_list = ft.Column(spacing=15)
    filter_type = 'all'

    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_tasks(filter_type):
            task_list.controls.append(
                view_task(task_id, task_text, completed)
            )
        page.update()

    def view_task(task_id, task_text, completed):
        task_field = ft.TextField(
            value=task_text,
            read_only=True,
            expand=True
        )

        checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        def enable_edit(e):
            task_field.read_only = not task_field.read_only
            page.update()

        def save_task(e):
            main_db.update_task(task_id, new_task=task_field.value)
            task_field.read_only = True
            page.update()

        def delete_task_ui(e):
            main_db.delete_task(task_id)
            load_tasks()

        row = ft.Row([
            checkbox,
            task_field,
            ft.IconButton(ft.Icons.EDIT, on_click=enable_edit),
            ft.IconButton(ft.Icons.SAVE, on_click=save_task),
            ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=delete_task_ui),
        ])

        return row

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id, completed=is_completed)
        load_tasks()

    def add_task(e):
        if task_input.value:
            main_db.add_task(task_input.value)
            task_input.value = ""
            load_tasks()

    def set_filter(value):
        nonlocal filter_type
        filter_type = value
        load_tasks()

    def clear_completed(e):
        main_db.delete_completed_tasks()
        load_tasks()

    task_input = ft.TextField(
        label="Введите задачу",
        expand=True,
        on_submit=add_task
    )

    add_button = ft.IconButton(ft.Icons.ADD, on_click=add_task)

    filter_buttons = ft.Row(
        [
            ft.ElevatedButton("Все", on_click=lambda e: set_filter('all')),
            ft.ElevatedButton("В работе", on_click=lambda e: set_filter('uncompleted')),
            ft.ElevatedButton("Готово", on_click=lambda e: set_filter('completed')),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY
    )

    clear_button = ft.ElevatedButton(
        "Очистить выполненные",
        icon=ft.Icons.DELETE_SWEEP,
        icon_color=ft.Colors.RED,
        on_click=clear_completed
    )

    page.add(
        ft.Row([task_input, add_button]),
        filter_buttons,
        clear_button,
        task_list
    )

    load_tasks()


if __name__ == '__main__':
    main_db.init_db()
    ft.run(main)
