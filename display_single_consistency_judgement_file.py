import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import sys

def main():
    # Load data from the JSONL file
    data_file = './Data/Output/consistency_judgements/3v_big_c_test_aya_8b_vs_gpt_4o.jsonl'

    # Check if the file exists
    if not os.path.isfile(data_file):
        messagebox.showerror("File Not Found", f"The file {data_file} does not exist.")
        sys.exit(1)

    try:
        df = pd.read_json(data_file, lines=True)
    except ValueError as e:
        messagebox.showerror("Data Load Error", f"Unable to read JSON data:\n{e}")
        sys.exit(1)
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred:\n{e}")
        sys.exit(1)

    # Define the judgment column
    judgment_column = 'gpt_4o_consistency_judgment'
    if judgment_column not in df.columns:
        messagebox.showerror("Column Error", f"No judgment column '{judgment_column}' found in the data.")
        sys.exit(1)

    # Get v1_model and v2_model from the DataFrame
    v1_models = df['v1_model'].unique()
    v2_models = df['v2_model'].unique()

    # Assuming v1_model and v2_model are consistent, get the first value
    v1_model = v1_models[0] if len(v1_models) > 0 else 'N/A'
    v2_model = v2_models[0] if len(v2_models) > 0 else 'N/A'

    # Translation columns for each model
    v1_translation_v1 = f"{v1_model}_translation_t1"
    v1_translation_v2 = f"{v1_model}_translation_t2"
    v2_translation_v1 = f"{v2_model}_translation_t1"
    v2_translation_v2 = f"{v2_model}_translation_t2"

    # Check if the columns exist
    required_columns = [
        v1_translation_v1, v1_translation_v2,
        v2_translation_v1, v2_translation_v2,
        'joined_bemba_sentences', 'joined_english_sentences',
        'full_consistency_judgment_prompt'
    ]
    for col in required_columns:
        if col not in df.columns:
            messagebox.showerror("Column Error", f"The expected column '{col}' does not exist in the data.")
            sys.exit(1)

    # Compute judgment counts
    count_model_1 = (df[judgment_column] == v1_model).sum()
    count_model_2 = (df[judgment_column] == v2_model).sum()
    count_equal = len(df) - count_model_1 - count_model_2

    # Define columns to display in the Treeview
    display_columns = [
        'id',
        judgment_column,
        'v1_model',
        'v2_model'
    ]

    # Replace NaN values with empty strings
    df.fillna('', inplace=True)

    # Create Tkinter window
    root = tk.Tk()
    root.title("Consistency Judgment Results")

    # Set window size
    root.geometry("800x600")

    # Create a frame for the summary
    summary_frame = ttk.Frame(root, padding="10")
    summary_frame.pack(side=tk.TOP, fill=tk.X)

    # Display summary including model names and counts
    summary_text = (
        f"Model 1: {v1_model}\n"
        f"Model 2: {v2_model}\n\n"
        f"Consistency Judgments:\n"
        f"{v1_model} judged more consistent: {count_model_1}\n"
        f"{v2_model} judged more consistent: {count_model_2}\n"
        f"Both equally consistent or other: {count_equal}\n"
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
        'v1_model': 'Model 1',
        'v2_model': 'Model 2'
    }

    # Adjust column widths
    column_widths = {
        'id': 50,
        judgment_column: 150,
        'v1_model': 150,
        'v2_model': 150
    }

    for col in display_columns:
        tree.heading(col, text=column_headings[col])
        tree.column(col, anchor=tk.CENTER, width=column_widths.get(col, 150))

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
        detail_text = f"ID: {row['id']}\n"
        detail_text += f"Judgment: {row[judgment_column]}\n"
        detail_text += f"Model 1: {row['v1_model']}\n"
        detail_text += f"Model 2: {row['v2_model']}\n\n"

        detail_text += f"Original Bemba Conversation:\n{row['joined_bemba_sentences']}\n\n"
        detail_text += f"Original English Conversation:\n{row['joined_english_sentences']}\n\n"
        detail_text += f"{v1_model} Translation 1:\n{row[v1_translation_v1]}\n\n"
        detail_text += f"{v1_model} Translation 2:\n{row[v1_translation_v2]}\n\n"
        detail_text += f"{v2_model} Translation 1:\n{row[v2_translation_v1]}\n\n"
        detail_text += f"{v2_model} Translation 2:\n{row[v2_translation_v2]}\n\n"
        detail_text += f"Full Consistency Judgment Prompt:\n{row['full_consistency_judgment_prompt']}\n\n"
        detail_text += f"{judgment_column}:\n{row[judgment_column]}\n"

        text.insert('1.0', detail_text)
        text.config(state='disabled')

    # Bind the treeview select event to the show_details function
    tree.bind('<<TreeviewSelect>>', show_details)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
