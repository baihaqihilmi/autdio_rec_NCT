import pyaudio
import wave
import numpy as np
import numpy as np
from scipy.signal import butter, lfilter
import time
def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

class AudioRecorder:
    def __init__(self, filename="output.wav", channels=1, rate=44100, chunk=1024, silence_threshold=500, silence_duration=5, format=pyaudio.paInt16):
        self.filename = filename
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.silence_threshold = silence_threshold  # Threshold for detecting silence
        self.silence_duration = silence_duration  # Duration to wait before stopping on silence
        self.format = format
        self.audio = pyaudio.PyAudio()

    def is_silent(self, data):
        # Convert audio chunk to numpy array and check if below the threshold
        audio_data = np.frombuffer(data, dtype=np.int16)
        return np.abs(audio_data).mean() < self.silence_threshold

    def start_recording(self):
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)

        print("Recording... Speak to start recording.")
        self.frames = []
        silent_chunks = 0
        silence_limit_chunks = int(self.silence_duration * self.rate / self.chunk)  # Calculate silence limit in chunks

        while True:
            data = self.stream.read(self.chunk)
            if not self.is_silent(data):  # Detect audio presence
                print("Audio detected, recording...")
                self.frames.append(data)
                silent_chunks = 0  # Reset silent chunks counter

            else:
                # Increment silent chunk count if silence is detected
                silent_chunks += 1
                print(f"Silent for {silent_chunks * self.chunk / self.rate:.2f} seconds...", end='\r')

                # Check if silent for the given duration
                if silent_chunks >= silence_limit_chunks:
                    print("\nSilence detected for 5 seconds. Stopping recording.")
                    break

            # Continue recording if not enough silence detected
            time.sleep(0.1)  # Small delay to avoid excessive CPU usage

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def save_recording(self):
        # Save the recorded audio to a file
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

        print(f"Audio saved to {self.filename}")

    def record(self):
        try:
            self.start_recording()
        except KeyboardInterrupt:  # Use Ctrl+C to stop the recording manually
            print("Stopped by user.")
        finally:
            self.stop_recording()
            self.save_recording()


# Usage
if __name__ == "__main__":
    recorder = AudioRecorder(filename="my_audio.wav", silence_threshold=500, silence_duration=5)  # Customize settings if needed
    recorder.record()