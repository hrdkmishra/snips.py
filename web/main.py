from fastapi import FastAPI, UploadFile, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import sqlite3
import os
import random
import string
from datetime import datetime
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
from pygments import highlight

app = FastAPI()

if not os.path.exists("templates"):
    os.makedirs("templates")

templates = Jinja2Templates(directory="templates")

if not os.path.exists("temp"):
    os.makedirs("temp")

conn = sqlite3.connect("file_upload.db")
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS file_uploads (
        id INTEGER PRIMARY KEY,
        user_ip TEXT,
        file_id TEXT,
        file_lang TEXT,
        file_size TEXT,
        file_content TEXT,
        create_datetime DATETIME,
        update_datetime DATETIME
    )
"""
)
conn.commit()
conn.close()


def generate_file_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))


def get_file_language(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        lexer = guess_lexer(content)
        return lexer.name
    except Exception:
        return "Unknown"


def highlight_code(file_content, file_lang):
    try:
        lex = get_lexer_by_name(file_lang.lower())
        selected_style = get_style_by_name("nord-darker")
        formatter = HtmlFormatter(style=selected_style, full=True, linenos="table")
        line_numbers = formatter.get_style_defs(".linenos")
        highlighted_code = highlight(file_content, lex, formatter)
        return highlighted_code, line_numbers
    except Exception as e:
        return f"Code highlighting error: {str(e)}"


def format_file_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


@app.get("/")
async def home():
    return {"how to use snips.py? --> curl -X POST -F ""file=@filename"" http://127.0.0.1:8000/upload/"}


@app.post("/upload/")
async def upload_file(request: Request, file: UploadFile):
    try:
        user_ip = request.client.host

        file_id = generate_file_id()

        file_path = os.path.join("temp", file_id)
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        file_lang = get_file_language(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()

        file_size_bytes = os.path.getsize(file_path)
        file_size = format_file_size(file_size_bytes)

        conn = sqlite3.connect("file_upload.db")
        cursor = conn.cursor()
        current_datetime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        cursor.execute(
            """
            INSERT INTO file_uploads (user_ip, file_id, file_lang, file_size, file_content, create_datetime)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (user_ip, file_id, file_lang, file_size, file_content, current_datetime),
        )
        conn.commit()
        conn.close()

        os.remove(file_path)

        response_data = {
            "message": "File uploaded successfully",
            "file id": file_id,
            "file size": file_size,
            "file lang": file_lang,
            "url": f"http://127.0.0.1:8000/f/{file_id}",
        }

        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/f/{file_id}")
async def read_item(request: Request, file_id: str):
    conn = sqlite3.connect("file_upload.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT file_content,file_lang,file_size,create_datetime FROM file_uploads WHERE file_id=?", (file_id,)
    )
    file_data = cursor.fetchone()
    conn.close()

    if file_data:
        file_content = file_data[0]
        file_lang = file_data[1]
        file_size = file_data[2]
        create_datetime = file_data[3]
        highlighted_code, line_numbers = highlight_code(file_content, file_lang)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "file_content": highlighted_code,
            "line_numbers": line_numbers,
            "file_lang": file_lang.lower(),
            "file_size": file_size,
            "create_datetime": create_datetime,
            "file_id": file_id,
        }
        )
    