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

print("🎤 Assistente de Memória Iniciado!")
print("💡 Dica: Diga 'sair' ou 'quit' para encerrar a aplicação")
print("-" * 50)

while True:
    memory = {
        "events": [],
        "interactions": []
    } if not os.path.exists("memory.json") else json.load(open("memory.json"))

    filename_audio = record_audio()

    with open(filename_audio, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="pt"
        )

    # Aguarda um pouco antes de tentar deletar o arquivo
    import time
    time.sleep(0.5)

    try:
        os.remove(filename_audio)
    except PermissionError:
        print(f"⚠️ Não foi possível deletar {filename_audio} - arquivo ainda em uso")
        # Tenta deletar novamente após mais tempo
        time.sleep(1)
        try:
            os.remove(filename_audio)
        except PermissionError:
            print(f"⚠️ Arquivo {filename_audio} não foi deletado automaticamente")

    text = transcription.text.lower().strip()

    print(f"🎤 Você disse: {text}")

    # Verificar se o usuário quer sair
    if text in ["sair", "quit", "exit", "encerrar", "parar"]:
        print("👋 Encerrando aplicação...")
        print("💾 Salvando memória...")
        with open("memory.json", "w") as f:
            json.dump(memory, f)
        print("✅ Memória salva com sucesso!")
        print("👋 Até logo!")
        break

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
        base_model2tool(DailyEvents)  # type: ignore
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
