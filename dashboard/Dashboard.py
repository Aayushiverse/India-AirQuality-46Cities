#!/usr/bin/env python
# coding: utf-8

# In[1]:



# In[2]:


import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Load your final processed dataset (e.g., 'result.csv')
df = pd.read_csv('aqi_dashboard_small.csv')

# In[3]:


from dash import dash_table

# AQI category table
aqi_category_data = [
    {"Category": "Good", "AQI Range": "0–50", "Health Impact": "Air quality is satisfactory."},
    {"Category": "Moderate", "AQI Range": "51–100", "Health Impact": "Acceptable; minor concern for sensitive people."},
    {"Category": "Unhealthy for Sensitive Groups", "AQI Range": "101–150", "Health Impact": "May cause problems for vulnerable groups."},
    {"Category": "Unhealthy", "AQI Range": "151–200", "Health Impact": "Everyone may experience health effects."},
    {"Category": "Very Unhealthy", "AQI Range": "201–300", "Health Impact": "Health alert: serious effects for everyone."},
    {"Category": "Hazardous", "AQI Range": "301–500", "Health Impact": "Emergency conditions. Avoid outdoor exposure."}
]

# Pollutant descriptions
pollutant_descriptions = {
    "pm2_5": "Fine particles that penetrate lungs and enter bloodstream. Cause heart and respiratory issues.",
    "pm10": "Inhalable particles affecting lungs and throat. Can worsen asthma and bronchitis.",
    "ozone": "At ground level, ozone triggers asthma and reduces lung function.",
    "nitrogen_dioxide": "Irritates airways and increases susceptibility to infections.",
    "sulphur_dioxide": "Causes wheezing, shortness of breath and asthma symptoms.",
    "carbon_monoxide": "Reduces oxygen delivery to organs. Dangerous at high levels."
}


# In[4]:


df.drop(columns=['lat', 'lon'])


# In[5]:


import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Load & preprocess
df["datetime"] = pd.to_datetime(df["datetime"])
df["date"] = df["datetime"].dt.date

# Daily averages
df_daily = df.groupby(["city", "date"])[
    ["pm2_5", "pm10", "ozone", "nitrogen_dioxide", "sulphur_dioxide", "carbon_monoxide"]
].mean().reset_index()

