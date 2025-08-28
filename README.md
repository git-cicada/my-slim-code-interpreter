# 🐍 My Slim Code Interpreter

This project is a lightweight **LangChain-based Python code interpreter** that combines two agents:

1. **Python Agent** – Executes Python code in a safe REPL environment.  
2. **CSV Agent** – Analyzes CSV files and extracts insights.  

Both are routed through a **Router Agent**, which decides which tool to use based on the user’s query.

---

## 🚀 Features

- ✅ Run Python code safely inside a REPL environment.  
- ✅ Generate outputs, explanations, and summaries in plain English.  
- ✅ Analyze CSV files with natural language queries.  
- ✅ Router Agent automatically decides whether to use Python or CSV analysis.  
- ✅ Error handling with `handle_parsing_errors=True`.  
- ⚠️ Dangerous code execution is disabled by default (except explicitly allowed in CSV Agent).  

---

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/my-slim-code-interpreter.git
cd my-slim-code-interpreter
pipenv shell
pipenv install
```

## Sample Ouput for 
![alt text](QRCode1.png)
