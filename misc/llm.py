import boto3
import json


ENDPOINT_NAME = "huggingface-pytorch-tgi-inference-2023-11-17-19-32-22-366"


def load_llm(payload):
    client = boto3.client('runtime.sagemaker', region_name='us-east-1')
    response = client.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                      ContentType='application/json',
                                      Body=json.dumps(payload))
    return response


prompt = "What is AI?"

payload = {
    "inputs": prompt,
    "parameters": {
        "do_sample": True,
        "top_p": 0.6,
        "temperature": 0.8,
        "top_k": 50,
        "max_new_tokens": 512,
        "repetition_penalty": 1.03,
        "stop": ["</s>"]
    }
}

result = load_llm(payload=payload)

final_result = result['Body']

print(final_result.read())

