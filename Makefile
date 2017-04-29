install:
	npm install

start:
	npm run babel-node -- 'src/bin/repassgen.js'

publish:
	npm publish

lint:
	npm run eslint
