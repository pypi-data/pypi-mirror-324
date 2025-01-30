import psutil
from whatllm import ERRORS

def get_total_ram() -> float:
    gibi = 1073741824

    try:
        memory = psutil.virtual_memory().total
    except:
        raise ERRORS[1] # RAM_ERROR
    
    memory_gib = round(memory / gibi, 2)

    return memory_gib
