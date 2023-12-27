from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('./Video_Games_Sales_as_at_22_Dec_2016.csv')

# Use a dark-themed Bootstrap CSS
external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootswatch@4.4.1/dist/darkly/bootstrap.min.css', 'assets/custom.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

regionsList = ['NA', 'JP', 'EU', 'Other', 'Global']
region_sales_suffix = '_Sales'

platformList = df['Platform'].dropna().unique()

publisherList = df['Publisher'].dropna().unique()

genreList = df['Genre'].dropna().unique()

def animated_graph():
    regions = [region + region_sales_suffix for region in regionsList]

    yearly_region_sales = df.groupby('Year_of_Release')[regions].sum().reset_index()

    melted_data = yearly_region_sales.melt(id_vars='Year_of_Release', value_vars=regions, var_name='Region', value_name='Sales')

    fig = px.bar(
        melted_data,
        x='Region',
        y='Sales',
        color='Region',
        animation_frame='Year_of_Release',
        range_y=[0, melted_data['Sales'].max() + 10],
        title="Yearly Sales(M) Distribution by Region",
    )

    fig.update_layout(
        paper_bgcolor='rgba(34, 33, 35, 1)',  # Dark background color
        plot_bgcolor='rgba(40, 40, 40, 1)',   # Dark background color
        font=dict(color='white'),             # Text color for better contrast
    )  

    return fig

