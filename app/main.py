from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from .auth import create_access_token, decode_access_token, hash_password, verify_password
from .database import Base, engine, get_db
from .models import Publication, User

app = FastAPI(title="maqola.tj")
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")



def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    return db.get(User, int(user_id))


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db), current_user: User | None = Depends(get_current_user)):
    publications = db.scalars(select(Publication).order_by(Publication.created_at.desc())).all()
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "publications": publications, "current_user": current_user},
    )


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request, current_user: User | None = Depends(get_current_user)):
    if current_user:
        return RedirectResponse("/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("register.html", {"request": request, "error": None, "current_user": current_user})


@app.post("/register", response_class=HTMLResponse)
def register(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    existing_user = db.scalar(select(User).where(User.email == email.lower().strip()))
    if existing_user:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Пользователь с таким email уже существует", "current_user": None},
            status_code=400,
        )

    user = User(full_name=full_name.strip(), email=email.lower().strip(), hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)

    response = RedirectResponse("/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", token, httponly=True, samesite="lax", max_age=86400)
    return response


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, current_user: User | None = Depends(get_current_user)):
    if current_user:
        return RedirectResponse("/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("login.html", {"request": request, "error": None, "current_user": current_user})


@app.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.scalar(select(User).where(User.email == email.lower().strip()))
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Неверный email или пароль", "current_user": None},
            status_code=401,
        )

    response = RedirectResponse("/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", token, httponly=True, samesite="lax", max_age=86400)
    return response


@app.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db), current_user: User | None = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

    publications = db.scalars(
        select(Publication).where(Publication.author_id == current_user.id).order_by(Publication.created_at.desc())
    ).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "current_user": current_user, "publications": publications},
    )


@app.get("/publications/new", response_class=HTMLResponse)
def new_publication_page(request: Request, current_user: User | None = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("new_publication.html", {"request": request, "current_user": current_user})


@app.post("/publications/new")
def create_publication(
    request: Request,
    title: str = Form(...),
    category: str = Form(...),
    annotation: str = Form(...),
    content: str = Form(...),
    current_user: User | None = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Необходима авторизация")

    publication = Publication(
        title=title.strip(),
        category=category.strip() or "Образование",
        annotation=annotation.strip(),
        content=content.strip(),
        author_id=current_user.id,
    )
    db.add(publication)
    db.commit()
    db.refresh(publication)

    return RedirectResponse(f"/publications/{publication.id}", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/publications/{publication_id}", response_class=HTMLResponse)
def publication_detail(
    publication_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user),
):
    publication = db.get(Publication, publication_id)
    if not publication:
        raise HTTPException(status_code=404, detail="Публикация не найдена")
    return templates.TemplateResponse(
        "publication_detail.html",
        {"request": request, "publication": publication, "current_user": current_user},
    )
