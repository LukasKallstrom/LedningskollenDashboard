import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, Input, Output, State, callback
import dash.dash_table.FormatTemplate as FormatTemplate
from dash.dash_table.Format import Format, Group, Scheme
import pandas as pd
import plotly.express as px
import numpy as np
import io

# Load DataFrame from Excel
df = pd.read_excel('Ledningsägare.xlsx')

# Extract unique 'Län' and 'Typ av ledningar' for dropdown options
unique_lans = df['Län'].dropna().explode().unique()
unique_lans = sorted(unique_lans, key=len)

unique_foretag = df['Företag'].dropna().explode().unique()
unique_foretag = sorted(unique_foretag, key=len)


unique_typ_av_ledningar = df['Typ av ledningar'].dropna().explode().unique()
unique_typ_av_ledningar = sorted(unique_typ_av_ledningar, key=len)

# Initialize the Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Custom style for the DataTable
custom_table_style = {
    'height': '700px',
    'maxHeight': '80%', 
    'overflowX': 'auto',
    'fontSize': '14px',
    'fontFamily': 'Arial',
    'border': '1px solid #dee2e6',
    'marginTop': '20px',
    'maxWidth': '100%',
    'width': '100%',
    'minWidth': '800px',
}

# Custom style for cells
custom_cell_style = {
    'textAlign': 'left', 
    'backgroundColor': '#f8f9fa', 
    'borderBottom': '1px solid #dee2e6',
    'lineHeight': '12px',
    'maxWidth': '400px',
    'minWidth': '40px'
    
}

# Set up the layout
app.layout = dbc.Container(
    [
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
                id='search-input-foretag',
                type='text',
                placeholder='Search företag...',
                style={'width': '100%', 'padding': '10px', 'fontSize': '16px'}
            ),
            html.Div(
                [
                dcc.Checklist(
                            id='select-all-foretag',
                            labelStyle={"margin-left": "10px"},
                            className='mb-2',
                            options=[{'label': 'Select All', 'value': 'all'}],
                            value=[]
                        ),
                dcc.Checklist(
                    id='checklist-foretag',
                    options=[{'label': foretag, 'value': foretag} for foretag in unique_foretag],
                    value=[],  # Default no selection
                    inline=False,
                    inputStyle={"margin-right": "5px", "margin-left": "10px"},
                )],
                style={'height': '400px', 'overflowY': 'auto', 'marginTop': '10px', 'width': '100%'}
            )
        ], width=3),
        dbc.Col([
            dcc.Input(
                id='search-input-lan',
                type='text',
                placeholder='Search län...',
                style={'width': '100%', 'padding': '10px', 'fontSize': '16px'}
            ),
            html.Div(
                [
                dcc.Checklist(
                            id='select-all-lan',
                            labelStyle={"margin-left": "10px"},
                            className='mb-2',
                            options=[{'label': 'Select All', 'value': 'all'}],
                            value=[]
                        ),
                dcc.Checklist(
                    id='checklist-lan',
                    options=[{'label': lan, 'value': lan} for lan in unique_lans],
                    value=[],  # Default no selection
                    inline=False,
                    inputStyle={"margin-right": "5px", "margin-left": "10px"},
                )],
                style={'height': '400px', 'overflowY': 'auto', 'marginTop': '10px', 'width': '100%'}
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
                [
                        dcc.Checklist(
                            id='select-all-typ',
                            labelStyle={"margin-left": "10px"},
                            className='mb-2',
                            options=[{'label': 'Select All', 'value': 'all'}],
                            value=[]
                        ),
                        dcc.Checklist(
                            id='checklist-typ',
                            options=[{'label': typ, 'value': typ} for typ in unique_typ_av_ledningar],
                            value=[],
                            inline=False,
                            inputStyle={"margin-right": "5px", "margin-left": "10px"}
                        )
                    ],
                style={'height': '400px', 'overflowY': 'auto', 'marginTop': '10px'}
            )
        ],
          width=3),
          dbc.Col([
              dcc.RadioItems(
                id='search-mode',
                options=[
                    {'label': 'Exclusive', 'value': 'exclusive'},
                    {'label': 'Inclusive', 'value': 'inclusive'}
                ],
                value='exclusive',  # Default to exclusive
                labelStyle={'display': 'block'}
            ),
            html.Div([
                # ... existing components ...
                html.Button("Download Excel", id="btn_excel"),
                dcc.Download(id="download-excel"),
                dcc.Store(id='store-dataframe')
            ])
        ],
          width=3),
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
                                "format": FormatTemplate.money(0) if i == "Omsättning (tkr)" else None,
                            } 
                            for i in df.columns
                        ],
                data=df.to_dict('records'),
                sort_action='native',
                fixed_columns={'headers': True, 'data': 1},
                fixed_rows={'headers': True, 'data': 0},
                style_table=custom_table_style,
                style_cell=custom_cell_style,
                style_data={'whiteSpace': 'normal',
                    'height': 'auto',
                },
            )
        ], width=12)
    ])
], fluid=True)

