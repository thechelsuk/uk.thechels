# importing modules
import os
import pathlib

root = pathlib.Path(__file__).parent.parent.resolve()
yamlFile = root / "_data/podcasts.yml"

content = os.getenv("content").replace('`','').strip()

try:    
    with open(yamlFile, 'a') as f:
        outputs = f.write(content)
        print(outputs)        
except FileNotFoundError:
        print('File does not exist, unable to proceed') 
