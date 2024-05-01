import dash
from dash import dcc, html, dash_table, Input, Output
import pandas as pd

# Load DataFrame from Excel
df = pd.read_excel('LK_Ledningsägare.xlsx')

# Extract unique 'Län' for dropdown options
unique_lans = [
 'Blekinge län',
 'Dalarnas län',
 'Gotlands län',
 'Gävleborgs län',
 'Hallands län',
 'Jämtlands län',
 'Jönköpings län',
 'Kalmar län',
 'Kronobergs län',
 'Norrbottens län',
 'Skåne län',
 'Stockholms län',
 'Södermanlands län',
 'Uppsala län',
 'Värmlands län',
 'Västerbottens län',
 'Västernorrlands län',
 'Västmanlands län',
 'Västra Götalands län',
 'Örebro län',
 'Östergötlands län']

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server
# Set up the layout
app.layout = html.Div([
    html.H1('Ledningsägare Sverige Dashboard', style={'textAlign': 'center', 'color': '#007BFF'}),
    html.Div([
        dcc.Dropdown(
            id='dropdown-lan',
            options=[{'label': lan, 'value': lan} for lan in unique_lans],
            multi=True,  # Allows multiple selections
            placeholder='Välj län...',
            style={'width': '50%', 'padding': '10px', 'margin': 'auto'}  # Styling the dropdown
        )
    ], style={'display': 'flex', 'justifyContent': 'center', 'padding': '20px'}),
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            sort_action='native',  # Enables basic sorting
            style_table={'height': '95%', 'overflowY': 'auto', 'minWidth': '100%'},
            style_cell={'textAlign': 'left', 'padding': '10px', 'fontFamily': 'Arial', 'fontSize': '14px'},
            fixed_columns={'headers': True, 'data': 1},
            fixed_rows={'headers': True, 'data': 0},
        )
    ], style={'padding': '20px', 'margin': 'auto', 'width': '95%', 'height': '100%'}),
], style={'fontFamily': 'Sans-serif', 'backgroundColor': '#F9F9F9', 'height': '100%'})

@app.callback(
    Output('table', 'data'),
    [Input('dropdown-lan', 'value')]
)
def update_table(selected_lans):
    if selected_lans:
        filtered_df = df[df['Län'].apply(lambda x: any(lan in x for lan in selected_lans) if pd.notna(x) else False)]
    else:
        filtered_df = df
    return filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True, port=4093)
