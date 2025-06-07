# Contract Processing Application

This application processes contracts, potentially using PDF inputs and Word document templates.

## Project Structure
The project is organized into the following main directories:
- `core/`: Contains the core business logic and processing functions.
- `gui/`: Contains all components related to the graphical user interface (PyQt6).
- `templates/`: Contains Word document templates used for generation.
- `main.py`: The main entry point for the application.
- `app_controller.py`: Manages the overall application flow, configuration, and GUI initialization.
- `config.YAML`: Main configuration file for the application.
- `requirements.txt`: Lists all Python dependencies.

## Setup
1.  Ensure you have Python 3.x installed.
2.  Clone the repository (if applicable).
3.  Navigate to the project directory.
4.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Review and customize `config.YAML` if needed. Default settings are provided.

## Usage
Run the application from the project root directory:
```bash
python main.py
```
