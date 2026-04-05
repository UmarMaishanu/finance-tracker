import flet as ft
from ui.components import section, build_status_section
from data.repository import get_expenses, get_total_expenses

def build_reports_view(page: ft.Page):

    expenses = get_expenses()
    total    = get_total_expenses()

    # Group by category
    category_totals = {}
    for t in expenses:
        category_totals[t.category] = category_totals.get(t.category, 0) + t.amount

    colors = ["green", "orange", "purple", "red", "blue", "teal", "pink"]

    def report_row(label, amount, color):
        pct = amount / total * 100 if total > 0 else 0
        return ft.Container(
            content=ft.Row([
                ft.Container(width=12, height=12, bgcolor=color, border_radius=3),
                ft.Text(label, size=14, expand=True),
                ft.Text(f"${amount:.2f}", size=14, weight=ft.FontWeight.BOLD),
                ft.Text(f"({pct:.1f}%)", size=12, color="grey", width=60),
            ], spacing=10),
            padding=ft.padding.symmetric(vertical=8, horizontal=12),
            border=ft.border.only(bottom=ft.BorderSide(1, "#eeeeee")),
        )

    rows = [
        report_row(cat, amt, colors[i % len(colors)])
        for i, (cat, amt) in enumerate(sorted(category_totals.items(), key=lambda x: -x[1]))
    ]

    rows.append(
        ft.Container(
            content=ft.Row([
                ft.Text("Total Expenses", size=14, weight=ft.FontWeight.BOLD, expand=True),
                ft.Text(f"${total:.2f}", size=14, weight=ft.FontWeight.BOLD, color="red"),
            ], spacing=10),
            padding=ft.padding.symmetric(vertical=10, horizontal=12),
            bgcolor="#fff8f8", border_radius=6, margin=ft.margin.only(top=8),
        )
    )

    status_container, _ = build_status_section("Reports view loaded")

    return ft.Column([
        ft.Text("Reports", size=24, weight=ft.FontWeight.BOLD, color="blue"),
        ft.Text("Analyse your spending patterns", size=13, color="grey", italic=True),
        ft.Divider(height=15),
        section("Expense Breakdown", ft.Column(rows), subtitle="All categories this period"),
        status_container,
    ], spacing=10, scroll=ft.ScrollMode.ADAPTIVE)
