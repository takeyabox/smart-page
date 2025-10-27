from openai import OpenAI

# APIキーを設定（環境変数でも可）
client = OpenAI(api_key="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")

response = client.chat.completions.create(
    model="gpt-4o-mini",  # 例：GPT-4系
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "こんにちは、自己紹介してください。"}
    ]
)

print(response.choices[0].message.content)
