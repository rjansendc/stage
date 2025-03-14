import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_choir_stage(df_choir):
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
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Scatter plot for choir members
    for _, row in df_choir.iterrows():
        x = row["Stage Column"]
        y = row["Stage Row"]
        color = voice_colors.get(row["Section"], "black")  # Default to black if unknown section

        # Plot point
        ax.scatter(x, y, color=color, s=200, edgecolors="black", alpha=0.7)

        # Annotate with initials
        initials = f"{row['Name'].split()[0][0]}{row['Name'].split()[-1][0]}"  # First and last initial
        label_offset = -0.1 if y == 3 else 0.2  # Move labels above only for bottom row
        ax.text(x, y + label_offset, initials, ha="center", fontsize=10, fontweight='bold')
    
    # Set labels and title
    ax.set_xlabel("Stage Columns")
    ax.set_ylabel("Stage Rows (Back = Higher)")
    ax.set_title("Choir Stage Layout Visualization")
    
    # Reverse y-axis so back row is at the top
    ax.invert_yaxis()
    
    # Show legend for voice parts
    legend_labels = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=c, markersize=10) for c in voice_colors.values()]
    ax.legend(legend_labels, voice_colors.keys(), title="Voice Part", loc="upper right")
    
    # Show the plot
    plt.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig)

# Streamlit App
st.title("🎶 Choir Stage Visualization")

uploaded_file = st.file_uploader("Upload Choir Excel File", type=["xlsm", "xlsx"])

if uploaded_file:
    df_choir = pd.read_excel(uploaded_file, sheet_name="Choir List")
    plot_choir_stage(df_choir)
