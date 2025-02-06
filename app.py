import streamlit as st
import glob
from data_processing import combine_data, process_data
from data_visualization import create_all_visuals


st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.markdown("""
    <style>
        /* Warning displayed only on small screens */
        @media screen and (min-width: 800px) {
            .mobile-warning {
                display: none; /* Hide on desktop */
            }
        }
        @media screen and (max-width: 799px) {
            .mobile-warning {
                display: block; /* Show on mobile */
                text-align: center;
                background-color: #ffcccb;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 20px;
                font-size: 16px;
                color: black;
                font-weight: bold;
            }
        }
    </style>
    <div class="mobile-warning">
        <strong>Note:</strong> This website is optimized for desktop view.
    </div>
""", unsafe_allow_html=True)


st.title("Sales Dashboard")
st.markdown("This is a data analysis and visualization project.")

visuals_files = glob.glob("static/visuals/*.html")

@st.cache_data
def load_visuals(files):
    visuals_html = []
    for file in files:
        try:
            with open(file, "r") as f:
                visuals_html.append(f.read())
        except Exception as e:
            st.error(f"Error reading {file}: {e}")
    return visuals_html

try:
        visuals_html = load_visuals(visuals_files)
        for visual in visuals_html:
            st.components.v1.html(visual, height=900)
except Exception as e:
    st.error(f"Error! Reload the page. Details: {e}")
