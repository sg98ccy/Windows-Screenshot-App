# Screenshot Selector

**Screenshot Selector** is a simple and customizable Python-based tool that allows users to capture screenshots with specific dimensions and aspect ratios. The app provides an interactive interface to select width and height, lock aspect ratios, and automatically scale dimensions with a slider.

## Features

- **Custom Dimensions**: Specify width and height in pixels.
- **Aspect Ratio Lock**: Choose from preset ratios (16:9, 16:10, 4:3, 1:1) to automatically adjust dimensions and maintain the selected aspect ratio.
- **Scaling Slider**: Smoothly scale dimensions up or down while maintaining the selected ratio.
- **Clipboard Copy**: Automatically copies the captured screenshot to the clipboard.
- **Auto-Save**: Saves the screenshot in a specified folder with a timestamped filename.

## Prerequisites

- **Python 3.7+**: Ensure Python is installed. [Download Python](https://www.python.org/downloads/)
- **pip**: Python's package manager, usually included with Python.
- **Git**: To clone the repository if desired.

## Setup Instructions

### Step 1: Clone the Repository or Download Files

To clone this repository, use the following command in your terminal or command prompt:

```bash
git clone https://github.com/yourusername/screenshot-selector.git
```

Alternatively, you can download the files as a ZIP from GitHub and extract them.

### Step 2: Set Up a Virtual Environment

1. Navigate to the project directory:

   ```bash
   cd screenshot-selector
   ```

2. Create a virtual environment named `screenshot-app`:

   ```bash
   python -m venv screenshot-app
   ```

3. Activate the virtual environment:

   - **On Windows**:

     ```bash
     screenshot-app\Scripts\activate
     ```

   - **On macOS/Linux**:

     ```bash
     source screenshot-app/bin/activate
     ```

### Step 3: Install Dependencies

With the virtual environment activated, install the required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 4: Verify the `favicon.ico` Path

The application uses a custom icon (`favicon.ico`). Ensure that `favicon.ico` is located in the project’s root directory. If not, place it there or update the icon path in the code (`app.py`).

### Step 5: Run the Application

With all dependencies installed, you can now launch the app by running the main script:

```bash
python app.py
```

This will open the **Screenshot Selector** GUI.

## How to Use the Screenshot Selector

1. **Specify Width and Height**:
   - Enter your desired dimensions (in pixels) in the width and height boxes.
   - If you have selected an aspect ratio, changing one dimension will automatically adjust the other to maintain the ratio.

2. **Select Aspect Ratio**:
   - Choose from the dropdown to select a predefined ratio (e.g., 16:9, 4:3). Selecting a ratio will lock the dimensions, meaning changes in width will adjust height proportionally.
   - The default is set to "Custom," which allows free adjustments of width and height without locking.

3. **Use the Scaling Slider**:
   - The slider starts in the middle with no scaling effect. Moving it left will reduce the dimensions, and moving it right will increase them, keeping the selected aspect ratio.

4. **Capture the Screenshot**:
   - Once the dimensions are set, click the **Select Screenshot Area** button.
   - A fullscreen selector will appear, allowing you to choose the specific area to capture.

5. **Auto-Save and Copy to Clipboard**:
   - The captured screenshot will be saved automatically in the `Screenshot Outputs` folder on your Desktop, with a timestamped filename.
   - The screenshot is also copied to the clipboard for easy pasting.

## Folder Structure

The project files are organized as follows:

```plaintext
screenshot-selector/
├── app.py                  # Main application code
├── App.ipynb               # Optional notebook version
├── favicon.ico             # Custom icon for the application
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation (this file)
```

## Building an Executable (Optional)

If you’d like to create a standalone executable for the application:

1. Install `pyinstaller` if it’s not already installed:

   ```bash
   pip install pyinstaller
   ```

2. Run `pyinstaller` with the following command:

   ```bash
   pyinstaller --onefile --windowed --name "Screenshot Selector" --icon="favicon.ico" app.py
   ```

3. After running the above command, the executable will be created in the `dist` folder. You can now run the `Screenshot Selector.exe` file directly.

## Troubleshooting

- **Icon Not Displaying**: Ensure `favicon.ico` is in the project’s root directory and correctly referenced in `app.py`.
- **Dependencies Missing**: If the app does not launch, double-check that all dependencies in `requirements.txt` were installed correctly.
- **Virtual Environment Issues**: If you encounter issues with activating or using the virtual environment, try deleting the `screenshot-app` folder and recreating it by following **Step 2**.

## Contributing

Contributions are welcome! If you find bugs or have suggestions, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
