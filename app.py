# app.py

import plotly.graph_objects as go
from dash import Dash, dcc, html
from simulation import run_simulation
import networkx as nx  # For network visualizations

def visualize_blockchain(blockchain):
    G = nx.DiGraph()
    labels = {}

    # Add nodes and edges
    for block in blockchain.chain:
        index = block.index
        G.add_node(index)
        labels[index] = f"Block {index}\nHash: {block.hash()[:6]}..."
        if index > 0:
            G.add_edge(index - 1, index)

    # Layout
    pos = nx.spring_layout(G)

    # Edges
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='gray'),
        hoverinfo='none',
        mode='lines')

    # Nodes
    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(labels[node])

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="bottom center",
        hoverinfo='text',
        marker=dict(
            color='skyblue',
            size=50,
            line_width=2))

    # Figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Blockchain Structure',
                        showlegend=False,
                        hovermode='closest'))
    return fig

def visualize_entity_network(products):
    G = nx.MultiDiGraph()
    for product in products.values():
        history = product.get_history()
        for i in range(len(history) - 1):
            source = history[i]['updated_by']
            target = history[i+1]['updated_by']
            G.add_edge(source, target, product=product.product_id)

    pos = nx.spring_layout(G)

    # Edges
    edge_traces = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_traces.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            line=dict(width=1, color='gray'),
            hoverinfo='text',
            mode='lines',
            text=f"Product: {edge[2]['product']}"))

    # Nodes
    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            color='lightgreen',
            size=10,
            line_width=2))

    # Figure
    fig = go.Figure(data=edge_traces + [node_trace],
                    layout=go.Layout(
                        title='Network of Entities',
                        showlegend=False,
                        hovermode='closest'))
    return fig

def visualize_product_flow(products):
    sources = []
    targets = []
    values = []
    label_list = []

    for product in products.values():
        history = product.get_history()
        for i in range(len(history) - 1):
            source = history[i]['updated_by']
            target = history[i+1]['updated_by']
            if source not in label_list:
                label_list.append(source)
            if target not in label_list:
                label_list.append(target)
            sources.append(label_list.index(source))
            targets.append(label_list.index(target))
            values.append(1)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            label=label_list,
            color="blue"),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color="lightblue"))])

    fig.update_layout(title_text="Product Flow Through Entities", font_size=10)
    return fig

# Run the simulation and get data
scm = run_simulation()
products = scm.products
blockchain = scm.blockchain

# Initialize the Dash app
app = Dash(__name__)

# Define the layout with tabs
app.layout = html.Div([
    html.H1("Supply Chain Simulation Dashboard"),
    dcc.Tabs([
        dcc.Tab(label='Product Flow', children=[
            dcc.Graph(figure=visualize_product_flow(products))
        ]),
        dcc.Tab(label='Blockchain Structure', children=[
            dcc.Graph(figure=visualize_blockchain(blockchain))
        ]),
        dcc.Tab(label='Network of Entities', children=[
            dcc.Graph(figure=visualize_entity_network(products))
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)