# Audio2VideoMaker: Transform Audio into Engaging Videos

**Audio2VideoMaker** is a powerful Python-based tool that transforms your audio files into captivating videos. It achieves this by synchronizing a sequence of text-based images with your audio, creating a dynamic visual experience that complements the audio content.  This project is perfect for creating:

*   **Lyric videos:** Display song lyrics in sync with the music.
*   **Podcast videos:** Add visual interest to your podcast episodes.
*   **Educational content:** Combine audio explanations with relevant text and visuals.
*   **Social media content:** Create engaging videos for platforms like YouTube, Instagram, and TikTok.
* **Presentations**: Create a video presentation with audio and text.

## Key Features

*   **Audio-Driven Video Generation:** Automatically generates a video based on the duration of your audio file.
*   **Text-Based Image Creation:** Creates images with customizable text, font, color, and layout.
*   **Multi-Image Support:** Supports multiple images with varying durations, allowing for a dynamic video flow.
*   **Configurable via YAML:** Easily customize the video's content, timing, and appearance using a simple YAML configuration file.
*   **Error Handling:** Robust error handling to catch issues like missing files or text exceeding image boundaries.
*   **Logging:** Detailed logging to track the video creation process and identify potential problems.
* **Status Indicators:** Clear status indicators (e.g., [✅ OK!], [⏳️WIP]) in the logs to show the progress and success of operations.
* **Customizable:** Change the font, font size, background color, text color, padding, and more.

## Getting Started

### Installation

1. **Clone the Repository:**

   ```shell
   git clone git@github.com:msampathkumar/Audio2VideoMaker
   git cd Audio2VideoMaker/app
   ```

1. **Create a Virtual Environment (Recommended):**

   It's highly recommended to use a virtual environment to isolate the project's dependencies.

   ```shell
   python3 -m venv venv
   source venv/bin/activate
   ```

1. **Install Dependencies:**

   ```shell
   pip install -r requirements.txt
   ```

### Configuration

1.  **Create or Modify `config.yaml`:**

    The `data/sample_data/config.yaml` file is your control center. Here's a breakdown of its structure:

      ```text
      # Add your audio file here
      audio: tell-me-the-truth-260010.mp3 # Replace with your audio file name (must be in the data folder)
      
      # Add your output path here
      video: tell-me-the-truth-260010.mp4 # Replace with your desired output video name
      
      # Add your text information here
      images:
          # Add your first image data
          - duration: 15 # Duration in seconds for this image
            text: |
              Welcome to Audio-Video.
              I hope that this tool is useful to you.
                              Just don't be evil for anyone!
              Thank you, Author
          # Add your next image data
          - duration: 30 # Duration in seconds for this image
            text: Hello world!
          # Add your next image data
          - duration: 15 # Duration in seconds for this image
            text: "Thank you                              Thank you\n\n\n\n\n\n\n\n\n\nThank you                              Thank you"
      # Add your output path here
      comment: Thank you, Author # Any additional comments
      ```

 *   **`audio`:** The name of your audio file (e.g., `my_audio.mp3`). Place your audio file in the `data/sample_data` directory.
 *   **`video`:** The desired name of the output video file (e.g., `my_video.mp4`).
 *   **`images`:** A list of image configurations. Each image configuration has:
     *   **`duration`:** The duration (in seconds) for which the image will be displayed.
     *   **`text`:** The text to be displayed on the image. Use `|` to write multiline text.
 * **`comment`**: Any additional comments.

1. **Add your audio file**
    * Add your audio file to `data/sample_data` folder.
   
1. **Add your text**
    * Add your text to `config.yaml` file.

### Running the Application

**Generate an Image:**

```shell
python main.py image data/sample_data/config. yaml
```  

This command will create an image(s) based on the configuration in `config.yaml`.

**Generate a Video:**

```shell
python main.py video data/sample_data/config. yaml
```
 
This command will create a video based on the configuration in `config.yaml`.

### Testing

1. **Run the test script**


```
./test.sh
```


## Project Structure

```text
Audio2VideoMaker/
├── app/
    │
    ├── config.py # Configuration settings (font, image dimensions, etc.)
    ├── image.py # Image generation logic
    ├── main.py # Main application entry point
    ├── text_manager.py # Text validation and management
    ├── utils.py # Utility functions and classes (e.g., Status)
    ├── video.py # Video generation logic 
    ├── requirements.txt # Project dependencies
    └test.sh # Test script
├── data/ 
    └── sample_data/
        ├── config.yaml # Sample configuration file
        └── tell-me-the-truth-260010. mp3 # Sample audio file
└── README.md # This file
```

# Credits & Sources

*   **Fonts:** Google Fonts (You can download and use any font you like).


## Contributing

If you want to contribute to the project, please follow these steps:

1. Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them.
4.  Push your changes to your fork.
5.  Create a pull request to the original repository.

## License

MIT










































