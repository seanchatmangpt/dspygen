import os
from re import M
import ollama

# Define the path to the folder containing the images
folder_path = '/Users/sac/dev/vault/myvault/notebook-pages'

def transcribe_notes(folder_path, model):
    # Get a list of all image files in the specified folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpeg', '.jpg', '.png'))]

    # Initialize a dictionary to hold transcriptions
    transcriptions = {}

    for image_file in image_files:
        # Construct the full path to the image
        image_path = os.path.join(folder_path, image_file)

        # Use the Ollama chat function to transcribe the image
        res = ollama.chat(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': 'Transcribe the notes in this image:',
                    'images': [image_path]
                }
            ]
        )

        # Extract the transcription content
        transcription = res['message']['content']
        transcriptions[image_file] = transcription
        print(f'Transcribed {image_file}: {transcription}')

    return transcriptions

# Call the transcribe_notes function
if __name__ == "__main__":
    all_transcriptions = transcribe_notes(folder_path, model="llava-llama3")

    # Optionally, save the transcriptions to a file
    with open('transcriptions.txt', 'w') as f:
        for image, text in all_transcriptions.items():
            f.write(f'{image}: {text}\n')
            break

    print("Transcription complete. Results saved to transcriptions.txt.")
