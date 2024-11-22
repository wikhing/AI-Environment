const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const app = express();
const port = 3000;

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));

// Route to serve the SnakeGame.html file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'SnakeGame.html'));
});

// Route to save the JSON data
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

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});