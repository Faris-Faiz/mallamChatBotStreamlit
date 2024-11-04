# Mallam ChatBot 🤖

A Streamlit-powered chatbot application that provides interactive conversational capabilities.

## Prerequisites 📋

Before you begin, ensure you have the following installed on your Windows system:
- [Python 3.12.7](https://www.python.org/downloads/release/python-3127/) (recommended version)
- [Git](https://git-scm.com/downloads) (for cloning the repository)

## Installation Guide 🚀

Follow these steps to set up the project locally on your Windows machine:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mallamChatBotStreamlit.git
cd mallamChatBotStreamlit
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to avoid any conflicts with other Python projects. Open Command Prompt and run:

```bash
# Create a new virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

You'll know the virtual environment is activated when you see `(venv)` at the beginning of your command prompt.

### 3. Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application 🎯

Once you've completed the installation, you can run the application:

```bash
streamlit run app.py
```

The application will start and automatically open in your default web browser. If it doesn't, you can manually navigate to the URL shown in the terminal (typically `http://localhost:8501`).

## Troubleshooting 🔧

If you encounter any issues:

1. Ensure Python 3.12.7 is properly installed:
   ```bash
   python --version
   ```

2. Verify that your virtual environment is activated (you should see `(venv)` in your command prompt)

3. If you face dependency issues, try:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

## Development 💻

To deactivate the virtual environment when you're done:
```bash
deactivate
```

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.
