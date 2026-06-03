from google import genai
client = genai.Client(api_key="AQ.Ab8RN6JABLZktGiRO_suIgdIwjuItfodObDFLjy_G8IpLFQMMA")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is Python?"
)

print(response.text)