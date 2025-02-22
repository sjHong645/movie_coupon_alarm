from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()

# 영화 데이터 
movies = {
    '퇴마록': '02-11 14시',
    '그 시절, 우리가 좋아했던 소녀': '02-12 11시',
    '고백': '02-17 11시',
    '패딩턴: 페루에 가다!': '02-24 16시',
    '써니데이': '02-17 16시',
    '데드데드 데몬즈 디디디디 디스트럭션: 파트2': '02-21 11시',
    '[15주년]500일의 썸머': '02-21 14시',
    '괜찮아 괜찮아 괜찮아!': '02-24 11시',
    '캔터빌의 유령': '02-24 14시'
}

# 현재 디렉토리의 templates 폴더를 참조하도록 설정
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "movies" : movies})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000, reload = True)