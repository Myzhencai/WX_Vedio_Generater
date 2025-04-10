

from google import genai

# 初始化Google GenAI客户端
client = genai.Client(api_key="AIzaSyDnJ-HAfTYa7hdO4V2xXhuIAbElsjfxtSI")



# 读取txt文件
with open('SourceFile/cotant.txt', 'r', encoding='utf-8') as file:
    # 逐行读取文件并按“；”分割每一行
    lines = file.readlines()
    for line in lines:
        # 去除行尾换行符并按“；”分割
        # files = line.strip().split("；")

        content = line.strip().replace(";", "")
        # 构造新的内容
        prompt = f"翻译:{content}"

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        # print(response.text)  # 输出生成的内容

        prompt2= f"重写成80个汉字的新内容，内容意思不变:{prompt}"

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt2,
        )
        print(response.text)  # 输出生成的内容


