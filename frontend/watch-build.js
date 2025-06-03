// watch-build.js
const chokidar = require('chokidar');
const { exec } = require('child_process');

chokidar.watch('./data/blog/**/*.mdx', { ignoreInitial: true })
  .on('all', (event, path) => {
    console.log(`Detected ${event} in ${path}, triggering build...`);
    exec('yarn build', (err, stdout, stderr) => {
      if (err) console.error(stderr);
      else console.log(stdout);
    });
  });

console.log('Watching MDX files...');