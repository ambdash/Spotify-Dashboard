from application import app
import main as mp

app.layout = mp.layout

if __name__ == '__main__':
    app.run_server(debug=False)
