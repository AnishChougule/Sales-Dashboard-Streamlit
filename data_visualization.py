import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def product_quantity(df):
    best_product = df.groupby('Product')
    quantity_sold = best_product['Quantity Ordered'].sum()
    product_data = quantity_sold.reset_index()
    product_data = product_data.sort_values('Quantity Ordered', ascending=True).rename(columns={'Quantity Ordered': 'Quantity Sold'})

    fig = px.bar(
        product_data,
        x='Product',
        y='Quantity Sold',
        orientation='v',
        title='Total Quantity Sold for Each Product',
        color='Quantity Sold',
        color_continuous_scale='darkmint',
        labels={'Quantity Sold': 'Quantity', 'Product': 'Product'}
    )

    fig.update_layout(
        title_font_size=20,
        xaxis_title="Product",
        yaxis_title="Quantity",
        xaxis_tickfont_size=12,
        yaxis_tickfont_size=12,
        font_family="Arial Black",
        margin=dict(t=150, l=150, r=150, b=150),
        bargap=0.2,
        height=800
    )

    return fig

def product_sales(df):
    best_product = df.groupby('Product')
    sales = best_product['Sales'].sum()
    product_data = sales.reset_index()
    product_data = product_data.sort_values('Sales', ascending=True)


    fig = px.bar(product_data,
        x='Product',
        y='Sales',  
        orientation='v', 
        title='Total Sales for Each Product',
        color='Sales', 
        color_continuous_scale='darkmint',
        labels={'Sales': 'Sales', 'Product': 'Product'})


    fig.update_layout(
        title_font_size=20,
        font_family="Arial Black",
        xaxis_title="Product",
        yaxis_title="Sales",
        xaxis_tickfont_size=12,
        yaxis_tickfont_size=12,
        margin=dict(t=150, l=150, r=150, b=150),
        bargap=0.2,
        height=800
    )
    return fig



def orders_by_hour(df):
    hourly_orders = df.groupby(['Weekday', 'Hour']).size().reset_index(name='Order Count')

    fig = go.Figure()

    days = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}

    for day in range(0, 7):
        day_data = hourly_orders[hourly_orders['Weekday'] == day]
        fig.add_trace(go.Scatter(
            x=day_data['Hour'],
            y=day_data['Order Count'],
            mode='lines+markers',
            line=dict(width=3),
            marker=dict(color='cadetblue',size=8),
            name=days[day],
            visible=(day == 0)  
        ))


    buttons = []
    for day in days:
        button = dict(
            method="update",
            label=days[day],
            args=[{"visible": [i == day for i in range(7)]},
                {"title": f"Orders by Hour for {days[day]}"}]
        )
        buttons.append(button)


    fig.update_layout(
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            x=0.4,
            xanchor="left",
            y=1.1,
            yanchor="top",
            direction="down",
        )],
        title="Orders by Hour",
        title_font=dict(size=20),
        xaxis=dict(title="Hour of the Day", tickmode='linear', dtick=1, range=[0, 23]),
        yaxis=dict(title="Orders"),
        font=dict(size=12),
        font_family="Arial Black",
        margin=dict(t=150, l=150, r=150, b=150),
        hovermode="x",
        height=800
    )
    return fig

def sales_by_city(df):
    city_sales = df.groupby('City State')['Sales'].sum()
    city_data = city_sales.reset_index()
    total_sales = city_data['Sales'].sum()
    city_data['Percentage Contribution'] = (city_data['Sales'] / total_sales) * 100

    hover_template = (
        "<b>%{label}</b><br>"
        "Sales: $%{value:,.2f}<br>"
        "Percentage Contribution: %{customdata[0]:.2f}%<br>"
    )


    fig = px.treemap(
        city_data,
        path=["City State"],
        values="Sales",
        color="Sales",
        color_continuous_scale="darkmint",
        title="Sales by City",
    )


    fig.data[0].customdata = city_data[["Percentage Contribution"]].values

    fig.update_traces(
        hovertemplate=hover_template,
        hoverinfo="skip",
        marker=dict(cornerradius=5),
    )


    fig.update_layout(
        margin=dict(t=150, l=150, r=150, b=150),
        title_font=dict(size=20),
        font_family="Arial Black", 
        height=800
    )
    return fig


