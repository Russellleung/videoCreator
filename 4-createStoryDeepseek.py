from dotenv import dotenv_values
import json

import requests

config = dotenv_values(".env")
json_file_path = config["metadataFilePath"]

API_KEY = config["API_KEY"]
API_URL = config["API_URL"]
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


def get_chat_response(imageMetaData, batchIdx) -> str:
    """Get streaming response from OpenAI API.

    Args:
        messages: Chat history
        context: Retrieved context from database

    Returns:
        str: Model's response
    """
    minifiedImageMetaData = [
        [item["labels"], item["description"]] for item in imageMetaData
    ]

    system_prompt = f"""You are an older sister who likes to tease your siblings. You read flipping through a travel album from a friend. Talk like a teenager. You are sarcastic and snappy at first, but you warm up to the pictures. You grow bored of some pictures and comment less on those. Imagine what the picture is like from the labels and description. People in the pictures are mostly likely the same person. Each comment on a photo should be on a new line. Do not number the lines. Your output needs to equal the number of photos given. 
    
    Context:
    {minifiedImageMetaData}
    """

    messages_with_context = [{"role": "system", "content": system_prompt}]

    # Define the request payload (data)
    data = {
        "model": "deepseek/deepseek-chat:free",
        "messages": messages_with_context,
    }

    # Send the POST request to the DeepSeek API
    response = requests.post(API_URL, json=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("API Response:", response.json()["choices"][0]["message"]["content"])
        response = response.json()["choices"][0]["message"]["content"]
        # Split the response text by newline characters and filter out any empty lines
        lines = [line.strip() for line in response.split("\n") if line.strip()]
        if len(lines) != len(imageMetaData):
            print("failed prompt by deepseek at batch " + str(batchIdx))
            return
        for line, met in zip(lines, imageMetaData):
            met["line"] = line

        # with open("deepseekResponse.json", "w") as json_file:
        #     json.dump({"response": response}, json_file, indent=4)
    else:
        print("Failed to fetch data from API. Status Code:", response.status_code)

    # # Create the streaming response
    # stream = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=messages_with_context,
    #     temperature=0.7,
    #     stream=True,
    # )

    # # Use Streamlit's built-in streaming capability
    # response = st.write_stream(stream)
    return response


with open(json_file_path, "r") as json_file:
    data = json.load(json_file)

for i in range(0, len(data), 20):
    get_chat_response(data[i : i + 20], i)


with open(json_file_path, "w") as json_file:
    json.dump(data, json_file, indent=4)
