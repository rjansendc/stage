import streamlit as st
import openpyxl
import pandas as pd
import plotly.express as px
import math



def plot_stage(df_choir):
    
    
    """Plot choir stage layout based on dynamically assigned row and column positioning."""
    voice_colors = {
        "Soprano": "red",
        "Alto": "blue",
        "Tenor": "green",
        "Bass": "purple"
    }
    
    df_choir["Color"] = df_choir["Section"].map(voice_colors)
    
    fig = px.scatter(df_choir, x="Column", y="Row", 
                     color="Section", color_discrete_map=voice_colors, 
                     hover_name="Name", size_max=20)
    
    fig.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))
    
    fig.update_layout(
        title="Choir Stage Layout",
        xaxis_title="Stage Columns",
        yaxis_title="Stage Rows (Front = 1, Back = Max)",
        yaxis=dict(autorange="reversed", tickmode='array', 
                   tickvals=sorted(df_choir['Row'].unique(), reverse=True), 
                   ticktext=[f"Row {i}" for i in sorted(df_choir['Row'].unique(), reverse=True)]),
        showlegend=True
    )
    
    st.plotly_chart(fig)

# Streamlit App
st.title("🎶 Choir Stage Dynamic Visualization")



uploaded_file = st.file_uploader("Upload Choir Positioning File", type=["xlsx"])

if uploaded_file:
    df_choir = pd.read_excel(uploaded_file)
    
    plot_stage(df_choir)
