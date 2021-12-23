# Make commands for development
# 
# `make run` runs the development server, listening on port 4000.

NPM=npm

devserver: package-lock.json
	node_modules/.bin/nodemon server.js

package-lock.json: package.json
	$(NPM) install
