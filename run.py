from app import app

if __name__ == "__main__":
	app.secret_key = os.environ['app.secret_key']
	app.run(host='0.0.0.0', port=5000)