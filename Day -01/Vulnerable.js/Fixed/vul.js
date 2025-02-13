const express = require('express');
const { spawn } = require('child_process');
 
const app = express();
app.use(express.json());
 
app.post('/ping', (req, res) => {
    const host = req.body.host;
 
    if (!/^[a-zA-Z0-9.\-]+$/.test(host)) {
        return res.status(400).send("Invalid host input.");
    }
    const ping = spawn('ping', ['-c', '4', host]);
 
    let output = '';
 
    ping.stdout.on('data', (data) => {
        output += data.toString();
    });
 
    ping.stderr.on('data', (data) => {
        output += data.toString();
    });
 
    ping.on('close', (code) => {
        res.send(`<pre>${output}</pre>`);
    });
});
 
app.listen(3000, () => console.log('Server running on port 3000'));