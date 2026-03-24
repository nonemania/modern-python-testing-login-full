from __future__ import annotations

from fastapi import FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.auth import authenticate, validate_login_input

app = FastAPI(title="Modern Python Testing Login Demo", version="1.0.0")
templates = Jinja2Templates(directory="app/templates")


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, description="Login username")
    password: str = Field(..., min_length=4, max_length=20, description="Login password")


class LoginResponse(BaseModel):
    message: str
    token: str


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    # Temporary fix for Jinja2/Python 3.14 compatibility issue
    simple_login_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login Demo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f6f7fb; }
            .card { max-width: 420px; margin: 80px auto; background: white; border-radius: 12px; 
                   box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08); padding: 24px; }
            .form-group { margin-bottom: 16px; }
            label { display: block; margin-bottom: 8px; font-weight: bold; }
            input[type="text"], input[type="password"] { width: 100%; padding: 12px; border: 1px solid #ddd; 
                                                        border-radius: 8px; box-sizing: border-box; }
            button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; 
                    border-radius: 8px; cursor: pointer; font-size: 16px; }
            button:hover { background: #0056b3; }
            .error { color: red; margin-bottom: 16px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Login Demo</h1>
            <form method="post" action="/login">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(simple_login_html)


@app.post("/login", response_class=HTMLResponse, include_in_schema=False)
def login_page(request: Request, username: str = Form(...), password: str = Form(...)):
    if validate_login_input(username, password) and authenticate(username, password):
        return HTMLResponse("<h1>Dashboard</h1><p>Welcome admin</p>")

    # Error case - return login form with error message
    error_login_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login Demo</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f6f7fb; }}
            .card {{ max-width: 420px; margin: 80px auto; background: white; border-radius: 12px; 
                   box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08); padding: 24px; }}
            .form-group {{ margin-bottom: 16px; }}
            label {{ display: block; margin-bottom: 8px; font-weight: bold; }}
            input[type="text"], input[type="password"] {{ width: 100%; padding: 12px; border: 1px solid #ddd; 
                                                        border-radius: 8px; box-sizing: border-box; }}
            button {{ width: 100%; padding: 12px; background: #007bff; color: white; border: none; 
                    border-radius: 8px; cursor: pointer; font-size: 16px; }}
            button:hover {{ background: #0056b3; }}
            .error {{ color: red; margin-bottom: 16px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Login Demo</h1>
            <div id="error" class="error">Invalid credentials</div>
            <form method="post" action="/login">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" value="{username}" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(error_login_html, status_code=status.HTTP_401_UNAUTHORIZED)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post(
    "/api/login",
    response_model=LoginResponse,
    responses={400: {"description": "Invalid input"}, 401: {"description": "Invalid credentials"}},
)
def api_login(payload: LoginRequest):
    if not validate_login_input(payload.username, payload.password):
        raise HTTPException(status_code=400, detail="invalid input")

    if not authenticate(payload.username, payload.password):
        raise HTTPException(status_code=401, detail="invalid credentials")

    return LoginResponse(message="login success", token="fake-jwt-token")
