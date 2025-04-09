import pandas as pd
import mysql.connector
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
from plotly.subplots import make_subplots
from ipywidgets import interact, widgets
from datetime import datetime
import os

pio.renderers.default = "browser"

def get_data_from_mysql():
    conn = mysql.connector.connect(
        host="localhost",
        user="test",
        password="test",
        database="itunes_db"
    )
    query = "SELECT * FROM subscriptions"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    df = pd.DataFrame(rows)
    return df

df = get_data_from_mysql()
df['event_date'] = pd.to_datetime(df['event_date'])

def analyze_data(start_date, end_date, subscription_name, app_id=None, subscriber_id=None, query_type=None, specific_date=None):
    filtered = df.copy()

    if start_date:
        filtered = filtered[filtered['event_date'] >= pd.to_datetime(start_date)]
    if end_date:
        filtered = filtered[filtered['event_date'] <= pd.to_datetime(end_date)]
    if subscription_name:
        filtered = filtered[filtered['subscription_name'] == subscription_name]

    if query_type == "subscription_duration" and subscriber_id:
        subscriber_data = filtered[filtered['subscriber_id'] == subscriber_id]
        if not subscriber_data.empty:
            first_date = subscriber_data['event_date'].min()
            last_date = subscriber_data['event_date'].max()
            duration = (last_date - first_date).days
            print(f"Subscription duration for subscriber {subscriber_id}: {duration} days")

    elif query_type == "subscriptions_for_app" and app_id:
        app_subscriptions = filtered[filtered['app_id'] == app_id]
        print(f"Subscriptions for app {app_id}:")
        print(app_subscriptions[['subscriber_id', 'subscription_name', 'event_date']])

    elif query_type == "highest_revenue_app":
        app_revenue = filtered.groupby('app_id')['usd_price'].sum()
        highest_revenue_app = app_revenue.idxmax()
        print(f"The app with the highest revenue in the given period is {highest_revenue_app}.")

    elif query_type == "conversion_rate_by_date" and specific_date:
        specific_date_data = filtered[filtered['event_date'] == pd.to_datetime(specific_date)]
        trial_users = specific_date_data[specific_date_data['is_trial'] == 1]['subscriber_id'].nunique()
        converted_users = specific_date_data[specific_date_data['is_converted_from_trial'] == 1]['subscriber_id'].nunique()
        conversion_rate = round((converted_users / trial_users) * 100, 2) if trial_users > 0 else 0
        print(f"Conversion rate from trial to paid subscription on {specific_date}: {conversion_rate}%")

    trial_users = filtered[filtered['is_trial'] == 1]['subscriber_id'].nunique()
    converted = filtered[filtered['is_converted_from_trial'] == 1]['subscriber_id'].nunique()
    paying_users = filtered[(filtered['is_trial'] == 0) & (filtered['usd_price'] > 0)]['subscriber_id'].nunique()

    conversion_rate = round((converted / trial_users) * 100, 2) if trial_users > 0 else 0
    share_of_converted = round((converted / paying_users) * 100, 2) if paying_users > 0 else 0

    print(f"Trial users: {trial_users}")
    print(f"Converted to paid: {converted}")
    print(f"Trial-to-paid conversion rate: {conversion_rate}%")
    print(f"Share of conversions among all payments: {share_of_converted}%")

    fig = make_subplots(
        rows=2, cols=3,
        specs=[[{"type": "domain"}, {"type": "bar"}, {"type": "scatter"}],
               [{"type": "bar"}, {"type": "bar"}, None]],
        subplot_titles=[
            "Converted vs Other Payers",
            "Top 10 countries by trial conversions",
            "Monthly subscriptions",
            "Conversions by subscription",
            "Top countries by users"
        ]
    )

    # 1. Pie chart
    labels = ['Converted from trial', 'Other paying users']
    values = [converted, max(paying_users - converted, 0)]
    fig.add_trace(go.Pie(labels=labels, values=values), row=1, col=1)

    # 2. Bar: Countries by conversion
    df_converted = filtered[filtered['is_converted_from_trial'] == 1]
    country_counts = df_converted['country'].value_counts().head(10)
    fig.add_trace(go.Bar(x=country_counts.index, y=country_counts.values), row=1, col=2)

    # 3. Line: Monthly subscriptions
    daily_subscriptions = filtered.groupby('event_date').size()
    fig.add_trace(
        go.Scatter(
            x=daily_subscriptions.index,
            y=daily_subscriptions.values,
            mode='lines+markers',
            name='Daily Subscriptions'
        ),
        row=1, col=3
    )

    # 4. Bar: Conversions by subscription
    subscription_conversion = filtered.groupby('subscription_name')['is_converted_from_trial'].sum()
    fig.add_trace(go.Bar(x=subscription_conversion.index, y=subscription_conversion.values), row=2, col=1)

    # 5. Bar: Countries by total users
    country_user_counts = filtered['country'].value_counts().head(10)
    fig.add_trace(go.Bar(x=country_user_counts.index, y=country_user_counts.values), row=2, col=2)

    fig.update_layout(
        height=1000,
        title_text="Subscription Insights Overview",
        title_x=0.5
    )

    fig.show()

    export_name = "filtered_conversions.csv"
    filtered.to_csv(export_name, index=False)
    print(f"Filtered data saved to {os.path.abspath(export_name)}")

unique_subscriptions = [None] + sorted(df['subscription_name'].dropna().unique().tolist())
interact(
    analyze_data,
    start_date=widgets.Text(value='', placeholder='YYYY-MM-DD', description='Start date:'),
    end_date=widgets.Text(value='', placeholder='YYYY-MM-DD', description='End date:'),
    subscription_name=widgets.Dropdown(options=unique_subscriptions, description='Subscription:'),
    app_id=widgets.IntText(value=None, description="App ID:", step=1),
    subscriber_id=widgets.IntText(value=None, description="Subscriber ID:", step=1),
    query_type=widgets.Dropdown(options=['', 'subscription_duration', 'subscriptions_for_app', 'highest_revenue_app', 'conversion_rate_by_date'], description="Query Type:"),
    specific_date=widgets.Text(value='', placeholder='YYYY-MM-DD', description="Date:")
)
