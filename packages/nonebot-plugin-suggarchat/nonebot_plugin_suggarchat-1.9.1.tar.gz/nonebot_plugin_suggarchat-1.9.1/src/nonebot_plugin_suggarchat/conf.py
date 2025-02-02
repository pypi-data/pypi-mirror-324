import os
from pathlib import Path
import nonebot_plugin_localstore as store
__KERNEL_VERSION__:str = "V1.9.1-Public-Dev"
# 获取当前工作目录  
current_directory:str = os.getcwd()  
config_dir = store.get_plugin_config_dir()
if not config_dir.exists():
    config_dir.mkdir()
group_memory = store.get_plugin_data_dir()/"group"
if not group_memory.exists():
    group_memory.mkdir()
private_memory = store.get_plugin_data_dir()/"private"
if not private_memory.exists():
    private_memory.mkdir()
main_config = config_dir/"config.json"
group_prompt = config_dir/"prompt_group.txt"
private_prompt = config_dir/"prompt_private.txt"
custom_models_dir = config_dir/"models"