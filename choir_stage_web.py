import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_choir_stage(df_choir):
    import plotly.express as px
    
    # Define colors for voice parts
    voice_colors = {
        "Soprano": "red",
        "Alto": "blue",
        "Tenor": "green",
        "Bass": "purple"
    }
    
    # Sort by height (assuming taller in the back)
    df_choir = df_choir.sort_values(by="Row", ascending=True)
    
    # Define row distribution (Back row has 2 more than middle, middle has 2 more than front)
    num_back = (len(df_choir) // 3) + 2
    num_middle = (len(df_choir) // 3)
    num_front = len(df_choir) - (num_back + num_middle)
    
    row_labels = ([3] * num_back) + ([2] * num_middle) + ([1] * num_front)
    df_choir["Stage Row"] = row_labels
    
    # Assign column positions evenly per row
    df_choir["Stage Column"] = [i % num_back + 1 if row == 3 else i % num_middle + 1 if row == 2 else i % num_front + 1 
                                 for i, row in enumerate(df_choir["Stage Row"]) ]
    
    # Convert color mapping for Plotly
    df_choir["Color"] = df_choir["Section"].map(voice_colors)
    
    # Create interactive plot using Plotly
    fig = px.scatter(df_choir, x="Stage Column", y="Stage Row", 
                     color="Section", color_discrete_map=voice_colors, 
                     hover_name="Name", size_max=20)
    
    fig.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))
    
    fig.update_layout(
        title="Choir Stage Layout Visualization",
        xaxis_title="Stage Columns",
        yaxis_title="Stage Rows (Back = Higher)",
        yaxis=dict(autorange="reversed"),
        showlegend=True
    )
    
    st.plotly_chart(fig)

# Streamlit App
st.title("🎶 Choir Stage Visualization")

uploaded_file = st.file_uploader("Upload Choir Excel File", type=["xlsm", "xlsx"])

if uploaded_file:
    df_choir = pd.read_excel(uploaded_file, sheet_name="Choir List")
    plot_choir_stage(df_choir)
