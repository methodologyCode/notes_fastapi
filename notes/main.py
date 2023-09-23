import os

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from schemas import Note, NoteID
from security import get_note_id
from db.service import SQLService

app = FastAPI()
templates = Jinja2Templates(directory="templates")

path_to_static = os.path.join(os.path.dirname(__file__), 'static')
app.mount("/static", StaticFiles(directory=path_to_static), name="static")


@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
    })


@app.get("/give-note", response_class=HTMLResponse)
async def get_note_page(request: Request):
    return templates.TemplateResponse("give_note.html", {
        "request": request,
    })


@app.post("/create_note", status_code=status.HTTP_201_CREATED)
async def send_notes(note_data: Note):
    note_id = get_note_id(text=note_data.text, salt=note_data.secret)
    result = await SQLService.add(text=note_data.text, secret=note_data.secret,
                                  note_hash=note_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Bad request")

    return {"response": "ok", "note_id": note_id}


@app.get("/result/{note_id}", response_class=HTMLResponse)
async def get_result_id(request: Request, note_id: str):
    return templates.TemplateResponse("hash_storage.html", {
        "request": request,
        "note_id": note_id
    })


@app.post("/get_note", status_code=status.HTTP_200_OK)
async def get_note(note_data: NoteID):
    note = await SQLService.find_one_or_none(note_hash=note_data.note_id,
                                             secret=note_data.note_secret)

    if note is None:    
        return {"response": "ok", "note_final_text": "Such a note does not exist"}
    
    await SQLService.delete(note_hash=note_data.note_id, secret=note_data.note_secret)
    return {"response": "ok", "note_final_text": note.text}


@app.get("/note_page/{note_text}", response_class=HTMLResponse)
async def get_result_note(request: Request, note_text: str):
    return templates.TemplateResponse("note_page.html", {
        "request": request,
        "note_text": note_text
    })