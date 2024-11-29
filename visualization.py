#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import plotly.figure_factory as ff
import plotly.graph_objects as go
import networkx as nx


def generate_gantt_chart(products):
    df = []
    for product in products.values():
        for event in product.get_history():
            df.append({
                'Task': product.product_id,
                'Start': event['date'],
                'Finish': event['date'],
                'Resource': event['status']
            })
    fig = ff.create_gantt(df, index_col='Resource', show_colorbar=True, group_tasks=True)
    return fig


def visualize_blockchain(blockchain):
    G = nx.DiGraph()
    for block in blockchain.chain:
        G.add_node(block.index, label=f"Block {block.index}\nHash: {block.hash()[:6]}...")
        if block.index > 0:
            G.add_edge(block.index - 1, block.index)

    pos = nx.spring_layout(G)
    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='lightblue'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_labels = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_labels.append(G.nodes[node]['label'])

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_labels,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            size=10,
            color='blue'))

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Blockchain Structure',
                        showlegend=False))
    return fig


def visualize_entity_network(products):
    G = nx.DiGraph()
    for product in products.values():
        history = product.get_history()
        for i in range(len(history) - 1):
            G.add_edge(history[i]['updated_by'], history[i + 1]['updated_by'], product=product.product_id)

    pos = nx.spring_layout(G)
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=1, color='grey'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            color='lightgreen',
            size=10,
            line_width=2))

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += [x]
        node_trace['y'] += [y]
        node_trace['text'] += [node]

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Entity Interaction Network',
                        showlegend=False))
    return fig

