from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="AeroRide Application",
        version="1.0.0",
        description="AeroRide is a ride-sharing application that connects airport passengers with drivers for "
                    "convenient and efficient transportation.",
        docs_url="/docs",
        redoc_url="/redoc"
    )

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
