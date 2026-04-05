import flet as ft
from ui.components import section, build_status_section
from data.repository import get_total_income, get_total_expenses, get_net_balance, get_transactions

def build_dashboard_view(page: ft.Page):

    def summary_card(label, value, icon, color, bg):
        return ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(icon, color=color, size=28), ft.Text(label, size=13, color="grey")], spacing=8),
                ft.Text(value, size=22, weight=ft.FontWeight.BOLD, color=color),
            ], spacing=6),
            padding=20,
            bgcolor=bg,
            border=ft.border.all(1, color),
            border_radius=12,
            width=200,
        )

    total_income   = get_total_income()
    total_expenses = get_total_expenses()
    net_balance    = get_net_balance()
    all_transactions = get_transactions()

    cards = ft.Row([
        summary_card("Total Income",   f"${total_income:.2f}",   ft.Icons.TRENDING_UP,     "green",  "#e8f5e9"),
        summary_card("Total Expenses", f"${total_expenses:.2f}", ft.Icons.TRENDING_DOWN,   "red",    "#ffebee"),
        summary_card("Net Balance",    f"${net_balance:.2f}",    ft.Icons.ACCOUNT_BALANCE, "blue",   "#e3f2fd"),
        summary_card("Transactions",   str(len(all_transactions)),ft.Icons.RECEIPT_LONG,   "purple", "#f3e5f5"),
    ], wrap=True, spacing=15)

    # Recent transactions (last 5)
    recent_rows = ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Text("📈" if t.transaction_type == "income" else "📉", size=16),
                ft.Text(t.description, size=14, expand=True),
                ft.Text(t.date, size=12, color="grey", width=90),
                ft.Text(
                    f"${t.amount:.2f}",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color="green" if t.transaction_type == "income" else "red",
                    width=90,
                ),
            ], spacing=10),
            padding=ft.padding.symmetric(vertical=8, horizontal=12),
            border=ft.border.only(bottom=ft.BorderSide(1, "#eeeeee")),
        )
        for t in reversed(all_transactions[-5:])
    ])

    status_container, _ = build_status_section("Dashboard loaded")

    return ft.Column([
        ft.Text("Dashboard", size=24, weight=ft.FontWeight.BOLD, color="blue"),
        ft.Text("Your financial overview", size=13, color="grey", italic=True),
        ft.Divider(height=15),
        section("Summary", cards, subtitle="Current period totals"),
        section("Recent Transactions", recent_rows, subtitle="Last 5 entries"),
        status_container,
    ], spacing=10, scroll=ft.ScrollMode.ADAPTIVE)