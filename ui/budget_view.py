import flet as ft
from ui.components import section, section_primary, build_status_section
from data.repository import search_budgets, get_budgets, add_budget, delete_budget, update_budget, get_spent_for_category
from models.budget import Budget

def build_budget_view(page: ft.Page):

    cat_field    = ft.Dropdown(
        label="Category", width=180,
        options=[ft.dropdown.Option(c) for c in ["Food","Transport","Entertainment","Bills","Salary","Health","Other"]],
        value="Food",
    )
    limit_field   = ft.TextField(label="Monthly Limit", width=150, prefix="$")
    form_feedback = ft.Text("", size=13)
    form_button   = ft.ElevatedButton("Add Budget", icon=ft.Icons.ADD, color="white", bgcolor="blue")
    cancel_button = ft.ElevatedButton(
        "Cancel Edit", icon=ft.Icons.CANCEL, visible=False,
        style=ft.ButtonStyle(color="white", bgcolor={ft.ControlState.DEFAULT: "grey"}),
    )

    search_field = ft.TextField(label="Search by category...", width=260)
    result_count = ft.Text("", size=13, color="blue", weight=ft.FontWeight.BOLD)

    editing_id = {"value": None}
    status_container, status_text = build_status_section("Budget view loaded")
    list_column = ft.Column(spacing=8)

    def budget_card(b):
        spent     = get_spent_for_category(b.category)
        pct       = min(spent / b.limit, 1.0) if b.limit > 0 else 0
        remaining = b.limit - spent
        bar_color = "red" if pct >= 0.9 else ("orange" if pct >= 0.7 else "green")
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(b.category, weight=ft.FontWeight.BOLD, size=15, expand=True),
                    ft.Text(f"${spent:.2f} / ${b.limit:.2f}", size=13, color="grey"),
                    ft.IconButton(icon=ft.Icons.EDIT,   icon_color="blue", tooltip="Edit",   on_click=lambda e, bid=b.id: load_for_edit(bid)),
                    ft.IconButton(icon=ft.Icons.DELETE, icon_color="red",  tooltip="Delete", on_click=lambda e, bid=b.id: on_delete(bid)),
                ]),
                ft.ProgressBar(value=pct, color=bar_color, bgcolor="#eeeeee", height=10),
                ft.Text(f"${remaining:.2f} remaining", size=12, color=bar_color, italic=True),
            ], spacing=5),
            padding=15, bgcolor="white",
            border=ft.border.all(1, "#dddddd"), border_radius=10,
        )

    def render_list():
        list_column.controls.clear()
        results = search_budgets(query=search_field.value or "")
        if results:
            result_count.value = f"📋 {len(results)} budget{'s' if len(results) != 1 else ''} found"
            for b in results:
                list_column.controls.append(budget_card(b))
        else:
            result_count.value = "No matching budgets found."
            list_column.controls.append(
                ft.Container(content=ft.Text("No matching budgets found.", color="grey", italic=True, size=14), padding=20)
            )
        status_text.value = f"Status: {len(results)} budgets shown"
        page.update()

    def load_for_edit(budget_id):
        matches = [b for b in get_budgets() if b.id == budget_id]
        if not matches: return
        b = matches[0]
        cat_field.value    = b.category
        limit_field.value  = str(b.limit)
        editing_id["value"] = budget_id
        form_button.text   = "Save Changes"
        form_button.icon   = ft.Icons.SAVE
        form_button.bgcolor = "green"
        cancel_button.visible = True
        form_feedback.value = f"✏️ Editing: {b.category}"
        form_feedback.color = "blue"
        page.update()

    def on_delete(budget_id):
        matches = [b for b in get_budgets() if b.id == budget_id]
        name = matches[0].category if matches else "budget"
        delete_budget(budget_id)
        form_feedback.value = f"🗑️ '{name}' budget deleted."
        form_feedback.color = "red"
        render_list()

    def on_submit(e):
        if not limit_field.value:
            form_feedback.value = "⚠️ Limit is required."
            form_feedback.color = "red"
            page.update()
            return
        try:
            limit = float(limit_field.value)
        except:
            form_feedback.value = "⚠️ Limit must be a valid number."
            form_feedback.color = "red"
            page.update()
            return

        b = Budget(cat_field.value, limit)

        if editing_id["value"] is not None:
            update_budget(editing_id["value"], b)
            form_feedback.value = f"✅ '{b.category}' updated!"
        else:
            add_budget(b)
            form_feedback.value = f"✅ '{b.category}' added!"

        form_feedback.color   = "green"
        limit_field.value     = ""
        cat_field.value       = "Food"
        editing_id["value"]   = None
        form_button.text      = "Add Budget"
        form_button.icon      = ft.Icons.ADD
        form_button.bgcolor   = "blue"
        cancel_button.visible = False
        render_list()

    def on_cancel(e):
        limit_field.value     = ""
        cat_field.value       = "Food"
        editing_id["value"]   = None
        form_button.text      = "Add Budget"
        form_button.icon      = ft.Icons.ADD
        form_button.bgcolor   = "blue"
        cancel_button.visible = False
        form_feedback.value   = "Edit cancelled."
        form_feedback.color   = "grey"
        page.update()

    form_button.on_click   = on_submit
    cancel_button.on_click = on_cancel
    search_field.on_change = lambda e: render_list()

    render_list()

    return ft.Column([
        ft.Text("Budget", size=24, weight=ft.FontWeight.BOLD, color="blue"),
        ft.Text("Manage your category spending limits", size=13, color="grey", italic=True),
        ft.Divider(height=15),
        section_primary(
            "Budget Form",
            ft.Column([
                ft.Row([cat_field, limit_field, form_button, cancel_button], wrap=True, spacing=10),
                form_feedback,
            ]),
            subtitle="Add or edit a category budget",
        ),
        section(
            "Search & Filter",
            ft.Column([
                ft.Row([search_field, ft.ElevatedButton("Reset", icon=ft.Icons.CLEAR, on_click=lambda e: (setattr(search_field, 'value', ''), render_list()))], spacing=10),
                result_count,
            ]),
            subtitle="Search budgets by category name",
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("Budget List", size=18, weight=ft.FontWeight.BOLD, color="green"),
                ft.Divider(height=10, color="green"),
                list_column,
            ]),
            padding=15, margin=ft.margin.only(bottom=15),
            bgcolor="white", border=ft.border.all(1, "green"), border_radius=10,
        ),
        status_container,
    ], spacing=0, scroll=ft.ScrollMode.ADAPTIVE)