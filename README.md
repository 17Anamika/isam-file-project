# 📁 ISAM File Management System using FastAPI

This project is a mini *database management system* built using Python and FastAPI. It implements the *Indexed Sequential Access Method (ISAM)* to efficiently manage student records stored in a text file.


## 🚀 Objective

Build a file-based data management system using *ISAM* that supports:
- Insert a record
- Search for a record
- Delete a record
- Update a record
- Advanced queries like search by name, roll number, email, or marks

---

⚙ Technologies Used

- *Python 3.11*
- *FastAPI* – for building web APIs
- *Pydantic* – for data validation
- *OS module* – for file operations

---

📄 Features:
- Store and manage student records in a file
- Search records by name,roll no,marks,email
- Perform operations using web API(FastAPI)

✅ Core Functions:
- Insert new record to file
- Read all records
- Update/delete records by key
- Maintain an in-memory index for fast access
  
🔍 Advanced Search:
- Search by *name prefix*
- Search by *marks range*
- Search by *email* or *roll number* pattern

  How to Run the project
1. Install reuired libraries
2. Run the FastAPI app
3. Open the browser and go to:
   https://127.0.0.1:8000


🛠 File Structure
- Isamfile project.py(ISAMFile class and file operations)
- main.py(FastApi endpoints setup)
- isamfile.txt(Storage file for records)
- README.md(Project description)

 👩‍💻 Author
 Anamika Mishra
 Internship Project- August2024
 GitHub:@17Anamika
