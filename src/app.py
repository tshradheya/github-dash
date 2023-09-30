from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import requests

app = Dash(__name__)
YOUR_TOKEN = "" # Add your token here

headers = {
    "Accept": "application/vnd.github.star+json",
    "Authorization": f"Bearer {YOUR_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28"
}


app.layout = html.Div(
    [
        dcc.Input(
            id ="repo-url",
            style={"width": "50%", "margin": "auto", "display": "flex", "margin-top": "10%"},
            type="url",
            placeholder="Enter Github Repo URL (https://github.com/tshradheya/bun-playground)"
        ),
        html.Div(id='my-output'),
        dcc.Graph(id='graph-content'),
        dcc.Graph(id='graph-content-contributor')
    ]
)

def get_stargazers(repo_url, page):
    url = f"https://api.github.com/repos/{repo_url}/stargazers?page={page}&per_page=100"
    response = requests.get(url, headers=headers)

    agg = []
    if response.status_code == 200 :
        for i in response.json():
            agg.append({
                "date": i["starred_at"].split("T")[0],
                "count": 1
            })
        return agg
    else:
        return None

def get_forks(repo_url, page):
    url = f"https://api.github.com/repos/{repo_url}/forks?page={page}&per_page=100"
    response = requests.get(url, headers=headers)

    agg = []
    if response.status_code == 200 :
        for i in response.json():
            agg.append({
                "date": i["created_at"].split("T")[0],
                "count": 1
            })
        return agg
    else:
        return None

@callback(
    Output('graph-content', 'figure'),
    Input('repo-url', 'value')
)
def update_graph(value):
    final_vals = []
    idx = 1
    go_on = True
    while(go_on):
        temp = get_stargazers(value, idx)
        if temp is None:
            go_on = False
        elif len(temp) < 100:
            final_vals.extend(temp)
            go_on = False
        else:
            final_vals.extend(temp)
            idx += 1
    if len(final_vals) > 0:
        df = pd.DataFrame(final_vals)
        df1 = df.groupby("date").sum().reset_index()
        return px.line(df1, x="date", y="count", title=f"Stargazers for {value}")
    else:
        df = pd.DataFrame(final_vals)
        return px.line(df1, x="date", y="count", title=f"Stargazers for {value}")

@callback(
    Output('graph-content-contributor', 'figure'),
    Input('repo-url', 'value')
)
def update_graph_forks(value):
    final_vals = []
    idx = 1
    go_on = True
    while(go_on):
        temp = get_forks(value, idx)
        if temp is None:
            go_on = False
        elif len(temp) < 100:
            final_vals.extend(temp)
            go_on = False
        else:
            final_vals.extend(temp)
            idx += 1
    if len(final_vals) > 0:
        df = pd.DataFrame(final_vals)
        df1 = df.groupby("date").sum().reset_index()
        return px.bar(df1, x="date", y="count", title=f"Contributor start for {value}")
    else:
        df = pd.DataFrame(final_vals)
        return px.bar(df1, x="date", y="count", title=f"Contributor start for {value}")



if __name__ == '__main__':
    app.run(debug=True)