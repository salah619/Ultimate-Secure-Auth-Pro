from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

# استيرادات المشروع الأساسية
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine

# 1. إعداد قاعدة البيانات وإنشاء الجداول تلقائياً
try:
    # نستورد الموديلات لكي يعرف SQLAlchemy الجداول المطلوبة
    from app.models.models import User, AuditLog
    # أمر إنشاء الجداول في ملف SQLite
    User.metadata.create_all(bind=engine)
    print("✅ Database Tables (users, audit_log) created successfully!")
except Exception as e:
    print(f"⚠️ Database Setup Notice: {e}")

# 2. تعريف تطبيق FastAPI
app = FastAPI(
    title="Ultimate Secure Auth Pro",
    docs_url=None, # معطل لاستخدام الروابط السريعة بالأسفل
    redoc_url=None
)

# 3. واجهة Swagger UI (روابط سريعة لتجنب الشاشة البيضاء)
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.9.0/swagger-ui.css",
    )

# 4. واجهة ReDoc
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://cdnjs.cloudflare.com/ajax/libs/redoc/2.1.3/redoc.standalone.js",
    )

# 5. Middleware للأمان (Security Headers)
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        # تم تعديل الـ CSP للسماح بتحميل ملفات الـ UI الخارجية في تيرمكس
        response.headers["Content-Security-Policy"] = "default-src * 'unsafe-inline' 'unsafe-eval'; img-src * data:; style-src * 'unsafe-inline';"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# 6. إعدادات الـ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 7. ربط الراوتر الأساسي (Endpoints)
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to Ultimate-Secure-Auth-Pro API (Running on Termux)"}

