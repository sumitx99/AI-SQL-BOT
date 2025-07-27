import os
import sqlite3
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

from langchain.memory import ConversationBufferMemory
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.agent_types import AgentType

load_dotenv()

app = Flask(__name__)

# LangChain setup
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0, convert_system_message_to_human=True)
db = SQLDatabase.from_uri("sqlite:///student.db")

memory = ConversationBufferMemory(memory_key="chat_history")

agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,
)

# Globals to store multiple chat threads
chat_threads = {}
current_thread_id = "thread-1"
thread_counter = 1

def store_message(role, text):
    if current_thread_id not in chat_threads:
        chat_threads[current_thread_id] = []
    chat_threads[current_thread_id].append({"role": role, "text": text})

def is_dml_query(prompt):
    dml_keywords = ["insert", "update", "delete", "add", "remove", "change", "create", "drop"]
    return any(keyword in prompt.lower() for keyword in dml_keywords)

def parse_comment_sql_output(output):
    """
    Parses LangChain's SQL output that contains comments with table info, e.g.:
    ... /* 3 rows from students table: id name age ... */
    Returns a dict with columns and rows for tabular display or None.
    """
    import re
    pattern = r"/\*\s*(\d+)\s+rows from \w+ table:\s*([\s\S]+)\*/"
    match = re.search(pattern, output)
    if not match:
        return None
    row_count = int(match.group(1))
    data_str = match.group(2).strip()

    # Split the data string into tokens
    tokens = data_str.split()
    # First tokens are column names (stop when next token matches data pattern)
    # The pattern: column names are all words until tokens start to look like data (a mix of digits or names)
    # But since format is fixed, the columns are all tokens before the first number that matches a row id
    # We'll assume first token with digit is the start of data rows
    col_names = []
    for i, token in enumerate(tokens):
        if token.isdigit():
            col_names = tokens[:i]
            data_tokens = tokens[i:]
            break
    else:
        # No digit found? fallback all as columns (unlikely)
        col_names = tokens
        data_tokens = []

    # Now split data tokens into rows with len = len(col_names)
    rows = []
    for i in range(0, len(data_tokens), len(col_names)):
        row = data_tokens[i:i+len(col_names)]
        if len(row) == len(col_names):
            rows.append(row)

    return {"columns": col_names, "rows": rows}

@app.route("/")
def home():
    memory.clear()
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    global current_thread_id
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    store_message("user", prompt)

    try:
        if is_dml_query(prompt):
            from langchain.chains import create_sql_query_chain
            query_chain = create_sql_query_chain(llm, db)
            sql_query = query_chain.invoke({"question": prompt})
            return jsonify({"requires_confirmation": True, "sql": sql_query.strip()})
        else:
            result = agent_executor.invoke({"input": prompt})
            output = result.get("output", "")
            store_message("bot", output)

            table_data = parse_comment_sql_output(output)
            return jsonify({"answer": output, "table": table_data})
    except Exception as e:
        return jsonify({"answer": f"Error: {e}"}), 500

@app.route("/execute_dml", methods=["POST"])
def execute_dml():
    global current_thread_id
    data = request.get_json()
    sql = data.get("sql")
    if not sql:
        return jsonify({"error": "No SQL provided"}), 400

    try:
        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        store_message("bot", "Success! The operation was completed.")
        return jsonify({"result": "Success! The operation was completed."})
    except Exception as e:
        store_message("bot", f"Error executing command: {e}")
        return jsonify({"result": f"Error executing command: {e}"}), 500

@app.route("/reset", methods=["POST"])
def reset():
    global current_thread_id, thread_counter
    memory.clear()
    thread_counter += 1
    current_thread_id = f"thread-{thread_counter}"
    return jsonify({"status": "new_thread", "thread_id": current_thread_id})

@app.route("/history", methods=["GET"])
def history():
    return jsonify({"threads": list(chat_threads.keys())})

@app.route("/load_thread", methods=["POST"])
def load_thread():
    global current_thread_id
    thread_id = request.json.get("thread_id")
    if thread_id in chat_threads:
        current_thread_id = thread_id
        return jsonify({"messages": chat_threads[thread_id]})
    return jsonify({"error": "Thread not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