# Define the app layout
app.layout = html.Div([
    html.Div([
        html.H2(children='Video Game Sales Dashboard', style={'textAlign':'center'}),
        
        # Year Range Slider
        html.Label("Select a range of years:"),
        dcc.RangeSlider(
            id='year-selection',
            min=int(df['Year_of_Release'].min()),
            max=int(df['Year_of_Release'].max()),
            step=1,
            marks={},
            value=[int(df['Year_of_Release'].min()), int(df['Year_of_Release'].max())]
        ),
        # Display selected range as two boxes
        html.Div(id='selected-year-range', style={'display': 'flex', 'justify-content': 'space-between'}),
        
        # Region Selector and Button
        html.Label("Select regions:"),
        dcc.Dropdown(regionsList, regionsList, id='region-selection', multi=True),
        html.Button('Select/Deselect all regions', id='region-select-all-button',
                style={
                'backgroundColor': '#007BFF',  # Bootstrap primary color
                'color': 'white',
                'border': 'none',
                'borderRadius': '4px',
                'padding': '10px 15px',
                'margin': '5px 0',
                'cursor': 'pointer',
                'fontSize': '14px',
                'fontWeight': 'bold',
                'textTransform': 'uppercase',
                'letterSpacing': '1px',
                'display': 'block',  # or 'inline-block' if you prefer
                'width': '100%',  # Adjust as needed
                'textAlign': 'center',
            }),
        
        # Platform Selector and Button
        html.Label("Select platforms:"),
        dcc.Dropdown(platformList, platformList, id='platform-selection', multi=True, style={'minHeight': '80px', 'maxHeight': '80px', 'overflowY': 'auto'}),
        html.Button('Select/Deselect all platforms', id='platform-select-all-button',
                style={
                'backgroundColor': '#007BFF',  # Bootstrap primary color
                'color': 'white',
                'border': 'none',
                'borderRadius': '4px',
                'padding': '10px 15px',
                'margin': '5px 0',
                'cursor': 'pointer',
                'fontSize': '14px',
                'fontWeight': 'bold',
                'textTransform': 'uppercase',
                'letterSpacing': '1px',
                'display': 'block',  # or 'inline-block' if you prefer
                'width': '100%',  # Adjust as needed
                'textAlign': 'center'
            }),
        
        # Publisher Selector and Button
        html.Label("Select publishers:"),
        dcc.Dropdown(
            options=[{'label': i, 'value': i} for i in publisherList],
            value=publisherList,
            multi=True,
            searchable=True,
            id='publisher-selection',
            style={'minHeight': '80px', 'maxHeight': '80px', 'overflowY': 'auto'}
        ),
        html.Button('Select/Deselect all publishers', id='publisher-select-all-button',
                style={
                'backgroundColor': '#007BFF',  # Bootstrap primary color
                'color': 'white',
                'border': 'none',
                'borderRadius': '4px',
                'padding': '10px 15px',
                'margin': '5px 0',
                'cursor': 'pointer',
                'fontSize': '14px',
                'fontWeight': 'bold',
                'textTransform': 'uppercase',
                'letterSpacing': '1px',
                'display': 'block',  # or 'inline-block' if you prefer
                'width': '100%',  # Adjust as needed
                'textAlign': 'center'
            }),
        
        # Genre selector
        html.Label("Select genres:"),
        dcc.Dropdown(genreList, genreList, id='genre-selection', multi=True, style={'minHeight': '80px', 'maxHeight': '80px', 'overflowY': 'auto'}), 
        html.Button('Select/Deselect all genres', id='genre-select-all-button',
                style={
                'backgroundColor': '#007BFF',  # Bootstrap primary color
                'color': 'white',
                'border': 'none',
                'borderRadius': '4px',
                'padding': '10px 15px',
                'margin': '5px 0',
                'cursor': 'pointer',
                'fontSize': '14px',
                'fontWeight': 'bold',
                'textTransform': 'uppercase',
                'letterSpacing': '1px',
                'display': 'block',  # or 'inline-block' if you prefer
                'width': '100%',  # Adjust as needed
                'textAlign': 'center'
            }),
        html.A(
        html.Button('Open Project Report', style={'backgroundColor': '#007BFF', 'color': 'white'}),
        href='https://github.com/martinloevborg/Data-Visualization-project/blob/main/Data_Visualization_2023_Group_5.pdf',
        target='_blank'
        ),
    ], style={'position': 'fixed', 'top': 0, 'left': 0, 'bottom': 0, 'width': '20%', 'padding': '20px'}),
    
    html.Div([
        html.H3("Sales(M) distribution by region", style={'textAlign': 'center', 'margin-top': '20px'}),
        html.Div(id='total-sales-boxes', className="total-sales-container", style={'text-align': 'center'}),
        html.Div([
            dcc.Graph(id='sales-by-region-line', style={'display': 'inline-block', 'width': '50%'}),
            dcc.Graph(id='sales-by-region-map', style={'display': 'inline-block', 'width': '50%'})
        ], style={'display': 'flex', 'flex-direction': 'row'}),
        dcc.Graph(figure=animated_graph()),        

        html.H3("Sales(M) distribution by genre", style={'textAlign': 'center', 'margin-top': '20px'}),
        html.Div([
            dcc.Graph(id='sales-by-genre-pie', style={'display': 'inline-block', 'width': '50%'}),
            dcc.Graph(id='sales-by-genre-bar', style={'display': 'inline-block', 'width': '50%'})
        ], style={'display': 'flex', 'flex-direction': 'row'}),

        html.H3("Game popularity", style={'textAlign': 'center', 'margin-top': '20px'}),
        html.Div([
            dcc.Graph(id='top-games-by-user-score', style={'display': 'inline-block', 'width': '50%'}),
            dcc.Graph(id='top-games-by-user-count', style={'display': 'inline-block', 'width': '50%'})
        ], style={'display': 'flex', 'flex-direction': 'row'}),
        html.Div([
            dcc.Graph(id='top-games-by-critic-score', style={'display': 'inline-block', 'width': '50%'}),
            dcc.Graph(id='critic-vs-user-score-comparison', style={'display': 'inline-block', 'width': '50%'})
        ], style={'display': 'flex', 'flex-direction': 'row'}),

        html.H3("Sales(M) distribution by platform", style={'textAlign': 'center', 'margin-top': '20px'}),
        dcc.Graph(id='sales-by-platform-bar'),

        html.H3("Sales(M) distribution by publisher", style={'textAlign': 'center', 'margin-top': '20px'}),
        dcc.Graph(id='top-publisher-by-sales')
    ], style={'marginLeft': '22%', 'marginTop': '20px', 'padding': '20px'}),
])

# Callback to update the selected year range display
@app.callback(
    Output('selected-year-range', 'children'),
    Input('year-selection', 'value')
)
def update_selected_year_range(year_range):
    return [
        html.Div(f"Min Year: {year_range[0]}", style={'flex': 1, 'textAlign': 'center'}),
        html.Div(f"Max Year: {year_range[1]}", style={'flex': 1, 'textAlign': 'center'})
    ]

def sales_by_region(selectedYears, selectedPlatforms, selectedPublishers, selectedGenres):
    figures = []

    min_year, max_year = selectedYears
    df_filtered = df[(df['Year_of_Release'] >= min_year) & 
                     (df['Year_of_Release'] <= max_year) & 
                     (df['Publisher'].isin(selectedPublishers)) & 
                     (df['Platform'].isin(selectedPlatforms)) &
                     df['Genre'].isin(selectedGenres)]

    #line_graph
    fig = go.Figure()
    fig.update_layout(
        hovermode='x unified'
    )
    
    regions = [region + region_sales_suffix for region in regionsList]
    regions_agg = {region: 'sum' for region in regions}

    geo_tdf = df_filtered.groupby(['Year_of_Release']).agg(regions_agg).reset_index()
    geo_tdf = geo_tdf.sort_values('Year_of_Release', ascending=True)

    if min_year == max_year:
        for region in regions:
            fig.add_trace(go.Bar(
                x=geo_tdf['Year_of_Release'],
                y=geo_tdf[region],
                name=region
            ))
    else:
        for region in regions:
            fig.add_trace(go.Scatter(
                x=geo_tdf['Year_of_Release'],
                y=geo_tdf[region],
                mode='lines',
                name=region
            ))

    fig.update_xaxes(type='category')
    fig.update_layout(
        paper_bgcolor='rgba(34, 33, 35, 1)',  # Dark background color
        plot_bgcolor='rgba(40, 40, 40, 1)',   # Dark background color
        font=dict(color='white'),             # Text color for better contrast
    )  
    figures.append(fig)

    #map
    sales_data = df_filtered[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum().round(2)

    locations = {
        'NA_Sales': {'lat': 40, 'lon': -100},
        'EU_Sales': {'lat': 50, 'lon': 10},
        'JP_Sales': {'lat': 36, 'lon': 138},
        'Other_Sales': {'lat': 0, 'lon': 0}
    }

    fig = go.Figure()
    fig.update_layout(
        paper_bgcolor='rgba(34, 33, 35, 1)',  # Dark background color
        plot_bgcolor='rgba(40, 40, 40, 1)',   # Dark background color
        font=dict(color='white'),             # Text color for better contrast
    )  
    for region, sales in sales_data.items():
        #marker_size = max(min(sales / 10, 50), 10)
        marker_size = sales / 50
        fig.add_trace(go.Scattergeo(
            lon=[locations[region]['lon']],
            lat=[locations[region]['lat']],
            text=f"{region}: {sales}M",
            marker=dict(size=marker_size, sizemode='area'),
            name=region

        ))

    fig.update_layout(
        geo=dict(
            showland=True,
            landcolor="rgb(217, 217, 217)",
            subunitcolor="rgb(217, 217, 217)",
            countrycolor="rgb(217, 217, 217)",
            showcountries=True,
            countrywidth=0.5,
            subunitwidth=0.5
        )
    )
    figures.append(fig)

    return figures

@app.callback(
    Output('total-sales-boxes', 'children'),
    [Input('year-selection', 'value'),
     Input('platform-selection', 'value'),
     Input('publisher-selection', 'value'),
     Input('genre-selection', 'value')]
)
def update_total_sales_boxes(selectedYears, selectedPlatforms, selectedPublishers, selectedGenres):
    min_year, max_year = selectedYears
    df_filtered = df[(df['Year_of_Release'] >= min_year) & 
                     (df['Year_of_Release'] <= max_year) & 
                     (df['Publisher'].isin(selectedPublishers)) & 
                     (df['Platform'].isin(selectedPlatforms)) &
                     df['Genre'].isin(selectedGenres)]

    regions = [region + region_sales_suffix for region in regionsList]
    total_sales = df_filtered[regions].sum()

    sales_boxes = []
    for region in regions:
        sales_boxes.append(
            html.Div(
                children=[
                    html.H6(region.replace("_Sales", "")),
                    html.P(f"{total_sales[region]:.2f}M")
                ],
                style={'display': 'inline-block', 'margin': '10px'}
            )
        )

    return sales_boxes


def sales_by_genre(selectedYears, selectedRegions, selectedPlatforms, selectedPublishers):
    figures = []
    if 'Global' in selectedRegions:
        region_sales_columns = ['Global' + region_sales_suffix]
    else:
        region_sales_columns = [region + region_sales_suffix for region in selectedRegions]

    min_year, max_year = selectedYears
    df_filtered = df[(df['Year_of_Release'] >= min_year) & 
                     (df['Year_of_Release'] <= max_year) & 
                     (df['Publisher'].isin(selectedPublishers)) & 
                     (df['Platform'].isin(selectedPlatforms))]

    df_genre_agg = df_filtered.groupby('Genre')[region_sales_columns].sum()
    df_genre_agg['Total_Sales'] = df_genre_agg.sum(axis=1)

    #pie
    fig = go.Figure(data=[go.Pie(labels=df_genre_agg.index, values=df_genre_agg['Total_Sales'])])
    fig.update_layout(
        paper_bgcolor='rgba(34, 33, 35, 1)',  # Dark background color
        plot_bgcolor='rgba(40, 40, 40, 1)',   # Dark background color
        font=dict(color='white'),             # Text color for better contrast
    )  

    figures.append(fig)

    #bar
    fig = go.Figure(data=[
        go.Bar(
            y=df_genre_agg.index,
            x=df_genre_agg['Total_Sales'],
            orientation='h'
        )
    ])
    fig.update_layout(
        xaxis_title="Total Sales(M)",
        yaxis_title="Genres",
        yaxis=dict(autorange="reversed")
    )
    fig.update_layout(
        paper_bgcolor='rgba(34, 33, 35, 1)',  # Dark background color
        plot_bgcolor='rgba(40, 40, 40, 1)',   # Dark background color
        font=dict(color='white'),             # Text color for better contrast
    )  
    fig.update_traces(text=df_genre_agg['Total_Sales'], textposition='auto')

    figures.append(fig)

    return figures

def top_games_by_user_score(selectedYears, selectedPlatforms, selectedPublishers, selectedGenres):
    min_year, max_year = selectedYears
    df_filtered = df[(df['Year_of_Release'] >= min_year) & 
                     (df['Year_of_Release'] <= max_year) & 
                     (df['Publisher'].isin(selectedPublishers)) & 
                     (df['Platform'].isin(selectedPlatforms)) &
                     df['Genre'].isin(selectedGenres)]

    aggregated_data = df_filtered.groupby('Name')['User_Score'].sum().reset_index()

    top_games = aggregated_data.sort_values(by='User_Score', ascending=False).head(10).round(2)

    fig = go.Figure([go.Bar(
        x=top_games['Name'],
        y=top_games['User_Score'],
        text=top_games['User_Score'],
        textposition='auto'
    )])
    fig.update_layout(
        paper_bgcolor='rgba(34, 33, 35, 1)',  # Dark background color
        plot_bgcolor='rgba(40, 40, 40, 1)',   # Dark background color
        font=dict(color='white'),             # Text color for better contrast
    )  
    

    fig.update_layout(
        title='Top 10 Video Games by User Score',
        xaxis_title='Game',
        yaxis_title='User Score',
        xaxis={'categoryorder':'total descending'}
    )

    return fig

def top_games_by_user_count(selectedYears, selectedPlatforms, selectedPublishers, selectedGenres):
    min_year, max_year = selectedYears
    df_filtered = df[(df['Year_of_Release'] >= min_year) & 
                     (df['Year_of_Release'] <= max_year) & 
                     (df['Publisher'].isin(selectedPublishers)) & 
                     (df['Platform'].isin(selectedPlatforms)) &
                     df['Genre'].isin(selectedGenres)]

    aggregated_data = df_filtered.groupby('Name')['User_Count'].sum().reset_index()
    
    top_games = aggregated_data.sort_values(by='User_Count', ascending=False).head(10)

    fig = go.Figure([go.Bar(
        x=top_games['Name'],
        y=top_games['User_Count'],
        text=top_games['User_Count'],
        textposition='auto'
    )])

    fig.update_layout(
        title='Top 10 Video Games by User Vote Count',
        xaxis_title='Game',
        yaxis_title='User Count',
        xaxis={'categoryorder':'total descending'}
    )

    fig.update_layout(
        paper_bgcolor='rgba(34, 33, 35, 1)',  # Dark background color
        plot_bgcolor='rgba(40, 40, 40, 1)',   # Dark background color
        font=dict(color='white'),             # Text color for better contrast
    )  

    return fig

def top_games_by_critic_score(selectedYears, selectedPlatforms, selectedPublishers, selectedGenres):
    min_year, max_year = selectedYears
    df_filtered = df[(df['Year_of_Release'] >= min_year) & 
                     (df['Year_of_Release'] <= max_year) & 
                     (df['Publisher'].isin(selectedPublishers)) & 
                     (df['Platform'].isin(selectedPlatforms)) &
                     df['Genre'].isin(selectedGenres)]

    aggregated_data = df_filtered.groupby('Name')['Critic_Score'].sum().reset_index()

    top_games = aggregated_data.sort_values(by='Critic_Score', ascending=False).head(10)

    fig = go.Figure([go.Bar(
        x=top_games['Name'],
        y=top_games['Critic_Score'],
        text=top_games['Critic_Score'],
        textposition='auto'
    )])

    fig.update_layout(
        title='Top 10 Video Games by Critic Score',
        xaxis_title='Game',
        yaxis_title='Critic Score',
        xaxis={'categoryorder':'total descending'}
    )

    fig.update_layout(
        paper_bgcolor='rgba(34, 33, 35, 1)',  # Dark background color
        plot_bgcolor='rgba(40, 40, 40, 1)',   # Dark background color
        font=dict(color='white'),             # Text color for better contrast
    )  

    return fig

def bar_chart_platform_sales(selectedYears, selectedRegions, selectedPublishers, selectedGenres):
    min_year, max_year = selectedYears
    df_filtered = df[(df['Year_of_Release'] >= min_year) & 
                     (df['Year_of_Release'] <= max_year) & 
                     (df['Publisher'].isin(selectedPublishers)) & 
                     df['Genre'].isin(selectedGenres)]

    region_sales_columns = [region + region_sales_suffix for region in selectedRegions]
    df_filtered['Total_Sales'] = df_filtered[region_sales_columns].sum(axis=1)

    platform_sales = df_filtered.groupby('Platform')['Total_Sales'].sum().reset_index()

    fig = px.bar(platform_sales, x='Platform', y='Total_Sales',
                      text='Platform',
                     title='Platform Sales(M)')

    fig.update_layout(
        xaxis_title='Platform',
        yaxis_title='Total Sales(M)',
        xaxis={'categoryorder':'total descending'},
        yaxis=dict(type='log')
    )

    fig.update_layout(
        paper_bgcolor='rgba(34, 33, 35, 1)',  # Dark background color
        plot_bgcolor='rgba(40, 40, 40, 1)',   # Dark background color
        font=dict(color='white'),             # Text color for better contrast
    )  

    return fig

def top_games_by_publisher(selectedYears, selectedPlatforms, selectedRegions, selectedGenres):
    min_year, max_year = selectedYears
    df_filtered = df[(df['Year_of_Release'] >= min_year) & 
                     (df['Year_of_Release'] <= max_year) & 
                     (df['Platform'].isin(selectedPlatforms)) &
                     df['Genre'].isin(selectedGenres)]
    
    region_sales_columns = [region + region_sales_suffix for region in selectedRegions]
    df_filtered['Total_Sales'] = df_filtered[region_sales_columns].sum(axis=1)

    publisher_sales = df_filtered.groupby('Publisher')['Total_Sales'].sum().sort_values(ascending=False).head(10)

    fig = go.Figure([go.Bar(
        x=publisher_sales.index,
        y=publisher_sales.values,
        text=publisher_sales.values,
        textposition='auto'
    )])

    fig.update_layout(
        title='Top 10 Publishers by Sales(M)',
        xaxis_title='Publisher',
        yaxis_title='Total Sales(M)',
        xaxis={'categoryorder':'total descending'}
    )

    fig.update_layout(
        paper_bgcolor='rgba(34, 33, 35, 1)',  # Dark background color
        plot_bgcolor='rgba(40, 40, 40, 1)',   # Dark background color
        font=dict(color='white'),             # Text color for better contrast
    )  

    return fig

def critic_vs_user_score_comparison(selectedYears, selectedGenres, selectedPlatforms, selectedPublishers):
    min_year, max_year = selectedYears
    df_filtered = df[(df['Year_of_Release'] >= min_year) & 
                     (df['Year_of_Release'] <= max_year) & 
                     (df['Publisher'].isin(selectedPublishers)) & 
                     (df['Platform'].isin(selectedPlatforms)) &
                     df['Genre'].isin(selectedGenres)]

    df_filtered['Critic_Score'] = pd.to_numeric(df_filtered['Critic_Score'], errors='coerce')
    df_filtered['User_Score'] = pd.to_numeric(df_filtered['User_Score'], errors='coerce')
    df_filtered = df_filtered.dropna(subset=['Critic_Score', 'User_Score'])

    fig = px.scatter(df_filtered, x='Critic_Score', y='User_Score', hover_name='Name',
                     title='Critic Score vs. User Score Comparison (Filtered Data)',
                     labels={'Critic_Score': 'Critic Score', 'User_Score': 'User Score'})

    fig.update_layout(
        xaxis_title='Critic Score',
        yaxis_title='User Score',
        xaxis={'range': [0, 100]},  
        yaxis={'range': [0, 10]}     
    )

    fig.update_layout(
        paper_bgcolor='rgba(34, 33, 35, 1)',  # Dark background color
        plot_bgcolor='rgba(40, 40, 40, 1)',   # Dark background color
        font=dict(color='white'),             # Text color for better contrast
    )  

    return fig

@callback(
    [Output('sales-by-region-line', 'figure'),
     Output('sales-by-region-map', 'figure'),
     Output('sales-by-genre-pie', 'figure'),
     Output('sales-by-genre-bar', 'figure'),
     Output('top-games-by-user-score', 'figure'),
     Output('top-games-by-user-count', 'figure'),
     Output('top-games-by-critic-score', 'figure'),
     Output('sales-by-platform-bar', 'figure'),
     Output('top-publisher-by-sales', 'figure'),
     Output('critic-vs-user-score-comparison', 'figure'),
    ],
    Input('year-selection', 'value'),
    Input('region-selection', 'value'),
    Input('platform-selection', 'value'),
    Input('publisher-selection', 'value'),
    Input('genre-selection', 'value')
)
def update_graphs(selectedYears, selectedRegions, selectedPlatforms, selectedPublishers, selectedGenres):

    figures = []

    figures.extend(sales_by_region(selectedYears, selectedPlatforms, selectedPublishers, selectedGenres))

    figures.extend(sales_by_genre(selectedYears, selectedRegions, selectedPlatforms, selectedPublishers))

    figures.append(top_games_by_user_score(selectedYears, selectedPlatforms, selectedPublishers, selectedGenres))
    figures.append(top_games_by_user_count(selectedYears, selectedPlatforms, selectedPublishers, selectedGenres))
    figures.append(top_games_by_critic_score(selectedYears, selectedPlatforms, selectedPublishers, selectedGenres))

    figures.append(bar_chart_platform_sales(selectedYears, selectedRegions, selectedPublishers, selectedGenres))

    figures.append(top_games_by_publisher(selectedYears, selectedPlatforms, selectedRegions, selectedGenres))

    figures.append(critic_vs_user_score_comparison(selectedYears, selectedGenres, selectedPlatforms, selectedPublishers))

    return figures



@app.callback(
    Output('region-selection', 'value'),
    [Input('region-select-all-button', 'n_clicks')],
    prevent_initial_call=True
)
def select_deselect_all_regions(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return regionsList
    else:
        return []
    
@app.callback(
    Output('platform-selection', 'value'),
    [Input('platform-select-all-button', 'n_clicks')],
    prevent_initial_call=True
)
def select_deselect_all_platforms(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return platformList
    else:
        return []

@app.callback(
    Output('publisher-selection', 'value'),
    [Input('publisher-select-all-button', 'n_clicks')],
    prevent_initial_call=True
)
def select_deselect_all_publishers(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return publisherList
    else:
        return []
    
@app.callback(
    Output('genre-selection', 'value'),
    [Input('genre-select-all-button', 'n_clicks')],
    prevent_initial_call=True
)
def select_deselect_all_genres(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return genreList
    else:
        return []


if __name__ == '__main__':
    app.run(debug=True)