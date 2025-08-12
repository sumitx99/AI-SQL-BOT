# 🧠 AI SQL Assistant

An AI-powered SQL assistant that allows you to interact with your database using natural language prompts. No need to remember complex SQL queries—just type what you want, and the AI does the rest!

![1_BzUPMYwp_bMx8z1BVnWkbw](https://github.com/user-attachments/assets/ca1c73b5-63a8-4eca-b951-e290982bfafc)

---

## 📌 Features

- 💬 **Prompt-Based Querying**  
  Interact with your database using simple English prompts.  
  Example:  
  - `"Add a new employee named Atul"`  
  - `"Update the contact number of Rohan to 9876543210"`

- 🧠 **Powered by Gemini + LangChain**  
  Uses Google Gemini (via LangChain) to convert prompts into SQL statements.

- 🗃️ **SQLite Integration**  
  Works seamlessly with an existing or new SQLite database. Easy to plug and play.

- 📊 **Formatted Tabular Output**  
  Select queries return results in a clean, readable HTML table.

- 🚨 **DML Safety Confirmation**  
  Prompts you before running `INSERT`, `UPDATE`, `DELETE`, or `CREATE` queries to prevent accidental changes.

- 🗂️ **Chat Threading + History Sidebar**  
  Create new chat sessions and store each session’s history in an organized sidebar.

---


## 🖥️ UI Demo

<div align="center">

  <img src="https://i.ibb.co/HDTDcGm4/Screenshot-2025-07-27-222941.png" alt="App Screenshot" style="max-width: 200%; height: auto;">

</div>

## 🛠️ Tech Stack

- **Frontend**: HTML + CSS + JavaScript  
- **Backend**: Python (Flask)  
- **LLM**: Google Gemini via LangChain  
- **Database**: SQLite  
- **Deployment**: Vercel or Flask local server

---
> # Agent

### agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
- AgentType: This is an enumeration from LangChain that lists the different pre-built agent architectures you can use.
 - ZERO_SHOT: This term means the agent is not given any specific examples of how to solve a problem beforehand. It must rely on its general knowledge and the descriptions of the "tools" it has access to (in this case, the database schema) to figure out what to do. It's like giving a skilled chef a box of ingredients they've never seen together and asking them to make a dish—they use their fundamental cooking knowledge to succeed.
 - REACT: This is an acronym for a framework called "Reason and Act." It's a powerful prompting strategy where the agent follows a specific loop to solve problems:
 - Thought: The agent first thinks about what it needs to do to answer the user's prompt.
 - Action: Based on its thought, it decides to take an action. For a SQL agent, the primary action is to use its "SQL tool" to write and execute a query.
 - Observation: The agent observes the result (or error) of its action.
The agent repeats this cycle. It looks at the new observation and thinks about the next step until it has the final answer.
 - DESCRIPTION: This part signifies that the agent heavily relies on the descriptions of the tools it can use. For your SQL agent, it means the agent is given the database schema (table names, column names, types, and relationships) as its "tool description." It uses this description to reason about how to construct a valid SQL query.

> # Working

| Responsibility | Who Does It? | How? |
| :--- | :--- | :--- |
| Understanding the user's question | Gemini | Natural Language Understanding (NLU) |
| Connecting to the database | LangChain | Using the `SQLDatabase` utility |
| Describing the database schema | LangChain | Inspects the DB and formats a text description |
| Planning how to answer | Gemini | The "Thought" step in the ReAct framework |
| Generating the SQL query | Gemini | Code generation based on the schema and prompt |
| Executing the SQL query | LangChain | Using its `SQLDatabase` tool to run the query |
| Remembering the conversation | LangChain | Using the `ConversationBufferMemory` module |
| Interpreting the SQL result | Gemini | Understands that `[(15,)]` means the number 15 |
| Formulating the final answer | Gemini | Natural Language Generation (NLG) |
| Managing the entire workflow | LangChain | The `agent_executor` orchestrates the entire loop |
