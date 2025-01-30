from datasets import load_dataset
#from vram import get_machine_spec
from huggingface_hub import list_models
import pandas as pd
import re
import os
# grateful that pandas supports emojis

# TODO: check if architecture allows for quantization
# TODO: if using ram instead of vram (cpu instead of gpu), log a note to user of potentially slow speed
# TODO: install the model via cli wait thats kinda like ollama then
# TODO: add project description on pypi
# TODO: check if it is necessary to also upload the wheels to github
# TODO: add testing
# TODO: refine readme
# TODO: add logging & more...

# run once or something
def list_to_excel():
    # should be all of the models listed in the leaderboard
    dataset = load_dataset("open-llm-leaderboard/contents", split="train")

    # conversion into a pandas DataFrame
    df = dataset.to_pandas()

    # conversion to excel to make visualization easier
    df.to_excel("leaderboard.xlsx")


def get_llm_list(precision: str, capacity: float) -> pd.DataFrame:
    """ Depending on user input, prolly, give us the appropriate list of llms
    """
    # first check if we have the leaderboard downloaded
    if not os.path.exists("leaderboard.xlsx"):
        list_to_excel()

    # i'll keep two copies of what is essentially the same cuz i can't think of anything for now
    precision_str = precision
    precision = float("".join(re.findall(r'\d+', precision))) # parse precision into float
    max_param = capacity / (precision / 8.0) # total capacity / unit memory usage per 1B params = max param we can store
    llm_list = pd.DataFrame(columns=['Model Name', 'Average Score', 'Architecture'])
    precision_mapping ={'fp16': 'float16', 'bf16': 'bfloat16'}
    df = pd.read_excel("leaderboard.xlsx")
    # filter by model parameters, and precision if applicable
    filtered_df = df[ 
        (df['#Params (B)'] <= max_param) &
        ((precision_str.lower() not in ['fp16', 'bf16']) |
            (df['Precision'] == precision_mapping.get(precision_str.lower(), False)))
        ]  # can None be an error or exception that we can return or log?

    sorted_df = filtered_df.sort_values(by='Average ⬆️', ascending=False).reset_index(drop=True)  # sort by average score in descending order and get natural indexing
    #sorted_df.to_excel("sorted_leaderboard.xlsx")

    for idx in range(5): # top 5 performing models
        model_name = sorted_df['fullname'][idx]
        model_average = sorted_df['Average ⬆️'][idx] 
        model_architecture = sorted_df['Architecture'][idx]

        llm_list.loc[len(llm_list)] = [model_name, model_average, model_architecture]

    llm_list.index = llm_list.index + 1 # looks nicer when printed

    return llm_list








