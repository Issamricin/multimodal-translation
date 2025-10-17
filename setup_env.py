import os

def set_cpu_env():
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    os.environ["STANZA_USE_GPU"] = "False"