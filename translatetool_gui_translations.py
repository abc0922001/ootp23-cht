import xml.etree.ElementTree as ET
import openai
import time

# 設定 OpenAI API 金鑰
openai.api_key = "YOUR_API_KEY"

# 讀取 XML 檔案
tree = ET.parse('demo.xml')
root = tree.getroot()

# 取得 <EN> 元素的值，加上 123 後貼到 <KR> 元素中
for hcs in root.iter('HCS'):
    en = hcs.find('EN')
    kr = hcs.find('KR')
    print(en.text)
    print("Call Open API")
    completion = openai.ChatCompletion.create(
    model="gpt-4", 
    messages=[{"role": "user",  "content": f"Please help me translate the following text into commonly used traditional Chinese in Taiwan. My input is all about baseball and comes from a baseball simulation game called OOTP. Please use commonly used punctuation marks in Taiwan, and make sure that the meaning is not deviated from the original text, the translation is accurate, without omission or arbitrary addition. The translation should be clear and smooth, and the choice of words should be appropriate, pursuing the elegance and simplicity of the article itself. Return only the translated content, not the original text. Here is the text:\n\n{en.text}"}]
    )
    print(completion.choices[0].message.content)
    kr.text = completion.choices[0].message.content
    time.sleep(5)

# 將修改後的 XML 檔案儲存
tree.write('modified_translation.xml', encoding='utf-8')
