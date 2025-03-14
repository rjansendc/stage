import streamlit as st
import pandas as pd
import plotly.express as px
import math

def assign_rows_and_columns(df_choir, num_rows):
    """Dynamically assign rows and columns based on height and number of rows."""
    df_choir = df_choir.sort_values(by="Height (in)", ascending=True).reset_index(drop=True)
    
    num_people = len(df_choir)
    row_counts = [math.ceil(num_people * (1 / num_rows)) for _ in range(num_rows - 1)]
    row_counts.append(num_people - sum(row_counts))  # Assign remainder to the front row
    
    row_assignments = []
    col_assignments = []
    current_index = 0
    
    for row in range(1, num_rows + 1):
        row_size = row_counts[row - 1]
        for col in range(1, row_size + 1):
            row_assignments.append(row)
            col_assignments.append(col)
            current_index += 1
    
    df_choir["Row"] = row_assignments
    df_choir["Column"] = col_assignments
    return df_choir

def plot_stage(df_choir, num_rows):
    
    # Save updated positioning to an Excel file
    output = "Choir_Positioning.xlsx"
    df_choir.to_excel(output, index=False)
    st.download_button(label="Download Updated Positioning", data=open(output, "rb").read(), file_name=output, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
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
        title=f"Choir Stage Layout ({num_rows} Rows)",
        xaxis_title="Stage Columns",
        yaxis_title="Stage Rows (Front = 1, Back = {num_rows})",
        yaxis=dict(autorange="reversed", tickmode='array', 
                   tickvals=list(range(1, num_rows + 1)), 
                   ticktext=[f"Row {i}" for i in range(1, num_rows + 1)]),
        showlegend=True
    )
    
    st.plotly_chart(fig)

# Streamlit App
st.title("🎶 Choir Stage Dynamic Visualization")

num_rows = st.slider("Select Number of Rows", min_value=2, max_value=4, value=3)

uploaded_file = st.file_uploader("Upload Choir Excel File", type=["xlsm", "xlsx"])

if uploaded_file:
    df_choir = pd.read_excel(uploaded_file, sheet_name="Choir List")
    df_choir = assign_rows_and_columns(df_choir, num_rows)
    plot_stage(df_choir, num_rows)
