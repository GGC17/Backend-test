from app import app as application

# Start terminal for requests
app = application


if __name__ == "__main__":
    app.run(host='0.0.0.0')