import flet as ft
from ui.components import section_primary, section, build_status_section
from data.repository import search_transactions, add_transaction, delete_transaction, update_transaction, get_transactions
from models.transaction import Transaction

def build_transactions_view(page: ft.Page):

    # === FORM FIELDS ===
    desc_field     = ft.TextField(label="Description", width=180)
    amount_field   = ft.TextField(label="Amount", width=120, prefix="$")
    category_field = ft.Dropdown(
        label="Category", width=160,
        options=[ft.dropdown.Option(c) for c in ["Food","Transport","Entertainment","Bills","Salary","Health","Other"]],
        value="Food",
    )
    type_field = ft.Dropdown(
        label="Type", width=130,
        options=[ft.dropdown.Option("expense"), ft.dropdown.Option("income")],
        value="expense",
    )
    date_field    = ft.TextField(label="Date", width=130, hint_text="YYYY-MM-DD", value="2026-03-10")
    form_feedback = ft.Text("", size=13)
    form_button   = ft.ElevatedButton("Add Transaction", icon=ft.Icons.ADD, color="white", bgcolor="blue")
    cancel_button = ft.ElevatedButton(
        "Cancel Edit", icon=ft.Icons.CANCEL, visible=False,
        style=ft.ButtonStyle(color="white", bgcolor={ft.ControlState.DEFAULT: "grey"}),
    )

    # === SEARCH FIELDS ===
    search_field    = ft.TextField(label="Search by description or date...", width=280)
    category_filter = ft.Dropdown(
        label="Category Filter", width=180,
        options=[ft.dropdown.Option(c) for c in ["All","Food","Transport","Entertainment","Bills","Salary","Health","Other"]],
        value="All",
    )
    type_filter = ft.Dropdown(
        label="Type Filter", width=140,
        options=[ft.dropdown.Option(t) for t in ["All","income","expense"]],
        value="All",
    )
    result_count = ft.Text("", size=13, color="blue", weight=ft.FontWeight.BOLD)

    # === STATE ===
    editing_id = {"value": None}
    status_container, status_text = build_status_section("Ready")
    list_column = ft.Column(spacing=8)

    def clear_form():
        desc_field.value     = ""
        amount_field.value   = ""
        category_field.value = "Food"
        type_field.value     = "expense"
        date_field.value     = "2026-03-10"
        form_feedback.value  = ""
        editing_id["value"]  = None
        form_button.text     = "Add Transaction"
        form_button.icon     = ft.Icons.ADD
        form_button.bgcolor  = "blue"
        cancel_button.visible = False

    def transaction_row(t):
        is_income = t.transaction_type == "income"
        return ft.Container(
            content=ft.Row([
                ft.Text("📈" if is_income else "📉", size=16, width=25),
                ft.Column([
                    ft.Text(t.description, weight=ft.FontWeight.BOLD, size=14),
                    ft.Text(f"{t.category}  •  {t.date}", size=11, color="grey"),
                ], spacing=1, expand=True),
                ft.Text(
                    f"${t.amount:.2f}",
                    size=14, weight=ft.FontWeight.BOLD,
                    color="green" if is_income else "red",
                    width=85,
                ),
                ft.Container(
                    content=ft.Text(t.transaction_type.title(), size=11, color="white", text_align=ft.TextAlign.CENTER),
                    bgcolor="green" if is_income else "red",
                    border_radius=10,
                    padding=ft.padding.symmetric(horizontal=8, vertical=3),
                    width=70,
                ),
                ft.IconButton(icon=ft.Icons.EDIT,   icon_color="blue", tooltip="Edit",   on_click=lambda e, tid=t.id: load_for_edit(tid)),
                ft.IconButton(icon=ft.Icons.DELETE, icon_color="red",  tooltip="Delete", on_click=lambda e, tid=t.id: on_delete(tid)),
            ], spacing=8),
            padding=10,
            bgcolor="white",
            border=ft.border.all(1, "#e8e8e8"),
            border_radius=8,
        )

    def render_list():
        list_column.controls.clear()
        results = search_transactions(
            query=search_field.value or "",
            category=category_filter.value,
            transaction_type=type_filter.value,
        )
        if results:
            result_count.value = f"📋 {len(results)} matching transaction{'s' if len(results) != 1 else ''}"
            for t in results:
                list_column.controls.append(transaction_row(t))
        else:
            result_count.value = "No matching transactions found."
            list_column.controls.append(
                ft.Container(content=ft.Text("No matching transactions found.", color="grey", italic=True, size=14), padding=20)
            )
        total = len(get_transactions())
        status_text.value = f"Status: Showing {len(results)} of {total} transactions"
        page.update()

    def load_for_edit(transaction_id):
        matches = [t for t in get_transactions() if t.id == transaction_id]
        if not matches: return
        t = matches[0]
        desc_field.value     = t.description
        amount_field.value   = str(t.amount)
        category_field.value = t.category
        type_field.value     = t.transaction_type
        date_field.value     = t.date
        editing_id["value"]  = transaction_id
        form_button.text     = "Save Changes"
        form_button.icon     = ft.Icons.SAVE
        form_button.bgcolor  = "green"
        cancel_button.visible = True
        form_feedback.value  = f"✏️ Editing: {t.description}"
        form_feedback.color  = "blue"
        page.update()

    def on_delete(transaction_id):
        matches = [t for t in get_transactions() if t.id == transaction_id]
        name = matches[0].description if matches else "record"
        delete_transaction(transaction_id)
        form_feedback.value = f"🗑️ '{name}' deleted."
        form_feedback.color = "red"
        render_list()

    def on_submit(e):
        if not desc_field.value or not amount_field.value or not date_field.value:
            form_feedback.value = "⚠️ Description, amount and date are required."
            form_feedback.color = "red"
            page.update()
            return
        try:
            amount = float(amount_field.value)
        except:
            form_feedback.value = "⚠️ Amount must be a valid number."
            form_feedback.color = "red"
            page.update()
            return

        t = Transaction(desc_field.value, amount, category_field.value, type_field.value, date_field.value)

        if editing_id["value"] is not None:
            update_transaction(editing_id["value"], t)
            form_feedback.value = f"✅ '{t.description}' updated!"
        else:
            add_transaction(t)
            form_feedback.value = f"✅ '{t.description}' added!"

        form_feedback.color = "green"
        clear_form()
        render_list()

    def on_cancel(e):
        clear_form()
        form_feedback.value = "Edit cancelled."
        form_feedback.color = "grey"
        page.update()

    def on_reset_filters(e):
        search_field.value    = ""
        category_filter.value = "All"
        type_filter.value     = "All"
        render_list()

    form_button.on_click      = on_submit
    cancel_button.on_click    = on_cancel
    search_field.on_change    = lambda e: render_list()
    category_filter.on_change = lambda e: render_list()
    type_filter.on_change     = lambda e: render_list()

    render_list()

    return ft.Column([
        ft.Text("Transactions", size=24, weight=ft.FontWeight.BOLD, color="blue"),
        ft.Text("Create, search, edit and delete transactions", size=13, color="grey", italic=True),
        ft.Divider(height=15),
        section_primary(
            "Transaction Form",
            ft.Column([
                ft.Row([desc_field, amount_field, category_field, type_field, date_field], wrap=True, spacing=10),
                ft.Row([form_button, cancel_button], spacing=10),
                form_feedback,
            ]),
            subtitle="Add a new transaction or edit an existing one",
        ),
        section(
            "Search & Filter",
            ft.Column([
                ft.Row([search_field, category_filter, type_filter,
                        ft.ElevatedButton("Reset Filters", icon=ft.Icons.CLEAR, on_click=on_reset_filters)], wrap=True, spacing=10),
                result_count,
            ]),
            subtitle="Narrow results by description, category or type",
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("Transactions List", size=18, weight=ft.FontWeight.BOLD, color="green"),
                ft.Divider(height=10, color="green"),
                list_column,
            ]),
            padding=15, margin=ft.margin.only(bottom=15),
            bgcolor="white", border=ft.border.all(1, "green"), border_radius=10,
        ),
        status_container,
    ], spacing=0, scroll=ft.ScrollMode.ADAPTIVE)