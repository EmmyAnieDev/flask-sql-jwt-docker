from create_app_file import create_app


app = create_app()


@app.route('/')
def welcome():
    return 'Welcome to our store!'


if __name__ == '__main__':
    app.run(debug=True, port=5001)