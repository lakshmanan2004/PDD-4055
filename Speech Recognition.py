import socket
import speech_recognition as sr
import time
# Set up the recognizer
recognizer = sr.Recognizer()

# Define the host and port for communication with Unity
host = '127.0.0.1'  # Locsalhost (IP Address)
port = 5000         # Port (ensure it matches Unity's listener)

try:
    while True:  # Loop to continuously listen for commands
        # Speech Recognition
        with sr.Microphone() as source2:
            print("Silence Please")
            recognizer.adjust_for_ambient_noise(source2, duration=2)
            print("Speak now")
            audio2 = recognizer.listen(source2)

        try:
            # Convert speech to text
            text = recognizer.recognize_google(audio2).lower()
            print("Did you Say: " + text)

            if text in ["exit", "stop"]:  # Check for the exit condition
                print("Exiting the program. Goodbye!")
                break

            # Send the text to Unity
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(text.encode('utf-8'))  # Encode text and send
                print("Sent to Unity: " + text)

        except sr.UnknownValueError:  
            print("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as ex:
            print(f"An error occurred during processing: {ex}")

        # Wait for 5 seconds before next iteration
        time.sleep(5)

except KeyboardInterrupt:
    print("\nProgram interrupted by user. Exiting...")
except Exception as ex:
    print(f"An error occurred: {ex}")
