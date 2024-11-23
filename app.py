import streamlit as st
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

try:
    with st.spinner('Processing data... Please wait!'):
        filepath = "data/*.csv"
        combined_df = combine_data(filepath)
        maindf = process_data(combined_df)


    visuals = create_all_visuals(maindf)


    tabs = st.tabs(["Page 1", "Page 2", "Page 3"])

    with tabs[0]:
        st.plotly_chart(visuals[0], use_container_width=True)
        st.plotly_chart(visuals[1], use_container_width=True)
        st.plotly_chart(visuals[2], use_container_width=True)

    with tabs[1]:
        st.plotly_chart(visuals[3], use_container_width=True)
        st.plotly_chart(visuals[4], use_container_width=True)
        st.plotly_chart(visuals[5], use_container_width=True)

    with tabs[2]:
        st.plotly_chart(visuals[6], use_container_width=True)
        st.plotly_chart(visuals[7], use_container_width=True)
        st.plotly_chart(visuals[8], use_container_width=True)

except Exception as e:
    st.error("Error! Reload the page.")

