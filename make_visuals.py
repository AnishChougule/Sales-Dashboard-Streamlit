import os
from data_processing import combine_data, process_data
from data_visualization import create_all_visuals

filepath = "data/*.csv"

def process_and_save_visualizations(filepath):
    try:

        combined_df = combine_data(filepath)
        maindf = process_data(combined_df)

        visuals = create_all_visuals(maindf)
        fig_names = ['fig1', 'fig2', 'fig3', 'fig4', 'fig5', 'fig6', 'fig7', 'fig8', 'fig9']
        
        if not os.path.exists('static/visuals'):
            os.makedirs('static/visuals')

        for i, fig in enumerate(visuals):
            fig.write_html(f'static/visuals/{fig_names[i]}.html', auto_open=False)

        print("Data processed and visualizations saved successfully.")
        
    except Exception as e:
        print(f"Error during processing: {e}")

if __name__ == "__main__":
    process_and_save_visualizations(filepath)
