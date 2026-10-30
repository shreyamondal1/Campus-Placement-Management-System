from app.main import create_app, init_db

app = create_app()

init_db(app)

if __name__ == "__main__":
    
    app.run(host="127.0.0.1", port=5000, debug=True)
