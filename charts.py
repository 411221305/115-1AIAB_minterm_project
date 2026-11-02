"""
charts.py - Plotly 視覺化圖表模組
負責生成各種互動式統計圖表：分類圓餅圖、收支每日趨勢圖、預算進度條圖與資產分佈圖。
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict, Any


def make_category_pie_chart(df: pd.DataFrame, title: str = "支出分類分佈") -> go.Figure:
    """繪製分類圓餅/環形圖 (Donut Chart)"""
    if df.empty or df["total_amount"].sum() == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="本月份尚無任何支出紀錄 🍃",
            showarrow=False,
            font=dict(size=16, color="#888888"),
        )
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        return fig

    # 組合 Emoji 圖示與名稱
    labels = df["category_icon"] + " " + df["category_name"]
    fig = px.pie(
        df,
        values="total_amount",
        names=labels,
        title=title,
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>金額: NT$ %{value:,.0f}<br>佔比: %{percent}",
    )
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        height=380,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def make_daily_trend_chart(df: pd.DataFrame) -> go.Figure:
    """繪製每日收支對比長條/折線趨勢圖"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="本月份尚無任何每日收支資料 📈",
            showarrow=False,
            font=dict(size=16, color="#888888"),
        )
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        return fig

    fig = go.Figure()
    # 收入柱狀圖
    fig.add_trace(
        go.Bar(
            x=df["record_date"],
            y=df["income"],
            name="收入 (Income)",
            marker_color="#2ecc71",
            hovertemplate="日期: %{x}<br>收入: NT$ %{y:,.0f}<extra></extra>",
        )
    )
    # 支出柱狀圖
    fig.add_trace(
        go.Bar(
            x=df["record_date"],
            y=df["expense"],
            name="支出 (Expense)",
            marker_color="#e74c3c",
            hovertemplate="日期: %{x}<br>支出: NT$ %{y:,.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        title="本月份每日收支趨勢",
        barmode="group",
        xaxis_title="日期",
        yaxis_title="金額 (NT$)",
        height=380,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
    )
    return fig


def make_budget_progress_chart(budget_statuses: List[Dict[str, Any]]) -> go.Figure:
    """繪製分類預算消耗對比條形圖 (附警示顏色區分)"""
    if not budget_statuses:
        fig = go.Figure()
        fig.add_annotation(
            text="尚未設定任何分類預算 🎯",
            showarrow=False,
            font=dict(size=16, color="#888888"),
        )
        fig.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20))
        return fig

    names = [f"{b['category_icon']} {b['category_name']}" for b in budget_statuses]
    limits = [b["monthly_limit"] for b in budget_statuses]
    spents = [b["spent"] for b in budget_statuses]
    colors = [
        "#e74c3c" if b["status"] == "danger" else ("#f39c12" if b["status"] == "warning" else "#27ae60")
        for b in budget_statuses
    ]

    fig = go.Figure()
    # 預算上限背景
    fig.add_trace(
        go.Bar(
            y=names,
            x=limits,
            name="預算上限",
            orientation="h",
            marker=dict(color="#ecf0f1", line=dict(color="#bdc3c7", width=1)),
            hoverinfo="none",
        )
    )
    # 實際已花費
    fig.add_trace(
        go.Bar(
            y=names,
            x=spents,
            name="實際支出",
            orientation="h",
            marker=dict(color=colors),
            hovertemplate="已花費: NT$ %{x:,.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        title="預算執行與超支警示進度",
        barmode="overlay",
        xaxis_title="金額 (NT$)",
        height=max(280, len(names) * 45),
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=False,
    )
    return fig


def make_account_balance_chart(account_balances: List[Dict[str, Any]]) -> go.Figure:
    """繪製各帳戶即時餘額長條圖"""
    if not account_balances:
        fig = go.Figure()
        return fig

    names = [a["name"] for a in account_balances]
    balances = [a["current_balance"] for a in account_balances]
    colors = ["#3498db" if b >= 0 else "#e74c3c" for b in balances]

    fig = go.Figure(
        go.Bar(
            x=names,
            y=balances,
            marker_color=colors,
            text=[f"NT$ {b:,.0f}" for b in balances],
            textposition="auto",
        )
    )
    fig.update_layout(
        title="各帳戶當前資產餘額",
        yaxis_title="當前餘額 (NT$)",
        height=320,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig
