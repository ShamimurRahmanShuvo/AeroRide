from fastapi import FastAPI

from app.core.database import Base, get_engine
from app.core.auth import create_demo_admin

from app.routes.aero_user_routes import router as aero_user_router
from app.routes.aero_admin_routes import router as aero_admin_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="AeroRide Application",
        version="1.0.0",
        description="AeroRide is a ride-sharing application that connects airport passengers with drivers for "
                    "convenient and efficient transportation.",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    app.include_router(aero_user_router)
    app.include_router(aero_admin_router)

    @app.on_event("startup")
    def on_startup():
        # Create database tables
        engine = get_engine()
        Base.metadata.create_all(bind=engine)
        # Create a demo admin user if it doesn't exist
        create_demo_admin()

    @app.get("/")
    def read_root():
        return {
            "message": "Welcome to AeroRide! Your go-to ride-sharing application for seamless airport transportation.",
            "version": "1.0.0",
            "description": "AeroRide is a ride-sharing application that connects airport passengers with drivers "
                           "for convenient and efficient transportation.",
            "docs_url": "/docs"
        }

    return app


app = create_app()
