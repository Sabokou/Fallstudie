# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# from app import app
# import pickle
# import numpy as np

# layout = html.Div([
#     html.H1("Jungbank Verkaufstool", className="title"),

#     html.Div(id="tool_select", children=[
#         dcc.Dropdown(id="select_age",
#         options=[
#             {"label":"18 - 29", "value": 1},
#             {"label":"30 - 49", "value": 2},
#             {"label":"50 - 65", "value": 3},
#             {"label":"65+", "value": 4}
#         ]),

#         dcc.Dropdown(id="select_income",
#         options=[
#             {"label":"<0", "value": 1},
#             {"label":"0 - 19999", "value": 2},
#             {"label":"20000 - 39999", "value": 3},
#             {"label":"40000 - 59999", "value": 4},
#             {"label":"60000 - 79999", "value": 5},
#             {"label":"80000 - 99999", "value": 6},
#             {"label":"100000+", "value": 7}
#         ]),

#         dcc.Dropdown(id="select_sex",
#         options=[
#             {"label":"Männlich", "value": 1},
#             {"label":"Weiblich", "value": 2},
#             {"label":"Divers", "value": 3}
#         ]),

#         dcc.Dropdown(id="select_children",
#         options=[
#             {"label":"Ja", "value": 0},
#             {"label":"Nein", "value": 1}
#         ]),

#         dcc.Dropdown(id="select_marital",
#         options=[
#             {"label":"verheiratet", "value": 1},
#             {"label":"ledig", "value": 2},
#             {"label":"aufgelöste Beziehung", "value": 3}
#         ]),

#         dcc.Dropdown(id="select_job",
#         options=[
#             {"label":"Studium", "value": 0},
#             {"label":"Öffentlicher Dienst", "value": 1},
#             {"label":"Rente", "value": 2},
#             {"label":"Informatik", "value": 3},
#             {"label":"Handel", "value": 4},
#             {"label":"Handwerk", "value": 5},
#             {"label":"Administrativ", "value": 6},
#             {"label":"Ingenieurswesen", "value": 7},
#             {"label":"Management", "value": 8},
#             {"label":"Arbeitslos", "value": 9}

#         ])
#     ]),
#     html.Div(id="tool_output", children=[
#         html.Div(id="output1"),
#         html.Div(id="output2"),
#         html.Div(id="output3")


#     ])




# ])

# model = pickle.load(open("jungbank_xgb.sav", 'rb'))

# @app.callback(
#      [Output(component_id="output1", component_property="children"),
#      Output(component_id="output2", component_property="children"),
#      Output(component_id="output3", component_property="children")],
#      [Input(component_id="select_sex", component_property="value"),
#      Input(component_id="select_job", component_property="value"),
#      Input(component_id="select_marital", component_property="value"),
#      Input(component_id="select_children", component_property="value"),
#      Input(component_id="select_age", component_property="value"),
#      Input(component_id="select_income", component_property="value")]
# )
# def vorschlag(sex_value, job_value, marital_value, children_value, age_value, income_value):
    
#     kunde = [[sex_value,job_value,marital_value,children_value,age_value,income_value,0]]
#     kunde = np.array(kunde).reshape((1,-1))
    
#     kunde[0][6] = 1
#     prob1 = model.predict_proba(kunde)[0][1]
    
#     kunde[0][6] = 2
#     prob2 = model.predict_proba(kunde)[0][1]
    
#     kunde[0][6] = 3
#     prob3 = model.predict_proba(kunde)[0][1]
    
#     kunde[0][6] = 4
#     prob4 = model.predict_proba(kunde)[0][1]
    
#     kunde[0][6] = 5
#     prob5 = model.predict_proba(kunde)[0][1]
    
#     kunde[0][6] = 6
#     prob6 = model.predict_proba(kunde)[0][1]
    
#     kunde[0][6] = 7
#     prob7 = model.predict_proba(kunde)[0][1]
    
#     produkt = {"Girokonto":prob1,"Kredit":prob2, "Tagesgeldkonto":prob3, "Depotkonto":prob4, "Altersvorsorge":prob5, "Versicherung":prob6, "Bausparvertrag":prob7}

#     out1 = (f"1. {sorted(produkt, key=produkt.get, reverse=True)[:3][0]} mit {round((produkt.get(sorted(produkt, key=produkt.get, reverse=True)[:3][0])*100),2)}% Erfolgschance")
#     out2 = (f"2. {sorted(produkt, key=produkt.get, reverse=True)[:3][1]} mit {round((produkt.get(sorted(produkt, key=produkt.get, reverse=True)[:3][1])*100),2)}% Erfolgschance")
#     out3 = (f"3. {sorted(produkt, key=produkt.get, reverse=True)[:3][2]} mit {round((produkt.get(sorted(produkt, key=produkt.get, reverse=True)[:3][2])*100),2)}% Erfolgschance")

#     return out1, out2, out3



