import dash
import config as cfg

app = dash.Dash(cfg.APP_NAME, suppress_callback_exceptions=True)
app.title = cfg.APP_TITLE
