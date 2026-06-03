import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6JABLZktGiRO_suIgdIwjuItfodObDFLjy_G8IpLFQMMA")

try:
    models = genai.list_models()

    for model in models:
        print(model.name)

except Exception as e:
    print(e)