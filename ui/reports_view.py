import flet as ft
from ui.components import section, build_status_section
from data.repository import get_total_expenses, get_transactions

def build_reports_view(page: ft.Page):

    status_container, status_text = build_status_section("Reports view loaded")

    # === PERIOD SELECTOR ===
    period_dd = ft.Dropdown(
        label="Time Period",
        width=200,
        options=[
            ft.dropdown.Option("weekly",  "Weekly"),
            ft.dropdown.Option("monthly", "Monthly"),
            ft.dropdown.Option("yearly",  "Yearly"),
        ],
        value="monthly",
    )

    chart_column     = ft.Column(spacing=10)
    breakdown_column = ft.Column(spacing=0)

    # === HELPERS ===
    def get_period_label(date_str, period):
        try:
            from datetime import datetime, timedelta
            d = datetime.strptime(date_str, "%Y-%m-%d")
            if period == "weekly":
                monday = d - timedelta(days=d.weekday())
                return f"W {monday.strftime('%d %b')}"
            elif period == "monthly":
                return d.strftime("%b %Y")
            else:
                return d.strftime("%Y")
        except:
            return "Unknown"

    def group_by_period(transactions, period, t_type="expense"):
        groups = {}
        for t in transactions:
            if t.transaction_type != t_type or t.status != "confirmed":
                continue
            label = get_period_label(t.date, period)
            groups[label] = groups.get(label, 0) + t.amount
        return groups

    def group_by_category(transactions):
        groups = {}
        for t in transactions:
            if t.transaction_type != "expense" or t.status != "confirmed":
                continue
            groups[t.category] = groups.get(t.category, 0) + t.amount
        return groups

    HEX_COLORS = ["#1565C0","#C62828","#2E7D32","#E65100","#6A1B9A","#00695C","#AD1457","#4E342E"]

    def build_histogram(grouped_data, title, subtitle):
        if not grouped_data:
            return ft.Container(
                content=ft.Text("No confirmed data for this period.", color="grey", italic=True, size=14),
                padding=20,
            )

        max_val = max(grouped_data.values())
        max_bar_width = 380
        bars = []

        for i, (label, amount) in enumerate(sorted(grouped_data.items())):
            bar_width = max(8, int((amount / max_val) * max_bar_width))
            color = HEX_COLORS[i % len(HEX_COLORS)]
            bars.append(
                ft.Row([
                    ft.Container(
                        content=ft.Text(label, size=12, color="grey"),
                        width=100,
                    ),
                    ft.Container(
                        width=bar_width,
                        height=26,
                        bgcolor=color,
                        border_radius=4,
                    ),
                    ft.Text(f"  ${amount:.2f}", size=12, weight=ft.FontWeight.BOLD, color=color),
                ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER)
            )

        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color="blue"),
                ft.Text(subtitle, size=11, color="grey", italic=True),
                ft.Divider(height=10),
                ft.Column(bars, spacing=8),
            ]),
            padding=15,
            bgcolor="white",
            border=ft.border.all(1, "#dddddd"),
            border_radius=10,
            margin=ft.margin.only(bottom=15),
        )

    def build_category_breakdown(category_data, total):
        breakdown_column.controls.clear()

        if not category_data:
            breakdown_column.controls.append(
                ft.Text("No confirmed expense data.", color="grey", italic=True, size=14)
            )
            return

        for i, (cat, amt) in enumerate(sorted(category_data.items(), key=lambda x: -x[1])):
            pct = amt / total * 100 if total > 0 else 0
            color = HEX_COLORS[i % len(HEX_COLORS)]
            breakdown_column.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Container(width=12, height=12, bgcolor=color, border_radius=3),
                        ft.Text(cat, size=14, expand=True),
                        ft.Text(f"${amt:.2f}", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(f"({pct:.1f}%)", size=12, color="grey", width=60),
                    ], spacing=10),
                    padding=ft.padding.symmetric(vertical=8, horizontal=12),
                    border=ft.border.only(bottom=ft.BorderSide(1, "#eeeeee")),
                )
            )

        breakdown_column.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Text("Total Expenses", size=14, weight=ft.FontWeight.BOLD, expand=True),
                    ft.Text(f"${total:.2f}", size=14, weight=ft.FontWeight.BOLD, color="red"),
                ], spacing=10),
                padding=ft.padding.symmetric(vertical=10, horizontal=12),
                bgcolor="#fff8f8", border_radius=6, margin=ft.margin.only(top=8),
            )
        )

    def render_reports(e=None):
        chart_column.controls.clear()

        all_transactions = get_transactions()
        selected = period_dd.value or "monthly"
        label    = selected.title()

        # Expense histogram
        expense_groups = group_by_period(all_transactions, selected, "expense")
        chart_column.controls.append(
            build_histogram(expense_groups, f"Expenses by {label}", f"Confirmed expenses grouped by {selected} period")
        )

        # Income histogram
        income_groups = group_by_period(all_transactions, selected, "income")
        chart_column.controls.append(
            build_histogram(income_groups, f"Income by {label}", f"Confirmed income grouped by {selected} period")
        )

        # Category breakdown
        category_data = group_by_category(all_transactions)
        total = get_total_expenses()
        build_category_breakdown(category_data, total)

        status_text.value = f"Status: Reports updated — {label} view"
        page.update()

    period_dd.on_change = render_reports
    render_reports()

    return ft.Column([
        ft.Text("Reports", size=24, weight=ft.FontWeight.BOLD, color="blue"),
        ft.Text("Analyse your spending and income patterns", size=13, color="grey", italic=True),
        ft.Divider(height=15),

        # Period selector
        ft.Container(
            content=ft.Column([
                ft.Text("Time Period", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Switch between weekly, monthly and yearly views", size=12, color="grey", italic=True),
                ft.Divider(height=10),
                ft.Row([period_dd]),
            ]),
            padding=15, margin=ft.margin.only(bottom=15),
            bgcolor="white", border=ft.border.all(1, "#dddddd"), border_radius=10,
        ),

        # Histograms
        section(
            "Spending & Income Charts",
            chart_column,
            subtitle="Bar length represents amount relative to the largest value in that period",
        ),

        # Category breakdown
        ft.Container(
            content=ft.Column([
                ft.Text("Expense Breakdown by Category", size=18, weight=ft.FontWeight.BOLD, color="green"),
                ft.Text("All confirmed expenses", size=12, color="lightgreen", italic=True),
                ft.Divider(height=10, color="green"),
                breakdown_column,
            ]),
            padding=15, margin=ft.margin.only(bottom=15),
            bgcolor="white", border=ft.border.all(1, "green"), border_radius=10,
        ),

        status_container,
    ], spacing=0, scroll=ft.ScrollMode.ADAPTIVE)