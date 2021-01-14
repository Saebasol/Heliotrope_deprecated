import os
from Heliotrope.app import app

app.run(
    host="0.0.0.0", port=int(os.environ["PORT"]) if os.environ.get("PORT") else 8000
)
