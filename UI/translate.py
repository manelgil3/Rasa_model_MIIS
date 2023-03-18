import requests 
result = requests.get( 
   "https://api-free.deepl.com/v2/translate", 
   params={ 
     "auth_key": "017bb4a0-954d-54c9-09fd-30e123255439:fx", 
     "target_lang": "EN", 
     "text": "HOla gente, o cortamos esto, o incrementamos la pandemia ", 
   }, 
) 
translated_text = result.json()["translations"][0]["text"]
print(translated_text)