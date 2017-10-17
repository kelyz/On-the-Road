from app import app

app.secret_key = os.environ['app.secret_key']

if __name__ == "__main__":
	# app.run(host='0.0.0.0', port=5000)