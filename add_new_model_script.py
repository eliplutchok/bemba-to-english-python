import os
import re
import asyncio
from get_regular_translations import get_regular_translations
# import the new model service
from llm_services.get_google_translate_response import get_google_translate_response
from llm_services.get_gemini_response import get_gemini_response
from add_bertscores import add_bertscores
from add_similarity_scores import add_similarity_scores
from prepare_judgment_file import prepare_judgment_file
from add_judgments import add_judgments
translations_folder = "./Data/Output/translations"

new_llm_service = get_gemini_response

async def main():
    output_file = await get_regular_translations(new_llm_service)
    print(output_file) 
    bertscores_version_name = "v2"
    output_file = add_bertscores(
        model_name=new_llm_service.__name__,
        file_path=output_file,
        version_name=bertscores_version_name
    )
    print(output_file)
    similarity_scores_version_name = "a"
    add_similarity_scores(
        file_path=output_file,
        version_name=similarity_scores_version_name,
        embedding_model='text-embedding-ada-002'
    )

    existing_models = set()
    input_version_name = similarity_scores_version_name + "_" + bertscores_version_name
    for filename in os.listdir(translations_folder):
        if filename.endswith(".jsonl") and filename.startswith(input_version_name):
            model_name = filename.replace(f"{input_version_name}_big_c_conversations_test_", "").replace(".jsonl", "")
            if model_name != new_llm_service.__name__:
                existing_models.add(model_name)
    existing_models = list(existing_models)
    print(existing_models)

    output_files = []
    for model in existing_models:
        output_files.append(prepare_judgment_file(
            v1_model=new_llm_service.__name__,
            v2_model=model,
            input_version_name=input_version_name
        ))

    print(output_files)
    for file in output_files:
        await add_judgments(
            judgments_file_path=file,
            judgment_model='gpt_4o',
            version_name='v3'
        )


if __name__ == "__main__":
    asyncio.run(main())