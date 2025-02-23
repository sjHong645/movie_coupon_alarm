from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

from database import SessionLocal
from sqlalchemy import text

session = SessionLocal()

app = FastAPI()

# 현재 디렉토리의 templates 폴더를 참조하도록 설정
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):

    # DB에 저장된 내용을 가져온다.
    result = session.execute(text("SELECT * FROM lottecinema_event_list")).fetchall()

    movies = {} 
    for movie in result :
        movies[movie[0]] = movie[1].strftime("%m-%d %H시")


    return templates.TemplateResponse("index.html", {"request": request, "movies" : movies})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000, reload = True)