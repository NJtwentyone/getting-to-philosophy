# getting-to-philosophy
[Interview code example] Your goal is to build a full-stack app that takes a Wikipedia URL as input, and display the path taken from clicking the first link of each page until you get to the Philosophy article. This app should have a front-end form that interacts with a back-end API you’ve built, and it should store the paths taken in a database you’ve designed.

installation configuration notes:
1)Install Node.js
  $ brew install node
  -- reference: https://www.dyclassroom.com/howto-mac/how-to-install-nodejs-and-npm-on-mac-using-homebrew
2) created next.js app
  npx create-react-app philosophy-webapp
  -- reference: https://github.com/facebook/create-react-app

server commands:
Success! Created philosophy-webapp at /Users/njtwentyone/code_sandbox/bento/getting-to-philosophy/philosophy-webapp
Inside that directory, you can run several commands:

  npm start
    Starts the development server.

  npm run build
    Bundles the app into static files for production.

  npm test
    Starts the test runner.

  npm run eject
    Removes this tool and copies build dependencies, configuration files
    and scripts into the app directory. If you do this, you can’t go back!

We suggest that you begin by typing:

  cd philosophy-webapp
  npm start

3) node modules:
npm install ava -g
ava --init
npm install sinon --save-dev

4) how to install babel
https://semaphoreci.com/community/tutorials/getting-started-with-create-react-app-and-ava
then add .babrlrc with
{
  "presets": ["env"]
}
5) install logging
npm install winston-loggly-bulk
6) how to setup backend api
https://medium.freecodecamp.org/how-to-make-create-react-app-work-with-a-node-backend-api-7c5c48acb1b0
 - had to cd to backend dir and runn
 - npm install --save hapi@17.x.x

7) npm install axios

8) in backend
npm install --save babel-core babel-preset-es2015  babel-preset-es2017
update babel as in step 4
 -- ref https://scotch.io/tutorials/getting-started-with-hapi-js

 9) xml
 npm install xpath -g --save
 npm install xmldom -g --save
