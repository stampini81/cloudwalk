import pyaudio
import wave
import sys
import platform

# Conditionally import msvcrt on Windows
if platform.system() == "Windows":
    import msvcrt

def record_audio(filename="output.wav"):
    """
    Grava áudio do microfone e salva em um arquivo WAV.
    A gravação para quando o usuário pressiona Enter.
    Retorna None se a gravação for muito curta.
    """
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100
    min_duration = 0.5  # Duração mínima em segundos

    p = pyaudio.PyAudio()

    print("Press Enter to start recording, press Enter again to stop...")

    # Wait for user to press Enter to start
    input()
    print("🎤 Gravando...")

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []
    start_time = None

    while True:
        # Check for stop condition based on OS
        if platform.system() == "Windows":
            # Non-blocking key check for Windows
            if msvcrt.kbhit() and msvcrt.getch() == b'\r':
                break
        else:
            # Non-blocking key check for Unix-like systems (Linux, macOS)
            import select
            if select.select([sys.stdin], [], [], 0.01)[0]:
                sys.stdin.readline()
                break

        data = stream.read(chunk)
        frames.append(data)

        # Registra o tempo de início na primeira frame
        if start_time is None:
            import time
            start_time = time.time()

    stream.stop_stream()
    stream.close()
    p.terminate()

    print("🔴 Gravação finalizada.")

    # Verifica duração da gravação
    if start_time is not None:
        import time
        duration = time.time() - start_time
        if duration < min_duration:
            print(f"⚠️ Gravação muito curta ({duration:.2f}s). Mínimo: {min_duration}s")
            return None

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename

if __name__ == '__main__':
    record_audio()