app = dash.Dash(__name__)
app.title = "Breathe India: 46 Cities Air Dashboard"
# App layout
app.layout = html.Div(
    style={'backgroundColor': '#f4f7f9', 'padding': '20px', 'fontFamily': 'Arial, sans-serif'},
    children=[
    html.H1("🌆 Breathe India: 46 Cities Air Dashboard", style={'textAlign': 'center'}),

    html.H4("📅 Data Range: 25 April 2025 – 25 July 2025", style={'textAlign': 'center'}),

    html.Br(),

    html.Div([
        html.Label("Select City:"),
        dcc.Dropdown(
            id='city_selector',
            options=[{'label': city, 'value': city} for city in sorted(df['city'].unique())],
            value='Delhi',
            clearable=False
        )
    ], style={
            'width': '50%',
            'margin': 'auto',
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 5px rgba(0,0,0,0.05)'
        }),

     html.Div([
            dcc.Graph(id='time_series_plot')
        ], style={'backgroundColor': '#ffffff', 'padding': '20px', 'marginTop': '20px', 'borderRadius': '10px'}),


    html.Hr(),

    html.Div([
        html.H4("📍 Daily Average Pollutant Trend", style={'textAlign': 'center'}),
        html.Div([
            dcc.Dropdown(
                id='pollutant_dropdown',
                options=[{'label': p.upper(), 'value': p} for p in ["pm2_5", "pm10", "ozone", "nitrogen_dioxide", "sulphur_dioxide", "carbon_monoxide"]],
                value='pm2_5',
                clearable=False
            )
        ], style={'width': '40%', 'margin': 'auto'}),
        dcc.Graph(id='daily_pollutant_plot')
    ],style={'backgroundColor': '#eef6f9', 'padding': '20px', 'borderRadius': '10px'}),

    html.Hr(),

    html.Div([
        html.H4("🏙️ Average Pollutant Levels by City", style={'textAlign': 'center'}),
        dcc.Graph(id='avg_pollutant_bar', figure=px.bar(
            df.groupby("city")[["pm2_5", "pm10", "ozone", "nitrogen_dioxide", "sulphur_dioxide", "carbon_monoxide"]]
            .mean()
            .reset_index()
            .melt(id_vars="city", var_name="pollutant", value_name="level"),
            x="city", y="level", color="pollutant",
            template="plotly_white", title="Average Levels per City"
        ).update_layout(xaxis_tickangle=-45))
    ]),

    html.Hr(),

    html.Div([
        html.H4("🧭 AQI Category Box for Selected City", style={'textAlign': 'center'}),
        html.Div(id='aqi_category_box', style={'textAlign': 'center', 'fontSize': '24px'})
    ]),

    html.Hr(),

    html.Div([
    html.H4("🌤️ Daily Weather Trend", style={'textAlign': 'center'}),
    html.Div([
        dcc.Dropdown(
            id='weather_dropdown',
            options=[
                {'label': 'Temperature (°C)', 'value': 'temperature_2m'},
                {'label': 'Humidity (%)', 'value': 'humidity'},
                {'label': 'Wind Speed (m/s)', 'value': 'wind_speed'},
                {'label': 'Precipitation (mm)', 'value': 'precipitation'}
            ],
            value='temperature_2m',
            clearable=False
        )
    ], style={'width': '40%', 'margin': 'auto'}),
    dcc.Graph(id='weather_trend_plot')
],style={'backgroundColor': '#f6f9ee', 'padding': '20px', 'borderRadius': '10px'}),
    
    html.Div([
    html.H4("🧾 AQI Categories & Pollutant Info", style={'textAlign': 'center'}),

    html.Div([

        # Left: AQI Table
        html.Div([
            dash_table.DataTable(
                id='aqi_table',
                columns=[{"name": i, "id": i} for i in ["Category", "AQI Range", "Health Impact"]],
                data=aqi_category_data,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '5px'},
                style_header={'backgroundColor': '#f2f2f2', 'fontWeight': 'bold'}
            )
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        # Right: Pollutant Dropdown + City Info
        html.Div([
            html.Label("Select Pollutant:"),
            dcc.Dropdown(
                id='pollutant_selector',
                options=[{'label': p.upper(), 'value': p} for p in pollutant_descriptions.keys()],
                value='pm2_5'
            ),
            html.Br(),
            html.Div(id='pollutant_city_info', style={'whiteSpace': 'pre-line', 'fontSize': '16px'})
        ], style={'width': '48%', 'display': 'inline-block', 'paddingLeft': '2%'})

    ])
],  style={'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '10px'}),
 

    html.Hr(),

    html.Div([
        html.H4("🏆 Top 10 Most Polluted Cities (Max AQI)", style={'textAlign': 'center'}),
        dcc.Graph(
            id='top_polluted',
            figure=px.bar(
                df.groupby('city')['AQI'].max().nlargest(10).reset_index(),
                x='city', y='AQI', color='city',
                title="Top Polluted Cities by Max AQI",
                color_discrete_sequence=px.colors.qualitative.Set2,
                template='plotly_white'
            )
        )
    ], style={'backgroundColor': '#ffeef2', 'padding': '20px', 'borderRadius': '10px'}),


    html.Hr(),

    html.Div([
        html.H4("🌱 Top 10 Cleanest Cities (Lowest Average AQI)", style={'textAlign': 'center'}),
        dcc.Graph(
            id='cleanest_plot',
            figure=px.bar(
                df.groupby("city")["AQI"].mean().nsmallest(10).reset_index(),
                x="city", y="AQI", color="city",
                template="plotly_white", title="Cleanest Cities by Avg AQI"
            )
        )
    ], style={'backgroundColor': '#e8fff3', 'padding': '20px', 'borderRadius': '10px'})
])

# Time Series AQI
@app.callback(
    Output('time_series_plot', 'figure'),
    Input('city_selector', 'value')
)
def update_time_series(selected_city):
    city_df = df[df['city'] == selected_city].sort_values('datetime')
    fig = px.line(city_df, x='datetime', y='AQI', title=f"AQI Trend — {selected_city}", template='plotly_white')
    return fig

# Daily Pollutant Plot
@app.callback(
    Output('daily_pollutant_plot', 'figure'),
    [Input('city_selector', 'value'), Input('pollutant_dropdown', 'value')]
)
def update_pollutant_plot(selected_city, pollutant):
    city_data = df_daily[df_daily['city'] == selected_city]
    fig = px.line(city_data, x='date', y=pollutant,
                  title=f'Daily Avg {pollutant.upper()} — {selected_city}',
                  template='plotly_white')
    return fig

@app.callback(
    Output('weather_trend_plot', 'figure'),
    [Input('city_selector', 'value'),
     Input('weather_dropdown', 'value')]
)
def update_weather_plot(selected_city, weather_param):
    city_weather = df[df['city'] == selected_city].copy()
    city_weather = city_weather.groupby('date')[weather_param].mean().reset_index()
    param_name = weather_param.replace('_', ' ').title()
    
    fig = px.line(city_weather, x='date', y=weather_param,
                  title=f'{param_name} Trend — {selected_city}',
                  template='plotly_white')
    return fig

# AQI Category Box
@app.callback(
    Output('aqi_category_box', 'children'),
    Input('city_selector', 'value')
)
def update_aqi_category(selected_city):
    avg_aqi = df[df['city'] == selected_city]['AQI'].mean()
    if avg_aqi <= 50:
        category = "Good ✅"
    elif avg_aqi <= 100:
        category = "Moderate 🙂"
    elif avg_aqi <= 150:
        category = "Unhealthy for Sensitive 🟡"
    elif avg_aqi <= 200:
        category = "Unhealthy 🔴"
    elif avg_aqi <= 300:
        category = "Very Unhealthy 🟣"
    else:
        category = "Hazardous ☠️"
    return f"Average AQI: {avg_aqi:.1f} → {category}"

@app.callback(
    Output('pollutant_city_info', 'children'),
    [Input('pollutant_selector', 'value')]
)
def update_pollutant_info(pollutant):
    if pollutant:
        top_city = df.groupby('city')[pollutant].mean().idxmax()
        avg_val = df.groupby('city')[pollutant].mean().max()
        description = pollutant_descriptions[pollutant]

        return (
            f"📍 City with highest average {pollutant.upper()}: {top_city} ({avg_val:.2f})\n\n"
            f"🧪 About {pollutant.upper()}:\n{description}"
        )
    return "Select a pollutant to view details."

# Run app
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, host="0.0.0.0", port=port)
 


# In[ ]:






