import pandas as pd
import plotly.express as px
import plotly.io as pio
import dash
from dash import dcc,html
import dash_bootstrap_components as dbc
import numpy as np
from dash import Input,Output
from dash_bootstrap_templates import ThemeSwitchAIO
import joblib
from model import new_df

df=pd.read_csv("data/TB_Burden_Country.csv")
# df=df.dropna()
# df=df.drop_duplicates()
# print(df["Country or territory name"].dtype)
countries=df["Country or territory name"].unique().tolist()
continents=pd.read_csv("data/Countries by continents.csv")
# continents["Continent_lower"]=continents["Continent"].str.lower()
continents.rename(columns={"Country":"Country or territory name"},inplace=True)
merged_df=pd.merge(df,continents,how="inner",on="Country or territory name")
# print(countries)
new_df_cols=new_df.columns.tolist()
model=joblib.load("trained_regressor.pkl")
app=dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.themes.DARKLY])
server = app.server

app.layout=dbc.Container([
    html.H1("Tuberculosis Dashboard",style={"textAlign":"center"}),
    ThemeSwitchAIO(
        aio_id="theme", 
        themes=[dbc.themes.BOOTSTRAP, dbc.themes.DARKLY]
    ),
    dbc.Row([
        dbc.Col([
            html.Label("Select a Country or Territory"),
            dcc.Dropdown(
                id="country-picker",options=countries,value="India"
            )
        ],width=10,className="mb-3")
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Select starting date: "),
            dcc.Dropdown(id="start-date",options=df["Year"].unique().tolist(),value=1990)
        ],width=6),
        dbc.Col([
            html.Label("Select ending date: "),
            dcc.Dropdown(id="end-date",options=df["Year"].unique().tolist(),value=1991)
        ],width=6)
    ],className="mb-3"),
    dbc.Tabs([
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dbc.Card(dcc.Graph(id="prevalence-graph",figure={}))
                ],width=10,style={"margin":"auto"})
            ],className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Card(dcc.Graph(id="prevalence-map",figure={}))
                ],width=10,style={"margin":"auto"})
            ],className="mb-3")
        ],label="TB Prevalence",tab_id="prevalence_tab"),
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dbc.Card(dcc.Graph(id="nohiv",figure={}))
                ],lg=6,xs=12),
                dbc.Col([
                    dbc.Card(dcc.Graph(id="hiv",figure={}))
                ],lg=6,xs=12)
            ],className="mb-3"),
        ],label="Estimated Mortality",tab_id="mortality_tab"),
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dbc.Card(dcc.Graph(id="death-nohiv",figure={}))
                ],lg=6,xs=12),
                dbc.Col([
                    dbc.Card(dcc.Graph(id="death-hiv",figure={}))
                ],lg=6,xs=12)
            ],className="mb-3"),
        ],label="Estimated Deaths",tab_id="death_tab"),
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dbc.Card(dcc.Graph(id="case-detection",figure={}))
                ],width=10,style={"margin":"auto"})
            ],className="mb-3"),
        ],label="Case Detection",tab_id="case_detection"),
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dbc.Card(dcc.Graph(id="incidence",figure={}))
                ],width=10,style={"margin":"auto"})
            ],className="mb-3"),
        ],label="TB Incidence",tab_id="incidence_tb"), 
    ],active_tab="prevalence_tab",style={"marginBottom":40})
],fluid=True)

