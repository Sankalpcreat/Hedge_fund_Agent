import os
import getpass

def set_api_keys():
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Please provide your OPENAI_API_KEY: ")
    if not os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        os.environ["FINANCIAL_DATASETS_API_KEY"] = getpass.getpass("Please provide your FINANCIAL_DATASETS_API_KEY: ")

set_api_keys()