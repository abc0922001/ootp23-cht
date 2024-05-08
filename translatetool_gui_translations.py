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
    dc = hcs.find('DC')

    if kr is None or kr.text is None or kr.text.strip() == "":
        print("=======================================")
        if kr is None:
            kr = ET.SubElement(hcs, 'KR')
        print(en.text)
        print("")
        print("Call Open API")
        try:
            if dc is None or dc.text is None or dc.text.strip() == "":
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user",  "content": f"在棒球模擬遊戲裡面，「{en.text}」翻譯成臺灣常用的繁體中文是什麼呢？直接給我翻譯後的文字就好，不要有其他的解釋：\n\n{en.text}"}]
                )
            elif dc.text.strip() != "":
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user",  "content": f"在棒球模擬遊戲裡面，「{en.text}」翻譯成臺灣常用的繁體中文是什麼呢？字串的描述為「{dc.text}」，直接給我翻譯後的文字就好，不要有其他的解釋：\n\n{en.text}"}]
                )
            print("Transalte====================")
            print(completion.choices[0].message.content)
            kr.text = completion.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            print("Waiting for 60 seconds before retrying...")
            time.sleep(60)
            if dc is None or dc.text is None or dc.text.strip() == "":
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user",  "content": f"在棒球模擬遊戲裡面，「{en.text}」翻譯成臺灣常用的繁體中文是什麼呢？直接給我翻譯後的文字就好，不要有其他的解釋：\n\n{en.text}"}]
                )
            elif dc.text.strip() != "":
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user",  "content": f"在棒球模擬遊戲裡面，「{en.text}」翻譯成臺灣常用的繁體中文是什麼呢？字串的描述為「{dc.text}」，直接給我翻譯後的文字就好，不要有其他的解釋：\n\n{en.text}"}]
                )
            print("Transalte====================")
            print(completion.choices[0].message.content)
            kr.text = completion.choices[0].message.content
        finally:
            print("=======================================")
            print("time.sleep(3)")
            time.sleep(3)
    elif kr.text.strip() != "":
        print("KR is exist value,skip translate")
        continue
    else:
        kr.text += ""
    # 將修改後的 XML 檔案儲存
    tree.write('modified_translation.xml', encoding='utf-8')