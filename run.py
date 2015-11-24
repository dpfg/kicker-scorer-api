from app import app
import config

app.debug = config.DEBUG_MODE
app.run()