# Generic callback to handle select all for different checklists
# This callback manages both select all and deselect all actions based on a toggle button


# Optimized callback to update visible columns in a table based on user's selection
@app.callback(
    Output('table', 'columns'),
    Input('column-selector', 'value')
)
def update_columns(selected_columns):
    return [{"name": i, "id": i} for i in selected_columns]

def filter_options(query, unique_items):
    if not query:
        return [{'label': item, 'value': item} for item in unique_items]
    query = query.lower()
    return [{'label': item, 'value': item} for item in unique_items if query in item.lower()]

# Callback for select/deselect all functionality (now includes 'foretag')
@app.callback(
    [Output('checklist-lan', 'value'), Output('checklist-typ', 'value'), Output('checklist-foretag', 'value')],
    [Input('select-all-lan', 'value'), Input('select-all-typ', 'value'), Input('select-all-foretag', 'value'),
     Input('search-input-lan', 'value'), Input('search-input-typ', 'value'), Input('search-input-foretag', 'value')],
    [State('checklist-lan', 'options'), State('checklist-typ', 'options'), State('checklist-foretag', 'options')]
)
def update_selections(select_all_lan, select_all_typ, select_all_foretag,
                      search_input_lan, search_input_typ, search_input_foretag, options_lan, options_typ, options_foretag):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    current_lan_options = filter_options(search_input_lan, [opt['value'] for opt in options_lan])
    current_typ_options = filter_options(search_input_typ, [opt['value'] for opt in options_typ])
    current_foretag_options = filter_options(search_input_foretag, [opt['value'] for opt in options_foretag])

    updates = [dash.no_update] * 3  # lan, typ, foretag
    if 'select-all' in button_id:
        index = ['lan', 'typ', 'foretag'].index(button_id.split('-')[2])
        if ctx.triggered[0]['value'] == ['all']:
            updates[index] = [option['value'] for option in [current_lan_options, current_typ_options, current_foretag_options][index]]
        else:
            updates[index] = []
    return updates



# Callback for updating filter options (includes 'foretag')
@app.callback(
    [Output('checklist-lan', 'options'), Output('checklist-typ', 'options'), Output('checklist-foretag', 'options')],
    [Input('search-input-lan', 'value'), Input('search-input-typ', 'value'), Input('search-input-foretag', 'value')]
)
def update_filter_options(search_lan, search_typ, search_foretag):
    filtered_lans = filter_options(search_lan, unique_lans)
    filtered_typs = filter_options(search_typ, unique_typ_av_ledningar)
    filtered_foretag = filter_options(search_foretag, unique_foretag)
    return filtered_lans, filtered_typs, filtered_foretag


# Callback to update table data based on multiple filters
@app.callback(
    Output('table', 'data'),
    [Input('checklist-lan', 'value'), Input('checklist-typ', 'value'), Input('checklist-foretag', 'value'), Input('search-mode', 'value')]
)
def update_table(selected_lans, selected_typs, selected_foretags, search_mode):
    conditions = []
    if selected_lans:
        conditions.append(df['Län'].isin(selected_lans))
    if selected_typs:
        conditions.append(df['Typ av ledningar'].isin(selected_typs))
    if selected_foretags:
        conditions.append(df['Företag'].isin(selected_foretags))
    
    if conditions:
        if search_mode == 'exclusive':
            filtered_df = df[np.logical_and.reduce(conditions)]
        else:
            filtered_df = df[np.logical_or.reduce(conditions)]
    else:
        filtered_df = df
    
    return filtered_df.to_dict('records')

@app.callback(
    Output('store-dataframe', 'data'),
    Input('table', 'data')
)
def store_df(current_table_data):
    # Assuming 'current_table_data' is the up-to-date data in JSON format
    return current_table_data

@app.callback(
    Output("download-excel", "data"),
    Input("btn_excel", "n_clicks"),
    State("store-dataframe", "data"),
    prevent_initial_call=True
)
def download_excel(n_clicks, stored_data):
    if stored_data is None:
        raise dash.exceptions.PreventUpdate

    # Convert the stored JSON data back to a dataframe
    current_df = pd.DataFrame.from_dict(stored_data)

    # Convert the dataframe to an Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        current_df.to_excel(writer, sheet_name='Sheet1')
    output.seek(0)
    
    # Send the file to the user's browser

    return dcc.send_bytes(output, "my_dataframe.xlsx")

# Uncomment to initialize the app
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=4093,  use_reloader=False)
