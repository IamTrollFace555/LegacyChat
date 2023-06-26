import openai
openai.api_key = "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"

prompt = \
"""Please write a letter from a grandfather to a child congratulating him and providing advice on starting his first job with the following assumptions:
The grand father has the following core values:  family oriented, hardworking loyal and focused on helping others.
The grandson has the following traits:  he is very bright, friendly, social, and creative.
"""

model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": prompt}]
response = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=500)
generated_text = response["choices"][0]["message"]["content"]

print(response)
print(generated_text)