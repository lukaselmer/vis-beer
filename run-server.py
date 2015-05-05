from visbeer.server import app

if app.config['ApiKey'] is None or len(app.config['ApiKey']) < 15:
    raise RuntimeError('No api key given or api key is too short. '
                       'Use the env variable API_KEY to supply a valid api key.')
app.run(debug=True)
