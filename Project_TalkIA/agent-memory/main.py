from openai import OpenAI
from dotenv import load_dotenv
from dotenv import find_dotenv
import os
from utils.record_audio import record_audio
from utils.basemodel2tool import base_model2tool
from tools.daily_events import DailyEvents
from datetime import datetime
import json

load_dotenv(find_dotenv())

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

while True:
    memory = {
        "events": [],
        "interactions": []
    } if not os.path.exists("memory.json") else json.load(open("memory.json"))

    filename_audio = record_audio()

    audio_file = open(filename_audio, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        language="pt"
    )

    os.remove(filename_audio)

    text = transcription.text

    print(text)

    actual_date = datetime.now().strftime("%d/%m/%Y")

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "developer", "content": f"You are a helpful assistant. You are responsible for remembering events of my life. Today is {actual_date} use this as a reference to remember events. If the event occurred in the past, you should use the date to remember the event using today's date as a reference."},
        {"role": "assistant", "content": json.dumps(memory)},
        {"role": "user", "content": text}
    ],
    tool_choice="auto",
    tools=[
        base_model2tool(DailyEvents)
        ]
    )

    if completion.choices[0].message.tool_calls:
        for tool_call in completion.choices[0].message.tool_calls:
            if tool_call.function.name == "DailyEvents":
                daily_events = DailyEvents(**json.loads(tool_call.function.arguments))
                memory["events"].append(f"Day: {daily_events.date} - {daily_events.events}")

        memory['interactions'].append(f"Human: {text}")
        memory['interactions'].append(f"Assistant: Evento do dia {daily_events.date} registrado com sucesso, posso te ajudar com mais alguma coisa?")
        print(f"Evento do dia {daily_events.date} registrado com sucesso, posso te ajudar com mais alguma coisa?")

    if completion.choices[0].message.content:
        memory['interactions'].append(f"Human: {text}")
        memory['interactions'].append(f"Assistant: {completion.choices[0].message.content}")
        print(completion.choices[0].message.content)

    with open("memory.json", "w") as f:
        json.dump(memory, f)
