import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

df2 = pd.read_csv('df2.csv')
x = df2['total_cases'].sum()
y = df2['total_deaths'].sum()
z = df2['total_recovered'].sum()
df3 = pd.read_csv('covid1 (1).csv')
df4 = pd.read_csv('df3.csv')
fig1 = px.pie(names=df3['country'][:30],values =df3['total_cases'][:30])
df3['tc/population'] = df3['total_cases']/df3['population']
fig3 = px.pie(names=df3['country'][:30],values =df3['tc/population'][:30])
#df4['text'] = ','.join(df4['country'],df4['active_cases'])
fig2 = {'data':[go.Bar(x = df3['continent'],y = df3['total_cases'])],'layout':go.Layout(title ='Continent/Total_cases')}
fig = px.choropleth(locations=df4['code2'],color=df4['total_cases'],hover_name=df4['active_cases'],projection='natural earth',color_continuous_scale=px.colors.sequential.Plasma_r)

external_stylesheet = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh',
        'crossorigin': 'anonymous'
    }
]
options = [
    {'label':'All', 'value': 'All'},
    {'label':'Total_deaths_in_each_country', 'value':'Total_deaths_in_each_country'},
    {'label': 'Total_recoverd_in_each_country','value':'Total_recoverd_in_each_country'},
    {'label':'Active_cases_in_individual_country','value':'Active_cases_in_individual_country'}

    ]

app = dash.Dash(__name__, external_stylesheets = external_stylesheet)


app.layout= html.Div([html.H1('Covid Dashboard',style={'color':'red','text-align':'center'}),html.Div([html.Div([html.Div([html.Div([dcc.Dropdown(id = 'drop',options = options, value = 'All'),dcc.Graph(id = 'bar')],
className='card-body')],className='card ')],className = 'col-md-6'),html.Div([html.Div([html.Div([html.H4('Percentage of cases carried in individual country from total cases',style= {'text-align':'center','color':'red'}),dcc.Graph(figure = fig1)],className = 'card-body')],className = 'card ')],className ='col-md-6')],className='row'),
html.Div([html.Div([html.Div([html.Div([html.H5('Total cases',style= {'color':'red','text-align':'center'}),
html.H5(x,style = {'text-align':'center','color':'red'}),
html.H5('Total Deaths',style ={'color':'orange','text-align':'center',}),
html.H5(y,style = {'text-align':'center','color':'orange'}),html.H5('Total Recovered',style ={'text-align':'center','color':'green'}),
html.H5(z,style ={'text-align':'center','margin-right': '10px','color':'green'})],className='card-body')],className ='card')],className = 'col-md-2'),
html.Div([html.Div([html.Div([html.H4('Continent vs Total cases',style ={'text-align':'center','color':'red','font':'italic'}),dcc.Graph(figure = fig2)],className = 'card-body')],className = 'card')],className = 'col-md-4'),
html.Div([html.Div([html.Div([html.H4('Percentage of population impacted in individual country out of their population',style = {'text-align':'center','color':'red'}),dcc.Graph(figure = fig3)],className = 'card-body')],className ='card')],className = 'col-md-6')],
className='row'),
html.Div([html.Div([html.Div([html.Div([html.H3('Active cases in worldview',style ={'text-align':'center','color':'red'}),dcc.Graph(figure = fig)],className = 'card-body')],className = 'card')],className = 'col-md-9'),
 html.Div([html.Div([html.Div([html.H2('Note',style = {'text-align':'center', 'color':'red'}), html.H5('The drop down box plots and the pie charts represt the stats for top 30 countries that were impacted by Covid 19.',style = {'text-align':'center','color':'blue'})],className = 'card-body')],className = 'card')],className = 'col-md-3')],
 className = 'row')],className='container ')



@app.callback(Output('bar','figure'), [Input('drop','value')])
def graph1(type):
    if type == 'All':
        return {'data':[go.Bar(x= df3['country'][:30],y = df3['total_cases'][:30])],'layout':go.Layout(title = 'Total cases in individual country')}

    elif type == 'total_deaths_in_each_country':
        return {'data': [go.Bar(x = df3['country'][:30], y = df3['td/tc'][:30])],'layout': go.Layout(title = 'Total deaths in individual country out of total cases')}
    

    elif type == 'Total_recovered_in_each_country':
        return { 'data':[go.Bar(x = df3['country'][:30], y = df3['td/tr'][:30])],'layout': go.Layout(title = 'Total recovered in individual country out of total cases')}

    else:
        return {'data':[go.Bar(x=df3['country'][:30],y = df3['active_cases'])],'layout':go.Layout(title ='Active cases in individual country')}

if __name__ == '__main__':
    app.run(debug = True)
