# install dependency uv
install-server:
	uv pip install -r pyproject.toml 

# run server
run-server:
	fastapi dev server/src/main.py

# install dependency node
install-client:
	npm install --prefix client

# run client
run-client:
	npm run dev --prefix client

# run both client and server
run-all:
	make run-server & make run-client
