import flet as ft

# === SECTION COMPONENT ===
def section(title_text, content, subtitle=None):
    title_content = [ft.Text(title_text, size=18, weight=ft.FontWeight.BOLD)]
    if subtitle:
        title_content.append(ft.Text(subtitle, size=12, color="grey", italic=True))
    return ft.Container(
        content=ft.Column([ft.Column(title_content, spacing=0), ft.Divider(height=10), content]),
        padding=15,
        margin=ft.margin.only(bottom=15),
        bgcolor="white",
        border=ft.border.all(1, "#dddddd"),
        border_radius=10,
    )

# === PRIMARY SECTION VARIANT ===
def section_primary(title_text, content, subtitle=None):
    title_content = [ft.Text(title_text, size=18, weight=ft.FontWeight.BOLD, color="blue")]
    if subtitle:
        title_content.append(ft.Text(subtitle, size=12, color="lightblue", italic=True))
    return ft.Container(
        content=ft.Column([ft.Column(title_content, spacing=0), ft.Divider(height=10, color="blue"), content]),
        padding=15,
        margin=ft.margin.only(bottom=15),
        bgcolor="white",
        border=ft.border.all(1, "blue"),
        border_radius=10,
    )

# === SECONDARY SECTION VARIANT ===
def section_secondary(title_text, content, subtitle=None):
    title_content = [ft.Text(title_text, size=18, weight=ft.FontWeight.BOLD, color="green")]
    if subtitle:
        title_content.append(ft.Text(subtitle, size=12, color="lightgreen", italic=True))
    return ft.Container(
        content=ft.Column([ft.Column(title_content, spacing=0), ft.Divider(height=10, color="green"), content]),
        padding=15,
        margin=ft.margin.only(bottom=15),
        bgcolor="white",
        border=ft.border.all(1, "green"),
        border_radius=10,
    )

# === RESULT CARD COMPONENT ===
def result_card(transaction, icon=None):
    if transaction["type"] == "income":
        bg_color, border_color, text_color = "lightgreen", "green", "green"
    else:
        bg_color, border_color, text_color = "#ffcdd2", "red", "red"
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("📈" if transaction["type"] == "income" else "📉", size=20),
                ft.Text(transaction["description"], weight=ft.FontWeight.BOLD, size=16),
            ]),
            ft.Text(f"Amount: ${transaction['amount']:.2f}", color=text_color, size=14, weight=ft.FontWeight.BOLD),
            ft.Text(f"Category: {transaction['category']}", size=14),
            ft.Text(f"Type: {transaction['type'].title()}", color="grey", size=12, italic=True),
        ], spacing=5),
        padding=15,
        bgcolor=bg_color,
        border=ft.border.all(2, border_color),
        border_radius=10,
        margin=ft.margin.only(bottom=10),
        width=320,
    )

# === HEADER COMPONENT ===
def build_header():
    return ft.Container(
        content=ft.Column([
            ft.Text("Finance Tracker", size=28, weight=ft.FontWeight.BOLD, color="blue"),
            ft.Text("Track your income and expenses", size=14, color="grey"),
        ]),
        margin=ft.margin.only(bottom=20),
    )

# === STATUS COMPONENT ===
def build_status_section(status_text="Ready"):
    status_value = ft.Text(f"Status: {status_text}", size=14, color="blue")
    status_container = ft.Container(
        content=ft.Row([status_value]),
        padding=10,
        bgcolor="white",
        border=ft.border.all(1, "#dddddd"),
        border_radius=5,
    )
    return status_container, status_value