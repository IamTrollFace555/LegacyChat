import openai
openai.api_key = "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"

prompt = \
"""
Cómo se llamaría jaider si fuera holandés?
"""

model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": prompt}]
response = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=3500)
generated_text = response["choices"][0]["message"]["content"]

print(response)
print(generated_text)