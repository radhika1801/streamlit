import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot_predictions(predictions, title=""):
    """Create ultra-minimal bar chart"""
    labels = [p['label'].replace('_', ' ').title() for p in predictions]
    scores = [p['score'] for p in predictions]
    
    fig = go.Figure(data=[
        go.Bar(
            x=scores,
            y=labels,
            orientation='h',
            marker=dict(
                color='#0a0a0a',
                line=dict(width=0)
            ),
            text=[f"{s:.1%}" for s in scores],
            textposition='outside',
            textfont=dict(
                size=11, 
                color='#6a6a6a',
                family='Space Mono, monospace'
            ),
        )
    ])
    
    fig.update_layout(
        title=title,
        title_font=dict(
            size=14, 
            color='#0a0a0a', 
            family='Outfit, sans-serif',
            weight=300
        ),
        xaxis_title="",
        yaxis_title="",
        height=max(280, len(predictions) * 55),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(
                size=11, 
                color='#2a2a2a',
                family='Outfit, sans-serif'
            )
        ),
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            range=[0, max(scores) * 1.18]
        ),
        plot_bgcolor='rgba(250,250,250,0.3)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=80, t=30, b=10),
        showlegend=False
    )
    
    return fig

def plot_comparison(results_dict):
    """Compare multiple model outputs"""
    df_data = []
    for model_name, predictions in results_dict.items():
        for pred in predictions:
            df_data.append({
                'Model': model_name,
                'Label': pred['label'],
                'Score': pred['score']
            })
    
    df = pd.DataFrame(df_data)
    
    fig = px.bar(
        df,
        x='Score',
        y='Label',
        color='Model',
        barmode='group',
        orientation='h',
        color_discrete_sequence=['#0a0a0a', '#4a4a4a', '#8a8a8a']
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Outfit, sans-serif', color='#2a2a2a')
    )
    
    return fig

def create_confidence_gauge(confidence):
    """Minimal confidence gauge"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={
            'suffix': "%", 
            'font': {
                'size': 48, 
                'color': '#0a0a0a',
                'family': 'Outfit, sans-serif',
                'weight': 200
            }
        },
        gauge={
            'axis': {
                'range': [None, 100], 
                'tickwidth': 0,
                'tickcolor': "white"
            },
            'bar': {'color': "#0a0a0a", 'thickness': 0.25},
            'bgcolor': "#fafafa",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 100], 'color': '#f0f0f0'}
            ],
        }
    ))
    
    fig.update_layout(
        height=240,
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Outfit, sans-serif')
    )
    
    return fig