import pandas as pd
import json
import asyncio
import os

full_judgment_prompt = """
You will be given a short conversation in English between two speakers. Conversant A always begins with a description of an image they are viewing.

You will also receive two alternate versions of the same conversation: **Alternate Version 1** and **Alternate Version 2**.

Your task is to judge which alternate version is closer in meaning to the original conversation.

Respond with **1**, **2**, or **3**:
- **1** if **Alternate Version 1** is closer in meaning to the original conversation.
- **2** if **Alternate Version 2** is closer in meaning to the original conversation.
- **3** if both are equally close in meaning to the original conversation (either both good or both bad).

**Just respond with the number. Do not include any other text.**

---

**Original Conversation:**
{conversation}

**Alternate Version 1:**
{alternate_version_1}

**Alternate Version 2:**
{alternate_version_2}

**Your response:**
""" 

def prepare_judgment_file(
        v1_model,
        v2_model,
        input_version_name=None,
        output_version_name=None
    ):
    if input_version_name is None:
        v1_jsonl_path = f"./Data/Output/translations/big_c_conversations_test_{v1_model}.jsonl"
        v2_jsonl_path = f"./Data/Output/translations/big_c_conversations_test_{v2_model}.jsonl"
    else:
        v1_jsonl_path = f"./Data/Output/translations/{input_version_name}_big_c_conversations_test_{v1_model}.jsonl"
        v2_jsonl_path = f"./Data/Output/translations/{input_version_name}_big_c_conversations_test_{v2_model}.jsonl"

    # Read JSONL files
    df_1 = pd.read_json(v1_jsonl_path, lines=True)
    df_2 = pd.read_json(v2_jsonl_path, lines=True)

    # Ensure 'id' is included in the columns to use from df_2
    columns_to_use_from_df2 = [
        col for col in df_2.columns
        if col == 'id' or col not in df_1.columns or col == f'{v2_model}_translation'
    ]

    # Subset df_2 to include only necessary columns
    df_2_subset = df_2[columns_to_use_from_df2]

    # Merge DataFrames on 'id', keeping only one set of overlapping columns
    result_df = pd.merge(
        df_1,
        df_2_subset,
        on='id',
        how='inner'
    )

    # Add v1_model and v2_model columns
    result_df['v1_model'] = v1_model
    result_df['v2_model'] = v2_model

    # Generate the full judgment prompt
    result_df['full_judgment_prompt'] = result_df.apply(
        lambda row: full_judgment_prompt.format(
            conversation=row['joined_english_sentences'],
            alternate_version_1=row[f'{v1_model}_translation'],
            alternate_version_2=row[f'{v2_model}_translation']
        ), axis=1
    )

    # Define the output file path
    if output_version_name is None:
        output_file = f"./Data/Output/judgments/big_c_test_{v1_model}_vs_{v2_model}.jsonl"
    else:
        output_file = f"./Data/Output/judgments/{output_version_name}_big_c_test_{v1_model}_vs_{v2_model}.jsonl"

    # Check if the file already exists
    if os.path.exists(output_file):
        print(f"File '{output_file}' already exists. Skipping file creation.")
    else:
        # Save to JSONL file
        result_df.to_json(output_file, orient='records', lines=True)
        print(f"File '{output_file}' has been created.")

    return output_file

def main():
    prepare_judgment_file(
        v1_model="google_translate",
        v2_model="sonnet_3_point_5",
    )

# async def main():
#     translation_models = ["gpt_4o", "llama_3_1_400b", "aya_8b"]
#     for i in range(len(translation_models)):
#         # for j in range(i + 1, len(translation_models)):
#             # v1_model = translation_models[i]
#             v1_model = 'o1_preview'
#             v2_model = translation_models[i]
#             await prepare_judgment_file(
#                 v1_model=v1_model,
#                 v2_model=v2_model,
#             )

if __name__ == "__main__":
    main()