def sales_orders_by_month(df):
    monthly_data = df.groupby('Month').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Orders=('Order ID', 'count')).reset_index()


    fig = px.line(
        monthly_data,
        x="Month",
        y=["Total_Sales", "Total_Orders"],
        labels={
            "Month": "Month",
            "value": "Sales",
            "variable": "Metric"
        },
        title="Sales and Orders Over the Months",
        markers=True
    )


    fig.for_each_trace(lambda trace: trace.update(
        line=dict(
            color="cadetblue",
            dash="solid" if trace.name == "Total_Sales" else "dot"
        )
    ))


    fig.update_layout(
        title_font=dict(size=20),
        font_family="Arial Black",
        xaxis_title="Month", 
        xaxis=dict(
            tickvals=list(range(1, 13)),
            ticktext=[
                'January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December'
            ]
        ),
        yaxis_title="Sales",
        legend_title="Metrics",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=150, l=150, r=150, b=150),
        height=800
    )
    return fig


def totalsales_totalorders(df):
    total_sales = df['Sales'].sum()
    total_orders = df['Order ID'].count()

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="number",
        value=total_sales,
        number={"prefix": "$", "valueformat": ",.0f"},
        title={"text": "<b>Total Sales</b><br>"},
        domain={"x": [0, 0.5], "y": [0, 1]},
    ))


    fig.add_trace(go.Indicator(
        mode="number",
        value=total_orders,
        number={"valueformat": ",d"},
        title={"text": "<b>Total Orders</b><br>"},
        domain={"x": [0.5, 1], "y": [0, 1]},
    ))


    fig.update_layout(
        title="<b>Key Business Metrics</b>",
        title_font=dict(size=20),
        font_family = "Ariel Black",
        margin=dict(t=100, l=100, r=100, b=100),
        height=800
    )
    return fig

def city_sales_by_month(df):
    city_month_sales = df.groupby(['City State', 'Month'])['Sales'].sum().reset_index()

    fig = px.line(
        city_month_sales,
        x='Month',
        y='Sales',
        color='City State',
        title='Sales Trend for Each City',
        labels={'Month': 'Month', 'Sales': 'Total Sales ($)', 'City State': 'City'},
        markers=True,
        color_discrete_sequence=px.colors.sequential.Darkmint
    )


    fig.update_layout(
        title_font=dict(size=20),
        font_family="Arial Black",
        xaxis_title="Month", 
        xaxis=dict(
            tickvals=list(range(1, 13)),
            ticktext=[
                'January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December'
            ]
        ),
        yaxis_title="Sales",
        legend_title="Metrics",
        margin=dict(t=150, l=150, r=150, b=150),
        height=800
    )
    return fig



def product_sales_by_month(df):
    product_month_sales = df.groupby(['Product', 'Month'])['Sales'].sum().reset_index()

    fig = px.line(
        product_month_sales,
        x='Month',
        y='Sales',
        color='Product',
        title='Sales Trend for Each Product',
        labels={'Month': 'Month', 'Sales': 'Total Sales ($)', 'Product': 'Product'},
        markers=True,
        color_discrete_sequence=px.colors.sequential.Darkmint
    )


    fig.update_layout(
        title_font=dict(size=20),
        font_family="Arial Black",
        xaxis_title="Month", 
        xaxis=dict(
            tickvals=list(range(1, 13)),
            ticktext=[
                'January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December'
            ]
        ),
        yaxis_title="Sales",
        legend_title="Metrics",
        margin=dict(t=150, l=150, r=150, b=150),
        height=800
    )
    return fig


def product_quantity_by_month(df):
    product_month_quantity = df.groupby(['Product', 'Month'])['Quantity Ordered'].sum().reset_index()

    fig = px.line(
        product_month_quantity,
        x='Month',
        y='Quantity Ordered',
        color='Product',
        title='Quantity for Each Product by Month',
        labels={'Month': 'Month', 'Quantity Ordered': 'Quantity', 'Product': 'Product'},
        markers=True,
        color_discrete_sequence=px.colors.sequential.Darkmint
    )


    fig.update_layout(
        title_font=dict(size=20),
        font_family="Arial Black",
        xaxis_title="Month", 
        xaxis=dict(
            tickvals=list(range(1, 13)),
            ticktext=[
                'January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December'
            ]
        ),
        yaxis_title="Sales",
        legend_title="Metrics",
        margin=dict(t=150, l=150, r=150, b=150),
        height=800
    )
    return fig


@st.cache_data
def create_all_visuals(df):
    fig7 = product_quantity(df)
    fig4 = product_sales(df)
    fig2 = orders_by_hour(df)
    fig3 = sales_by_city(df)
    fig9 = sales_orders_by_month(df)
    fig1 = totalsales_totalorders(df)
    fig5 = city_sales_by_month(df)
    fig6 = product_sales_by_month(df)
    fig8 = product_quantity_by_month(df)

    return [fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9]