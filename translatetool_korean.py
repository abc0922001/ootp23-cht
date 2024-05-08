import xml.etree.ElementTree as ET
import openai
import time

# 設定 OpenAI API 金鑰
openai.api_key = "YOUR_API_KEY"

def replace_text(element):
    if element.tag == 'TXT' and element.text and element.text.strip():
        print(element.text.strip())
        print("")
        print("Call Open API")
        completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user",  "content": f"Translate the given text to traditional Chinese. Be faithful and accurate in translation. Make the translation readable and intelligible. Be elegant and natural in translation. If the text cannot be translated, return the original text as is. Do not translate person's names. Do not add any additional text in the translation. While translating, please note that the text is related to baseball. The text to be translated is:\n{element.text.strip()}"}]
                )
        print("Transalte====================")
        print(completion.choices[0].message.content)
        element.text = completion.choices[0].message.content
        save_to_file(tree)
        print("=======================================")
        
    for attr_name, attr_value in element.attrib.items():
        if attr_name == 'text' and attr_value.strip():
            print(attr_value.strip())
            print("")
            print("Call Open API")
            completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user",  "content": f"Translate the given text to traditional Chinese. Be faithful and accurate in translation. Make the translation readable and intelligible. Be elegant and natural in translation. If the text cannot be translated, return the original text as is. Do not translate person's names. Do not add any additional text in the translation. While translating, please note that the text is related to baseball. The text to be translated is:\n{attr_value.strip()}"}]
                )
            print("Transalte====================")
            print(completion.choices[0].message.content)
            element.set(attr_name, completion.choices[0].message.content)
            save_to_file(tree)
            print("=======================================")
    
    for child in element:
        while True:
            try:                
                replace_text(child)
                break
            except Exception as e:
                print(f"Error occurred: {e}")
                time.sleep(60)

def save_to_file(tree):
    with open('korean.xml', 'w', encoding='utf-8') as f:
        f.write(ET.tostring(tree, encoding='unicode'))

# 從外部文件讀取 XML 內容
with open('demo.xml', 'r', encoding='utf-8') as f:
    xml_data = f.read()

tree = ET.fromstring(xml_data)
replace_text(tree)

# 將修改後的 XML 內容寫入文件
save_to_file(tree)
