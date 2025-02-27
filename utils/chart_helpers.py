import plotly.graph_objects as go
import plotly.express as px

def create_price_history_chart(df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['price'],
            mode='lines',
            name='Price',
            line=dict(color='#FF4B4B', width=2)
        )
    )
    
    fig.update_layout(
        title="Price History",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        template="plotly_white",
        hovermode="x unified",
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig

def create_market_trend_chart(df):
    fig = px.bar(
        df.groupby('condition').agg({'price': 'mean'}).reset_index(),
        x='condition',
        y='price',
        color_discrete_sequence=['#FF4B4B']
    )
    
    fig.update_layout(
        title="Average Price by Condition",
        xaxis_title="Condition",
        yaxis_title="Average Price ($)",
        template="plotly_white",
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig
