import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, Input, Output, State, callback
from dash.dash_table.Format import Format, Group
import pandas as pd

# Load DataFrame from Excel
df = pd.read_excel('LK_Ledningsägare_5.0.xlsx')

# Extract unique 'Län' and 'Typ av ledningar' for dropdown options
unique_lans = df['Län'].dropna().explode().unique()
unique_lans = sorted(unique_lans, key=len)


unique_typ_av_ledningar = df['Typ av ledningar'].dropna().explode().unique()
unique_typ_av_ledningar = sorted(unique_typ_av_ledningar, key=len)

# Initialize the Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Custom style for the DataTable
custom_table_style = {
    'height': '500px', 
    'overflowY': 'auto',
    'overflowX': 'auto',
    'fontSize': '14px',
    'fontFamily': 'Arial',
    'border': '1px solid #dee2e6',
    'marginTop': '20px',
    'maxWidth': '100%'
}

# Custom style for cells
custom_cell_style = {
    'textAlign': 'left', 
    'padding': '10px', 
    'backgroundColor': '#f8f9fa', 
    'borderBottom': '1px solid #dee2e6',
    'lineHeight': '10px',
    'maxWidth': '200px',
    'minWidth': '40px'
    
}







# Set up the layout
app.layout = dbc.Container([
    html.H1('Ledningsägare Sverige Dashboard', className='text-center mb-4'),
    dbc.Row([
        dbc.Col([
            # text "Kolumner att visa"
            html.H4('Kolumner att visa'),
            dcc.Dropdown(
                id='column-selector',
                options=[{'label': col, 'value': col} for col in df.columns],
                value=list(df.columns),  # Default all columns selected
                multi=True
            ),
        ], width=3),
        dbc.Col([
            dcc.Input(
                id='search-input-lan',
                type='text',
                placeholder='Search län...',
                style={'width': '100%', 'padding': '10px', 'fontSize': '16px'}
            ),
            html.Div(
                dcc.Checklist(
                    id='checklist-lan',
                    options=[{'label': lan, 'value': lan} for lan in unique_lans],
                    value=[],  # Default no selection
                    inline=False,
                    inputStyle={"margin-right": "5px", "margin-left": "10px"},
                ),
                style={'height': '200px', 'overflowY': 'auto', 'marginTop': '10px', 'width': '100%'}
            )
        ], width=3),
        dbc.Col([
            dcc.Input(
                id='search-input-typ',
                type='text',
                placeholder='Search typ av ledningar...',
                style={'width': '100%', 'padding': '10px', 'fontSize': '16px'}
            ),
            html.Div(
                dcc.Checklist(
                    id='checklist-typ',
                    options=[{'label': typ, 'value': typ} for typ in unique_typ_av_ledningar],
                    value=[],  # Default no selection
                    inline=False,
                    inputStyle={"margin-right": "5px", "margin-left": "10px"}
                ),
                style={'height': '200px', 'overflowY': 'auto', 'marginTop': '10px'}
            )
        ], width=3)
    ]),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='table',
                columns=[
                            {
                                "name": i, 
                                "id": i,
                                "type": 'numeric' if i == "Omsättning (tkr)" else None,
                                "format": Format(group=True) if i == "Omsättning (tkr)" else None
                            } 
                            for i in df.columns
                        ],
                data=df.to_dict('records'),
                sort_action='native',
                fixed_columns={'headers': True, 'data': 1},
                fixed_rows={'headers': True, 'data': 0},
                style_table=custom_table_style,
                style_cell=custom_cell_style,
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
            )
        ], width=12)
    ])
], fluid=True)


# Callback to dynamically adjust visible columns based on user's selection
@app.callback(
    Output('table', 'columns'),
    Input('column-selector', 'value')
)
def update_columns(selected_columns):
    return [{"name": i, "id": i} for i in selected_columns]


@callback(
    Output('checklist-lan', 'options'),
    Input('search-input-lan', 'value'),
    State('checklist-lan', 'value')
)
def filter_options_lan(search_value, selected_values):
    if not search_value:
        return [{'label': lan, 'value': lan} for lan in unique_lans]
    filtered_lans = [lan for lan in unique_lans if search_value.lower() in lan.lower()]
    return [{'label': lan, 'value': lan} for lan in filtered_lans]

@callback(
    Output('checklist-typ', 'options'),
    Input('search-input-typ', 'value'),
    State('checklist-typ', 'value')
)
def filter_options_typ(search_value, selected_values):
    if not search_value:
        return [{'label': typ, 'value': typ} for typ in unique_typ_av_ledningar]
    filtered_typs = [typ for typ in unique_typ_av_ledningar if search_value.lower() in typ.lower()]
    return [{'label': typ, 'value': typ} for typ in filtered_typs]

@callback(
    Output('table', 'data'),
    [Input('checklist-lan', 'value'), Input('checklist-typ', 'value')]
)
def update_table(selected_lans, selected_typs):
    if not selected_lans and not selected_typs:
        # If no selections, show all data
        filtered_df = df
    elif not selected_lans:
        # If only "Typ av ledningar" is selected
        filtered_df = df[df['Typ av ledningar'].isin(selected_typs)]
    elif not selected_typs:
        # If only "Län" is selected
        filtered_df = df[df['Län'].isin(selected_lans)]
    else:
        # Both filters are selected
        filtered_df = df[(df['Län'].isin(selected_lans)) & (df['Typ av ledningar'].isin(selected_typs))]

    return filtered_df.to_dict('records')

# Uncomment to initialize the app
if __name__ == '__main__':
    app.run_server(debug=True, port=4093)
