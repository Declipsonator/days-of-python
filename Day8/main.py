# run with python -m uvicorn main:app --reload
import time
from fastapi import FastAPI, UploadFile
import json
import os
import csv
import uuid
from fastapi.responses import FileResponse

app = FastAPI()


def csv_to_column_array(csv_matrix, headers, columns):
    if columns:
        csv_matrix = list(zip(*csv_matrix))

    output_data = csv_matrix
    if headers:
        new_array = []
        for data_array in csv_matrix[1:]:
            data_dict = {}
            for element in range(0, len(data_array)):
                if csv_matrix[0][element]:
                    data_dict[csv_matrix[0][element]] = data_array[element]
                else:
                    data_dict[element] = data_array[element]
            new_array.append(data_dict)

        output_data = new_array

    return output_data


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/csv_to_json")
async def csv_to_json(file: UploadFile, noheaders: bool = False, columns: bool = False, delimiter: str = ","):
    # Clear old outputs
    for filename in os.listdir():
        # Clear if older than 30 seconds and is a json file
        if filename.endswith(".json") and (time.time() - os.path.getmtime(filename)) > 10:
            os.remove(filename)

    if os.path.splitext(file.filename)[-1] != '.csv':
        return {"message": "Invalid input file, please supply a real csv file"}
    else:
        content = str(await file.read()).replace('\\r', '\r').replace('\\n', '\n').removeprefix("b'").split("\n")
        csv_reader = csv.reader(content, delimiter=delimiter)
        table = [row for row in csv_reader]

        output_data = csv_to_column_array(table, not noheaders, columns)

        output_filename = str(uuid.uuid4()) + ".json"
        with open(output_filename, 'w') as f:
            json.dump(output_data, f)

    return FileResponse(output_filename)
