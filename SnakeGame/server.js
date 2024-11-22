const express = require('express');
const bodyParser = require('body-parser');
import * as fs from 'node:fs/promises';
const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post('/save', (req, res) => {
    const jsonContent = JSON.stringify(req.body);
    fs.writeFile('snake_data.json', jsonContent, 'utf8', (err) => {
        if (err) {
            res.status(500).send('Error saving file');
            return;
        }
        res.send('File saved successfully');
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});