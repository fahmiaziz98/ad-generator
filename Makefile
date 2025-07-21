# run server
run-server:
	uvicorn server.src.main:app --reload --host 0.0.0.0 --port 8000

# run client
run-client:
	npm run dev --prefix client

# run both client and server
run-all:
	make run-server & make run-client