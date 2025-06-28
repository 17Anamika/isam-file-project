import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

class ISAMFile:
    def __init__(self, filename: str):
        self.filename = filename
        self.index = {}
        self._build_index()

    def _write_to_file(self, record: str):
        with open(self.filename, 'a') as f:
            f.write(record + '\n')

    def _read_from_file(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as f:
            return f.readlines()

    def _update_index(self, key: str, offset: int):
        self.index[key] = offset
        
    def _build_index(self):
        self.index = {}
        records = self._read_from_file()
        offset = 0
        for record in records:
            key = record.split(',')[0]
            self._update_index(key, offset)
            offset += len(record)

    def insert_record(self, key: str, data: Dict[str, str]):
        if key in self.index:
            raise ValueError("Record with key already exists.")
        record = f"{key},{data['name']},{data['roll_no']},{data['email']},{data['marks']}"
        self._write_to_file(record)
        self._update_index(key, os.path.getsize(self.filename) - len(record) - 1)

    def search_record(self, key: str):
        if key not in self.index:
            raise KeyError("Record not found.")
        with open(self.filename, 'r') as f:
            f.seek(self.index[key])
            record = f.readline().strip()
        return record

    def search_records_by_name_prefix(self, prefix: str):
        records = self._read_from_file()
        matching_records = []
        for record in records:
            if record.split(',')[1].startswith(prefix):
                matching_records.append(record.strip())
        return matching_records
    
    def search_records_by_marks_range(self, min_marks: float, max_marks: float):
        records = self._read_from_file()
        matching_records = []
        for record in records:
            marks = float(record.split(',')[4])
            if min_marks <= marks <= max_marks:
                matching_records.append(record.strip())
        return matching_records
    

    def search_records_by_email(self, query: str):
        records = self._read_from_file()
        matching_records = []
        for record in records:
            email = record.split(',')[3]
            if query in email:
                matching_records.append(record.strip())
        return matching_records
    
    def search_records_by_roll_no(self, query: str):
        records = self._read_from_file()
        matching_records = []
        for record in records:
            roll_no = record.split(',')[2]
            if query in roll_no:
                matching_records.append(record.strip())
        return matching_records

    def delete_record(self, key: str):
        if key not in self.index:
            raise KeyError("Record not found.")
        records = self._read_from_file()
        with open(self.filename, 'w') as f:
            for record in records:
                if record.split(',')[0] != key:
                    f.write(record)
        self._build_index()

    def update_record(self, key: str, new_data: Dict[str, str]):
        if key not in self.index:
            raise KeyError("Record not found.")
        self.delete_record(key)
        self.insert_record(key, new_data)



app = FastAPI()
filename = 'isamfile.txt'
isam = ISAMFile(filename)

class Record(BaseModel):
    name: str
    roll_no: str
    email: str
    marks: float

@app.post("/insert/{key}")
def insert_record(key: str, record: Record):
    try:
        isam.insert_record(key, record.dict())
        return {"message": "Record inserted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/search/{key}")
def search_record(key: str):
    try:
        record = isam.search_record(key)
        return {"record": record}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/search_by_name/{prefix}")
def search_records_by_name_prefix(prefix: str):
    try:
        matching_records = isam.search_records_by_name_prefix(prefix)
        if not matching_records:
            raise HTTPException(status_code=404, detail="No records found.")
        return {"records": matching_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/search_by_marks/{min_marks},{max_marks}")
def search_records_by_marks_range(min_marks: float, max_marks: float):
    try:
        matching_records = isam.search_records_by_marks_range(min_marks, max_marks)
        if not matching_records:
            raise HTTPException(status_code=404, detail="No records found within the specified marks range.")
        return {"records": matching_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/search_by_email/{query}")
def search_records_by_email(query: str):
    try:
        matching_records = isam.search_records_by_email(query)
        if not matching_records:
            raise HTTPException(status_code=404, detail="No records found with the specified email query.")
        return {"records": matching_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/search_by_roll_no/{query}")
def search_records_by_roll_no(query: str):
    try:
        matching_records = isam.search_records_by_roll_no(query)
        if not matching_records:
            raise HTTPException(status_code=404, detail="No records found with the specified roll number query.")
        return {"records": matching_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete/{key}")
def delete_record(key: str):
    try:
        isam.delete_record(key)
        return {"message": "Record deleted successfully"}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.put("/update/{key}")
def update_record(key: str, new_record: Record):
    try:
        isam.update_record(key, new_record.dict())
        return {"message": "Record updated successfully"}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run("main:app", host="0.0.0.0", port = 8000 , log_level="debug")

    