from app import app, db
from app.models import Match

@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Match": Match}
