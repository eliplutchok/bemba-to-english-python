import pandas as pd
import tkinter as tk
from tkinter import ttk

def main():
    # Load data from the JSONL file
    data_file = './Data/Output/judgments/v2_big_c_test_gpt_4o_vs_sonnet_3_point_5.jsonl'
    df = pd.read_json(data_file, lines=True)

    # Identify judgment column
    judgment_column = 'gpt_4o_judgment'
    if judgment_column not in df.columns:
        raise ValueError(f"No judgment column '{judgment_column}' found in the data.")

    # Get v1_model and v2_model from the DataFrame
    v1_models = df['v1_model'].unique()
    v2_models = df['v2_model'].unique()

    # Assuming v1_model and v2_model are consistent, get the first value
    v1_model = v1_models[0] if len(v1_models) > 0 else 'N/A'
    v2_model = v2_models[0] if len(v2_models) > 0 else 'N/A'

    # Model output columns
    v1_output_column = f"{v1_model}_translation"
    v2_output_column = f"{v2_model}_translation"

    # Check if the columns exist
    for col in [v1_output_column, v2_output_column]:
        if col not in df.columns:
            raise ValueError(f"The expected model output column '{col}' does not exist in the data.")

    # Compute judgment counts
    count_v1 = (df[judgment_column] == v1_model).sum()
    count_v2 = (df[judgment_column] == v2_model).sum()

    # Check for similarity score columns
    similarity_columns = [
        f'{v1_model}_similarity_score',
        f'{v2_model}_similarity_score',
        'similarity_score_winner'
    ]
    similarity_columns_present = all(col in df.columns for col in similarity_columns)

    # Initialize similarity stats
    if similarity_columns_present:
        # Compute average similarity scores
        avg_similarity_v1 = df[f'{v1_model}_similarity_score'].mean()
        avg_similarity_v2 = df[f'{v2_model}_similarity_score'].mean()

        # Compute winner counts
        similarity_winner_counts = df['similarity_score_winner'].value_counts()
        similarity_winner_v1 = similarity_winner_counts.get(v1_model, 0)
        similarity_winner_v2 = similarity_winner_counts.get(v2_model, 0)
    else:
        avg_similarity_v1 = avg_similarity_v2 = None
        similarity_winner_v1 = similarity_winner_v2 = None

    # Define columns to display in the Treeview
    display_columns = [
        'id',
        judgment_column,
        'v1_model',
        'v2_model',
    ]
    if similarity_columns_present:
        display_columns.extend(similarity_columns)

    # Replace NaN values with empty strings
    df.fillna('', inplace=True)

    # Create Tkinter window
    root = tk.Tk()
    root.title("Judgment Results")

    # Set window size
    root.geometry("900x600")

    # Create a frame for the summary
    summary_frame = ttk.Frame(root, padding="10")
    summary_frame.pack(side=tk.TOP, fill=tk.X)

    # Display summary including model names and counts
    summary_text = (
        f"V1 Model: {v1_model}\n"
        f"V2 Model: {v2_model}\n\n"
        f"Total Judgments:\n"
        f"{v1_model}: {count_v1}\n"
        f"{v2_model}: {count_v2}\n"
    )
    if similarity_columns_present:
        summary_text += (
            f"\nAverage Similarity Scores:\n"
            f"{v1_model}: {avg_similarity_v1:.4f}\n"
            f"{v2_model}: {avg_similarity_v2:.4f}\n\n"
            f"Similarity Score Winner Counts:\n"
            f"{v1_model}: {similarity_winner_v1}\n"
            f"{v2_model}: {similarity_winner_v2}\n"
        )

    summary_label = ttk.Label(summary_frame, text=summary_text, font=("Arial", 12))
    summary_label.pack(side=tk.LEFT)

    # Create a frame for the table
    table_frame = ttk.Frame(root)
    table_frame.pack(fill=tk.BOTH, expand=True)

    # Create a Treeview widget
    tree = ttk.Treeview(table_frame, columns=display_columns, show='headings')

    # Define column headings with model labels
    column_headings = {
        'id': 'ID',
        judgment_column: 'Judgment',
        'v1_model': 'V1 Model',
        'v2_model': 'V2 Model',
        f'{v1_model}_similarity_score': f"{v1_model} Similarity Score",
        f'{v2_model}_similarity_score': f"{v2_model} Similarity Score",
        'similarity_score_winner': 'Similarity Winner'
    }

    # Adjust column widths
    column_widths = {
        'id': 50,
        judgment_column: 100,
        'v1_model': 120,
        'v2_model': 120,
        f'{v1_model}_similarity_score': 150,
        f'{v2_model}_similarity_score': 150,
        'similarity_score_winner': 130
    }

    for col in display_columns:
        tree.heading(col, text=column_headings.get(col, col))
        tree.column(col, anchor=tk.CENTER, width=column_widths.get(col, 100))

    # Insert data into the Treeview
    for index, row in df.iterrows():
        values = [str(row[col]) for col in display_columns]
        tree.insert("", tk.END, iid=index, values=values)

    # Add a vertical scrollbar to the Treeview
    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    tree.pack(fill=tk.BOTH, expand=True)

    # Define a function to show details when a row is selected
    def show_details(event):
        selected_item = tree.focus()
        if not selected_item:
            return

        index = int(selected_item)
        row = df.iloc[index]

        detail_window = tk.Toplevel(root)
        detail_window.title(f"Details for ID {row['id']}")
        detail_window.geometry("800x600")

        text = tk.Text(detail_window, wrap='word')
        text.pack(fill='both', expand=True)

        # Prepare the detail text
        detail_text = f"**ID:** {row['id']}\n"
        detail_text += f"**Judgment:** {row[judgment_column]}\n"
        detail_text += f"**V1 Model:** {row['v1_model']}\n"
        detail_text += f"**V2 Model:** {row['v2_model']}\n\n"

        if similarity_columns_present:
            detail_text += f"**{v1_model} Similarity Score:** {row[f'{v1_model}_similarity_score']}\n"
            detail_text += f"**{v2_model} Similarity Score:** {row[f'{v2_model}_similarity_score']}\n"
            detail_text += f"**Similarity Winner:** {row['similarity_score_winner']}\n\n"

        detail_text += f"**Original Conversation:**\n{row['joined_english_sentences']}\n\n"
        detail_text += f"**{v1_model} Translation:**\n{row[v1_output_column]}\n\n"
        detail_text += f"**{v2_model} Translation:**\n{row[v2_output_column]}\n\n"
        detail_text += f"**Full Judgment Prompt:**\n{row['full_judgment_prompt']}\n\n"
        detail_text += f"**{judgment_column}:**\n{row[judgment_column]}\n"

        text.insert('1.0', detail_text)
        text.config(state='disabled')

    # Bind the treeview select event to the show_details function
    tree.bind('<<TreeviewSelect>>', show_details)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
