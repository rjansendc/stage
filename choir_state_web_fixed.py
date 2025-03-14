import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
import plotly.express as px

def parse_xml(file):
    """Parse XML file containing choir member positioning information."""
    tree = ET.parse(file)
    root = tree.getroot()
    
    data = []
    for member in root.findall(".//member"):
        name = member.find("name").text
        section = member.find("section").text
        row = int(member.find("row").text)
        column = int(member.find("column").text)
        data.append({"Name": name, "Section": section, "Stage Row": row, "Stage Column": column})
    
    return pd.DataFrame(data)

def plot_fixed_stage(df_choir):
    """Plot choir stage layout based on fixed positioning."""
    voice_colors = {
        "Soprano": "red",
        "Alto": "blue",
        "Tenor": "green",
        "Bass": "purple"
    }
    
    df_choir["Color"] = df_choir["Section"].map(voice_colors)
    
    fig = px.scatter(df_choir, x="Stage Column", y="Stage Row", 
                     color="Section", color_discrete_map=voice_colors, 
                     hover_name="Name", size_max=20)
    
    fig.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))
    
    fig.update_layout(
        title="Choir Stage Layout (Fixed Positioning)",
        xaxis_title="Stage Columns",
        yaxis_title="Stage Rows (Back = Higher)",
        yaxis=dict(autorange="reversed"),
        showlegend=True
    )
    
    st.plotly_chart(fig)

# Streamlit App
st.title("🎶 Choir Stage Fixed Visualization")

uploaded_file = st.file_uploader("Upload Choir Excel File", type=["xlsm", "xlsx"])

if uploaded_file:
    df_choir = pd.read_excel(uploaded_file, sheet_name="Positioning")
    plot_fixed_stage(df_choir)
