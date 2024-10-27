<p align="center">
  <img src="hacker.png" alt="Bemba to English Logo" width="200" />
</p>

# Bemba to English Translation Evaluation Repository

This repository contains the code and data used to evaluate and rank various models for translating Bemba to English. It automates the process of generating translations, computing evaluation metrics, and preparing data for human-like judgments, utilizing both traditional evaluation metrics and some novel techniques.

**Website**: [bemba-to-english.netlify.app](https://bemba-to-english.netlify.app)

**Frontend Repository**: [Bemba to English React App](https://github.com/eliplutchok/bemba-to-english)

---

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Metrics and Methodologies](#metrics-and-methodologies)
  - [Judgment Battles](#judgment-battles)
  - [Consistency Battles](#consistency-battles)
  - [BERTScore Battles](#bertscore-battles)
  - [Similarity Score Battles](#similarity-score-battles)
- [Data Storage](#data-storage)
- [Scripts and Workflow](#scripts-and-workflow)
  - [Generating Translations](#generating-translations)
  - [Adding Evaluation Metrics](#adding-evaluation-metrics)
  - [Preparing Judgment Files](#preparing-judgment-files)
  - [Main Script](#main-script)
- [Display and Analysis Tools](#display-and-analysis-tools)
- [Prompts Used](#prompts-used)
  - [Translation Prompt](#translation-prompt)
  - [Judgment Prompt](#judgment-prompt)
  - [Consistency Judgment Prompt](#consistency-judgment-prompt)
- [How to Use](#how-to-use)
- [Additional Information](#additional-information)

---

## Overview

This repository automates the evaluation of translation models by generating translations, computing evaluation metrics, and preparing data for human-like judgments. The models are evaluated using the test set from the [Big C dataset](https://github.com/csikasote/bigc), and their rankings are determined using ELO ratings computed from various metrics.

We introduce **Consistency Battles**, a novel method to evaluate the quality of translation models without relying on reference translations. By assessing the consistency of a model's outputs when generating translations under varying conditions, we can infer the reliability and accuracy of the model. This approach does not require any target/reference text, making it particularly useful when high-quality reference translations are scarce or unavailable.

Our evaluation demonstrates that the ELO ratings derived from Consistency Battles closely align with those from traditional metrics such as BERTScore and human-like judgments, validating the effectiveness of our novel approach.

The results of our evaluations are available in the form of jsonl files in the Data directory. They are also available on our website: [bemba-to-english.netlify.app](https://bemba-to-english.netlify.app)

---

## Repository Structure

- **Main Script**:

  - `add_new_model_script.py`: Orchestrates the entire pipeline for adding a new model.

- **Translation Scripts**:

  - `get_regular_translations.py`: Generates translations using the models with default settings.
  - `get_high_temp_translations.py`: Generates high-temperature translations for consistency evaluations.

- **Evaluation Metrics Scripts**:

  - `add_bertscores.py`: Computes BERTScores for model translations.
  - `add_similarity_scores.py`: Computes similarity scores using embeddings from OpenAI models.

- **Judgment Preparation Scripts**:

  - `prepare_judgment_file.py`: Prepares files for human-like judgments between model translations.
  - `prepare_consistency_judgment_file.py`: Prepares files for consistency judgments between high-temperature translations.

- **Display and Analysis Tools**:

  - `big_c_conversations_eda.ipynb`: Exploratory Data Analysis notebook for the Big C dataset.
  - `display_battle_totals.py`: Visualizes battle totals between models.
  - `display_elo_rankings.py`: Displays the ELO rankings of models.
  - `display_single_judgment_file.py`: Visualizes individual judgment results.
  - `display_single_consistency_judgment_file.py`: Visualizes individual consistency judgment results.

- **Data Directory**:
  - `Data/`: Contains input datasets and stores all output data from translations, metrics, and judgments.
    - `Data/Static/`: Static input data such as the test set.
    - `Data/Output/`: Generated translations, computed metrics, prepared judgment files, and prepared files for the frontend application.

---

## Metrics and Methodologies

### Judgment Battles

In **Judgment Battles**, models are compared based on human-like judgments rendered by advanced language models (e.g., GPT-4). For each test instance, translations from two models are presented alongside the original conversation in English. The language model acts as an evaluator, judging which translation is closer in meaning to the original conversation.

While using large language models (LLMs) as judges is a technique that others have explored, it's only recently that we can reliably use LLMs for these kinds of tasks due to their new advanced capabilities. This allows for scalable and consistent evaluations compared to traditional human assessments.

### Consistency Battles

**Consistency Battles** are a novel way to evaluate translation models without the need for reference translations. By generating multiple translations from the same model using a high-temperature setting (which introduces randomness), we measure how consistent the model's outputs are under varying conditions. The assumption is that a more accurate model will produce more consistent translations even when randomness is introduced.

To our knowledge, we are not aware of anyone else using this approach for evaluating translation models. The key advantage is that it does not require any ideal or reference translation to compare against, making it especially valuable in low-resource language settings where high-quality reference translations may not be available.

Our results indicate that the ELO ratings derived from Consistency Battles are closely aligned with those from other traditional metrics. This alignment supports the validity of our novel approach and suggests that consistency can be an effective proxy for accuracy in translation evaluation.

### BERTScore Battles

**BERTScore** utilizes contextual embeddings from pre-trained BERT models to evaluate the similarity between candidate translations and reference translations. This is a traditional and widely used method in the field. It assesses the precision, recall, and F1 score based on token similarity in the embedding space.

### Similarity Score Battles

This metric evaluates models using embeddings from OpenAI's `text-embedding-ada-002` model. By converting texts into high-dimensional embeddings, cosine similarity scores are computed to assess semantic similarity between translations and references.

---

## Data Storage

All input and output data are stored in the `Data/` directory:

- **Input Data**:

  - `Data/Static/`: Contains static input data such as the test set from the Big C dataset.

- **Output Data**:
  - `Data/Output/`: Stores generated translations, computed metrics, prepared judgment files, and prepared files for the frontend application.
    - `Data/Output/translations/`: Contains translations generated by different models.
    - `Data/Output/translations_high_temp/`: Contains high-temperature translations for consistency evaluations.
    - `Data/Output/judgments/`: Contains prepared judgment files.
    - `Data/Output/consistency_judgments/`: Contains prepared consistency judgment files.
    - `Data/Output/prepared_files/`: Contains aggregated and preprocessed data files that are used by the React frontend application.

---

## Scripts and Workflow

### Generating Translations

- **Regular Translations**: Use `get_regular_translations.py` to generate translations using the models at a default temperature setting.

  ```bash
  python get_regular_translations.py
  ```

- **High-Temperature Translations**: Use `get_high_temp_translations.py` to generate translations with a higher temperature setting (e.g., 0.8) for consistency evaluations.

  ```bash
  python get_high_temp_translations.py
  ```

### Adding Evaluation Metrics

- **BERTScores**: Use `add_bertscores.py` to compute BERTScores for the model translations.

  ```bash
  python add_bertscores.py
  ```

- **Similarity Scores**: Use `add_similarity_scores.py` to compute similarity scores using embeddings from OpenAI's `text-embedding-ada-002` model.

  ```bash
  python add_similarity_scores.py
  ```

### Preparing Judgment Files

- **Regular Judgments**: Use `prepare_judgment_file.py` to prepare files for human-like judgments between two models' translations.

  ```bash
  python prepare_judgment_file.py
  ```

- **Consistency Judgments**: Use `prepare_consistency_judgment_file.py` to prepare files for consistency judgments by comparing high-temperature translations.

  ```bash
  python prepare_consistency_judgment_file.py
  ```

### Main Script

The **main script** is `add_new_model_script.py`, which orchestrates the entire pipeline for adding a new model:

1. **Generate Translations** using `get_regular_translations.py`.
2. **Add BERTScores** using `add_bertscores.py`.
3. **Add Similarity Scores** using `add_similarity_scores.py`.
4. **Prepare Judgment Files** using `prepare_judgment_file.py`.
5. **Create Prepared Files**: Aggregates and processes data to create files stored in `Data/Output/prepared_files/` for use in the frontend React application.

**Note**: The `add_new_model_script.py` handles everything except the consistency judgments. For consistency evaluations, you need to run `get_high_temp_translations.py` and `prepare_consistency_judgment_file.py` separately.

---

## Display and Analysis Tools

The repository includes several scripts and notebooks for data exploration and visualization:

- **Exploratory Data Analysis**:

  - `big_c_conversations_eda.ipynb`: Jupyter notebook for exploring the Big C dataset.

- **Visualization Scripts**:
  - `display_battle_totals.py`: Visualizes battle totals between models using heatmaps and network graphs.
  - `display_elo_rankings.py`: Displays the ELO rankings of models in a sortable table.
  - `display_single_judgment_file.py`: Visualizes individual judgment results, allowing you to inspect judgments between two models.
  - `display_single_consistency_judgment_file.py`: Visualizes individual consistency judgment results, enabling inspection of consistency judgments between models.

These tools help in analyzing the performance of different models and understanding the outcomes of various evaluation battles.

---

## Prompts Used

### Translation Prompt

Used in `get_regular_translations.py`:

```text:get_regular_translations.py
"""
You are a helpful assistant that translates Bemba to English.

You will be given a short conversation between 2 Bemba speakers.
FYI, the first line in the conversation will always be describing some image that the speakers are looking at.

Your task is to translate the Bemba conversation into English.
Your translation should be as exact as possible, including all details.
It should be formatted as a conversation between two people, with each line starting with \nA: or \nB:. Just like the way you got it.
You should respond with the translation only, without any other text.

Here is the conversation for you to translate:
"""
```

### Judgment Prompt

Used in `prepare_judgment_file.py`:

```text:prepare_judgment_file.py
"""
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
```

### Consistency Judgment Prompt

Used in `prepare_consistency_judgment_file.py`:

```text:prepare_consistency_judgment_file.py
"""
You will be given two versions of translations from the same model, generated with high temperature, and your task is to judge how consistent the translations are.

For each model, you are given two translations:

- **Model 1 Version 1**
- **Model 1 Version 2**

- **Model 2 Version 1**
- **Model 2 Version 2**

Your task is to judge which model produces more consistent translations.

Respond with **1**, **2**, or **3**:

- **1** if **Model 1** is more consistent.
- **2** if **Model 2** is more consistent.
- **3** if both are equally consistent.

**Just respond with the number. Do not include any other text.**

---

**Model 1 Version 1:**
{model_1_version_1}

**Model 1 Version 2:**
{model_1_version_2}

**Model 2 Version 1:**
{model_2_version_1}

**Model 2 Version 2:**
{model_2_version_2}

**Your response:**
"""
```

---

## How to Use

1. **Set Up Environment**:

   - Install necessary dependencies.
   - Ensure you have access to required APIs (e.g., OpenAI API key).

2. **Add a New Model**:

   - Update the `llm_services` with the new model's response function.
   - Use `add_new_model_script.py` to add the model to the evaluation pipeline:

     ```bash
     python add_new_model_script.py
     ```

   - The `add_new_model_script.py` script handles everything except the consistency judgments. It will:

     - Generate regular translations.
     - Compute BERTScores.
     - Compute Similarity Scores.
     - Prepare judgment files.
     - Create aggregated and preprocessed data files stored in `Data/Output/prepared_files/` for use in the React frontend application.

3. **Generate High-Temperature Translations** (for Consistency Battles):

   - Run `get_high_temp_translations.py` to generate translations at a higher temperature setting:

     ```bash
     python get_high_temp_translations.py
     ```

4. **Prepare Consistency Judgment Files**:

   - Run `prepare_consistency_judgment_file.py` to prepare files for consistency judgments:

     ```bash
     python prepare_consistency_judgment_file.py
     ```

5. **Compute Metrics**:

   - **Add BERTScores**:

     ```bash
     python add_bertscores.py
     ```

   - **Add Similarity Scores**:

     ```bash
     python add_similarity_scores.py
     ```

6. **Add Judgments**:

   - Use the prepared judgment files to obtain judgments (implementation details may vary).

7. **Visualize and Analyze Results**:

   - Use the display and analysis scripts to explore the results:
     - `display_battle_totals.py`
     - `display_elo_rankings.py`
     - `display_single_judgment_file.py`
     - `display_single_consistency_judgment_file.py`

8. **Frontend Application**:

   - The prepared files in `Data/Output/prepared_files/` can be used with the [Bemba to English React App](https://github.com/eliplutchok/bemba-to-english) to display the results on the website.

---

## Additional Information

For more detailed information about the methodologies, implementation details, or to access the data and code used in this project, please refer to the code in this repository.

If you have any questions or would like to contribute, feel free to open an issue or submit a pull request.
