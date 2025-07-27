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

  <img src="https://i.ibb.co/DSwPJNG/Screenshot-2025-07-27-222941.png" alt="App Screenshot" style="max-width: 100%; height: auto;">

</div>

## 🛠️ Tech Stack

- **Frontend**: HTML + CSS + JavaScript  
- **Backend**: Python (Flask)  
- **LLM**: Google Gemini via LangChain  
- **Database**: SQLite  
- **Deployment**: Vercel or Flask local server

---