@app.callback(
    [Output(component_id="prevalence-graph",component_property="figure"),
     Output(component_id="prevalence-map",component_property="figure"),
     Output(component_id="nohiv",component_property="figure"),
     Output(component_id="hiv",component_property="figure"),
     Output(component_id="death-nohiv",component_property="figure"),
     Output(component_id="death-hiv",component_property="figure"),
     Output(component_id="case-detection",component_property="figure"),
     Output(component_id="incidence",component_property="figure")],
    [Input(component_id="country-picker",component_property="value"),
     Input(component_id="start-date",component_property="value"),
     Input(component_id="end-date",component_property="value"),
     Input(ThemeSwitchAIO.ids.switch("theme"),"value")]
)
def generate_charts(country,start_year,end_year,theme_toggle):
    country_df=df[
        (df["Country or territory name"]==country) & (df["Year"]>=start_year) & (df["Year"]<=end_year)
    ]
    current_template = "plotly" if theme_toggle else "plotly_dark"

    tb_prevalence_chart=px.bar(
        data_frame=country_df,
        x="Year",
        y="Estimated prevalence of TB (all forms)",
        title=f"Estimated prevalence of TB (all forms) in {country} from {start_year} to {end_year}",
        labels={"Estimated prevalence of TB (all forms)":"Estimated Prevalence of TB"},
        range_x=[start_year,end_year],
        hover_name="Country or territory name",
        color="Method to derive prevalence estimates",
    )

    prevalence_map=px.choropleth(
        data_frame=merged_df,
        locations="ISO 3-character country/territory code",
        hover_name="Country or territory name",
        title="Estimated Prevalence of TB across countries",
        color="Estimated prevalence of TB (all forms)",
        color_continuous_scale=px.colors.sequential.YlOrRd,
        animation_frame="Year"
    )
    prevalence_map.update_layout(
        margin={"r":0,"t":50,"l":0,"b":0},
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        )
    )

    tb_mortality_chart_nohiv=px.line(
        data_frame=country_df,
        x="Year",
        y="Estimated mortality of TB cases (all forms, excluding HIV) per 100 000 population",
        title=f"Estimated mortality of TB cases (all forms, excluding HIV) per 100 000 <br>population in {country} from {start_year} to {end_year}",
        labels={"Estimated mortality of TB cases (all forms, excluding HIV) per 100 000 population":"Estimated Mortality of TB"},
        range_x=[start_year,end_year],
        hover_name="Country or territory name",
        color="Method to derive mortality estimates",
        # error_y="Estimated number of deaths from TB (all forms, excluding HIV), high bound",
        # error_y_minus="Estimated number of deaths from TB (all forms, excluding HIV), low bound"
    )

    tb_mortality_chart_hiv=px.line(
        data_frame=country_df,
        x="Year",
        y="Estimated mortality of TB cases who are HIV-positive, per 100 000 population",
        title=f"Estimated mortality of TB cases who are HIV-positive, per 100 000<br>population in {country} from {start_year} to {end_year}",
        labels={"Estimated mortality of TB cases who are HIV-positive, per 100 000 population":"Estimated Mortality of TB"},
        range_x=[start_year,end_year],
        hover_name="Country or territory name",
        color="Method to derive mortality estimates"
    )

    tb_death_chart_nohiv=px.line(
        data_frame=country_df,
        x="Year",
        y="Estimated number of deaths from TB (all forms, excluding HIV)",
        title=f"Estimated number of deaths from TB (all forms, excluding HIV) in <br>{country} from {start_year} to {end_year}",
        labels={"Estimated number of deaths from TB (all forms, excluding HIV)":"Estimated deaths from TB"},
        range_x=[start_year,end_year],
        hover_name="Country or territory name",
        # color="Method to derive mortality estimates"
    )

    tb_death_chart_hiv=px.line(
        data_frame=country_df,
        x="Year",
        y="Estimated number of deaths from TB in people who are HIV-positive",
        title=f"Estimated number of deaths from TB in people who are HIV-positive in <br>{country} from {start_year} to {end_year}",
        labels={"Estimated number of deaths from TB in people who are HIV-positive":"Estimated deaths from TB"},
        range_x=[start_year,end_year],
        hover_name="Country or territory name",
        # color="Method to derive mortality estimates"
    )
    #Case detection rate (all forms), percent
    tb_case_detection=px.line(
        data_frame=country_df,
        x="Year",
        y="Case detection rate (all forms), percent",
        title=f"Case Detection rate (all forms) percent in {country} from {start_year} to {end_year}",
        labels={"Case detection rate (all forms), percent":"Estimated Case Detection"},
        range_x=[start_year,end_year],
        hover_name="Country or territory name"
        # color="Method to derive mortality estimates"
    )

    tb_incidence_graph=px.line(
        data_frame=country_df,
        x="Year",
        y="Estimated number of incident cases (all forms)",
        title=f"Estimated number of incident cases (all forms) in {country} from {start_year} to {end_year}",
        labels={"Estimated number of incident cases (all forms)":"Estimated number of incident cases"},
        range_x=[start_year,end_year],
        hover_name="Country or territory name",
        color="Method to derive incidence estimates"
    )

    for fig in [tb_prevalence_chart,prevalence_map,tb_mortality_chart_nohiv,tb_mortality_chart_hiv,tb_death_chart_nohiv,tb_death_chart_hiv,tb_case_detection,tb_incidence_graph]:
        fig.update_layout(template=current_template)
    return tb_prevalence_chart,prevalence_map,tb_mortality_chart_nohiv,tb_mortality_chart_hiv,tb_death_chart_nohiv,tb_death_chart_hiv,tb_case_detection,tb_incidence_graph

if __name__=="__main__":
    app.run(debug=True)