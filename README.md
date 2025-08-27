# NL2SQL_Agent_With_Ollama_LangChain
Basic NL2SQL Agent With Python
=======
# Project Management AI Assistant

## Overview

Project Management AI Assistant is an intelligent desktop application designed to help teams and managers interact with their project database using natural language. Powered by advanced LLM models and a user-friendly PyQt6 interface, it enables users to query, analyze, and manage project data efficiently without writing complex SQL queries.

## Features

- **Natural Language to SQL:** Convert plain English or Turkish questions into accurate SQL queries for your SQLite project database.
- **AI Chatbot:** Get instant answers and insights about your projects, tasks, customers, and team members.
- **Secure Query Execution:** Prevents dangerous SQL operations and ensures data integrity.
- **Modern UI:** Clean and responsive PyQt6-based interface for seamless user experience.
- **Customizable LLM Backend:** Easily switch or configure LLM models for SQL generation and chatbot responses.

## Technologies Used

- **Python 3**
- **PyQt6** for the graphical user interface
- **SQLite** as the database engine
- **LangChain** and **Ollama** for LLM integration

## Getting Started

### Prerequisites

- Python 3.8 or higher
- SQLite3
- Required Python packages (see `requirements.txt`)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Pelphe/NL2SQL_Agent_With_Ollama_LangChain.git
    cd project-management-ai
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up the SQLite database:
    ```sh
    sqlite3 pro_mana.db < Project_Menegament.sql
    ```

4. Run the application:
    ```sh
    python AI.py
    ```

## Usage

- Ask questions about your projects, tasks, or team in natural language.
- The AI will generate and execute the appropriate SQL query, displaying results in the interface.
- Example queries:
    - "List all projects started in 2024."
    - "Show all tasks assigned to Fatma Kaya."
    - "Which customers have more than one project?"

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new features.

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please contact [your.email@example.com](mailto:m.salihcopur@gmail.com).
>>>>>>> 0739664 (İlk commit: Projeyi ve README dosyasını ekledim)
