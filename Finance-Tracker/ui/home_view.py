import flet as ft
from ui.dashboard_view import build_dashboard_view
from ui.transactions_view import build_transactions_view
from ui.budget_view import build_budget_view
from ui.reports_view import build_reports_view

def build_home_view(page: ft.Page):
    content_area = ft.Container(expand=True, padding=20)

    views = [
        build_dashboard_view(page),
        build_transactions_view(page),
        build_budget_view(page),
        build_reports_view(page),
    ]

    nav_labels = ["Dashboard", "Transactions", "Budget", "Reports"]
    active_label = ft.Text("📍 Dashboard", size=13, color="grey", italic=True)

    def change_view(e):
        idx = e.control.selected_index
        content_area.content = views[idx]
        active_label.value = f"📍 {nav_labels[idx]}"
        page.update()

    navigation = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        bgcolor="white",
        indicator_color="#e3f2fd",
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD, label="Dashboard"),
            ft.NavigationRailDestination(icon=ft.Icons.RECEIPT_LONG_OUTLINED, selected_icon=ft.Icons.RECEIPT_LONG, label="Transactions"),
            ft.NavigationRailDestination(icon=ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, selected_icon=ft.Icons.ACCOUNT_BALANCE_WALLET, label="Budget"),
            ft.NavigationRailDestination(icon=ft.Icons.BAR_CHART_OUTLINED, selected_icon=ft.Icons.BAR_CHART, label="Reports"),
        ],
        on_change=change_view,
    )

    content_area.content = views[0]

    return ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Text("💰 Finance Tracker", size=20, weight=ft.FontWeight.BOLD, color="blue"),
                ft.VerticalDivider(width=20, color="transparent"),
                active_label,
            ]),
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            bgcolor="white",
            border=ft.border.only(bottom=ft.BorderSide(1, "#dddddd")),
        ),
        ft.Row([
            navigation,
            ft.VerticalDivider(width=1),
            content_area,
        ], expand=True),
    ], spacing=0, expand=True)