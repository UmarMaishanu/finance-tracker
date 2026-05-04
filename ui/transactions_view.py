import flet as ft
from ui.components import section_primary, section, build_status_section
from data.repository import (
    search_transactions, get_transactions,
    add_transaction, delete_transaction, update_transaction,
    is_budget_available, confirm_transaction, revert_transaction,
)
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

    # === SEARCH / FILTER FIELDS ===
    search_field    = ft.TextField(label="Search by description or date...", width=260)
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
    status_filter = ft.Dropdown(
        label="Status Filter", width=150,
        options=[ft.dropdown.Option(s) for s in ["All","pending","confirmed"]],
        value="All",
    )
    result_count  = ft.Text("", size=13, color="blue", weight=ft.FontWeight.BOLD)
    list_feedback = ft.Text("", size=13)  # feedback shown near the list

    editing_id = {"value": None}
    status_container, status_text = build_status_section("Ready")
    list_column = ft.Column(spacing=8)

    # === HELPERS ===
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
        is_income  = t.transaction_type == "income"
        is_pending = t.status == "pending"

        status_badge = ft.Container(
            content=ft.Text(
                t.status.title(), size=11, color="white",
                text_align=ft.TextAlign.CENTER,
            ),
            bgcolor="orange" if is_pending else "green",
            border_radius=10,
            padding=ft.padding.symmetric(horizontal=8, vertical=3),
            width=80,
        )

        if is_pending:
            state_button = ft.ElevatedButton(
                "Confirm",
                icon=ft.Icons.CHECK_CIRCLE,
                color="white",
                bgcolor="green",
                on_click=lambda e, tid=t.id, cat=t.category, amt=t.amount, ttype=t.transaction_type:
                    on_confirm(tid, cat, amt, ttype),
            )
        else:
            state_button = ft.ElevatedButton(
                "Revert",
                icon=ft.Icons.UNDO,
                color="white",
                bgcolor="orange",
                on_click=lambda e, tid=t.id: on_revert(tid),
            )

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
                status_badge,
                state_button,
                ft.IconButton(
                    icon=ft.Icons.EDIT, icon_color="blue", tooltip="Edit",
                    on_click=lambda e, tid=t.id: load_for_edit(tid),
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE, icon_color="red", tooltip="Delete",
                    on_click=lambda e, tid=t.id: on_delete(tid),
                ),
            ], spacing=8),
            padding=10,
            bgcolor="#fffde7" if is_pending else "white",
            border=ft.border.all(1, "#ffe082" if is_pending else "#e8e8e8"),
            border_radius=8,
        )

    def render_list():
        list_column.controls.clear()

        results = search_transactions(
            query=search_field.value or "",
            category=category_filter.value,
            transaction_type=type_filter.value,
        )

        if status_filter.value != "All":
            results = [t for t in results if t.status == status_filter.value]

        if results:
            result_count.value = f"📋 {len(results)} matching transaction{'s' if len(results) != 1 else ''}"
            for t in results:
                list_column.controls.append(transaction_row(t))
        else:
            result_count.value = "No matching transactions found."
            list_column.controls.append(
                ft.Container(
                    content=ft.Text("No matching transactions found.", color="grey", italic=True, size=14),
                    padding=20,
                )
            )

        total = len(get_transactions())
        status_text.value = f"Status: Showing {len(results)} of {total} transactions"
        page.update()

    # === Lab 11 — State transition: pending → confirmed ===
    def on_confirm(transaction_id, category, amount, transaction_type):
        if transaction_type == "expense":
            if not is_budget_available(category, amount):
                list_feedback.value = f"⚠️ Cannot confirm — this would exceed the '{category}' budget limit."
                list_feedback.color = "red"
                page.update()
                return

        confirm_transaction(transaction_id)
        list_feedback.value = "✅ Transaction confirmed successfully."
        list_feedback.color = "green"
        render_list()

    # === Lab 11 — State transition: confirmed → pending ===
    def on_revert(transaction_id):
        revert_transaction(transaction_id)
        list_feedback.value = "↩️ Transaction reverted to pending."
        list_feedback.color = "orange"
        render_list()

    def load_for_edit(transaction_id):
        matches = [t for t in get_transactions() if t.id == transaction_id]
        if not matches:
            return
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
        list_feedback.value = f"🗑️ '{name}' deleted."
        list_feedback.color = "red"
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

        if editing_id["value"] is not None:
            existing = [x for x in get_transactions() if x.id == editing_id["value"]]
            preserved_status = existing[0].status if existing else "pending"
            t = Transaction(
                desc_field.value, amount, category_field.value,
                type_field.value, date_field.value,
                status=preserved_status,
            )
            update_transaction(editing_id["value"], t)
            form_feedback.value = f"✅ '{t.description}' updated!"
        else:
            t = Transaction(
                desc_field.value, amount, category_field.value,
                type_field.value, date_field.value,
                status="pending",
            )
            add_transaction(t)
            form_feedback.value = f"✅ '{t.description}' added as Pending. Press Confirm to approve."

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
        status_filter.value   = "All"
        list_feedback.value   = ""
        render_list()

    form_button.on_click      = on_submit
    cancel_button.on_click    = on_cancel
    search_field.on_change    = lambda e: render_list()
    category_filter.on_change = lambda e: render_list()
    type_filter.on_change     = lambda e: render_list()
    status_filter.on_change   = lambda e: render_list()

    render_list()

    return ft.Column([
        ft.Text("Transactions", size=24, weight=ft.FontWeight.BOLD, color="blue"),
        ft.Text("Create, search, edit and confirm transactions", size=13, color="grey", italic=True),
        ft.Divider(height=15),

        # Section 1 — Form
        section_primary(
            "Transaction Form",
            ft.Column([
                ft.Row([desc_field, amount_field, category_field, type_field, date_field], wrap=True, spacing=10),
                ft.Row([form_button, cancel_button], spacing=10),
                form_feedback,
            ]),
            subtitle="New transactions start as Pending. Confirming an expense checks it against the category budget. Use Revert to move back to pending.",
        ),

        # Section 2 — Search & Filter
        section(
            "Search & Filter",
            ft.Column([
                ft.Row([
                    search_field, category_filter, type_filter, status_filter,
                    ft.ElevatedButton("Reset", icon=ft.Icons.CLEAR, on_click=on_reset_filters),
                ], wrap=True, spacing=10),
                result_count,
            ]),
            subtitle="Filter by description, category, type or status",
        ),

        # Section 3 — Transactions List
        ft.Container(
            content=ft.Column([
                ft.Text("Transactions List", size=18, weight=ft.FontWeight.BOLD, color="green"),
                ft.Text("🟡 Yellow = Pending   ⬜ White = Confirmed", size=11, color="grey", italic=True),
                ft.Divider(height=10, color="green"),
                list_feedback,
                list_column,
            ]),
            padding=15, margin=ft.margin.only(bottom=15),
            bgcolor="white", border=ft.border.all(1, "green"), border_radius=10,
        ),

        # Section 4 — Status
        status_container,

    ], spacing=0, scroll=ft.ScrollMode.ADAPTIVE)