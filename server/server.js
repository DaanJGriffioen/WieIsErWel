import http from "http";
import { promises as fs } from 'fs';
import path, { basename } from 'path';

let hostname = "127.0.0.1"
let port = 8080


const requestListener = async function(req, res){
    let contentType = 'text/html';
    let __filename = "table.html"
    const __dirname = path.dirname(__filename);
    fs.readFile("./table.html")
    .then(contents => {
        res.setHeader("Content-Type", contentType);
        res.writeHead(200);
        res.end(contents);
    })
    .catch(err => {
        res.setHeader('Content-Type', 'text/plain');
        res.writeHead(500);
        console.log(err);
        res.end(`Error ${err}`);
    });
    return
}

const server = http.createServer(requestListener);

server.listen(port, () => {
  console.log(`Server is running on http://${hostname}:${port}`);
});
