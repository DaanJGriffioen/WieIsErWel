import http from "http";
import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

let hostname = "127.0.0.1"
let port = 8080

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const requestListener = async function(req, res){
    let contentType = 'text/html';
    let baseName = path.basename(req.url);
    const ext = path.extname(req.url);
    let filePath = "";
    

    switch(ext){
        case '.txt':
          // This is a bit hacky but works for now
          filePath = `/../src/files/logs/${baseName}`;
          contentType = 'text/plain; charset=UTF-8';
          break;
        case '.html':
          filePath = `/views/${baseName}`;
          contentType = 'text/html; charset=UTF-8';
          break;
        case '.js':
          filePath = `/scripts/${baseName}`;
          contentType = 'text/javascript/';
          break;
        case '.css':
          filePath = `/style/${baseName}`;
          contentType = 'text/css/';
          break;
        // Handle .ico like this for a while
        case '.ico':
          res.writeHead(204); // No Content
          res.end();
          return;
          
        default:
          contentType = 'text/html';
          filePath = `/views/index.html`;
          break;
      }

    console.log(`Request for ${req.url} received.`);
    console.log(__dirname + filePath);

    fs.readFile(__dirname + filePath)
    
    .then(contents => {
        res.setHeader("Content-Type", contentType);
        res.writeHead(200);
        res.end(contents);
    })
    .catch(err => {
        res.setHeader('Content-Type', 'text/plain');
        res.writeHead(404);
        console.log(err);
        res.end(`Error ${err}`);
    });
    return
}

const server = http.createServer(requestListener);

server.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
