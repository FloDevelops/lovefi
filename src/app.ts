import express, { Request, Response } from 'express';
var Twig = require("twig");

const app = express();
const port = process.env.PORT || 3000;

// This section is optional and used to configure twig.
app.set("twig options", {
    allowAsync: true, // Allow asynchronous compiling
    strict_variables: false
});

app.get('/', function(req, res) {
    res.render('index.twig', {
        message : "Hello World"
    });
});

app.get('/login', function(req, res) {
    res.render('base.twig', {
        message : "This is the login page"
    });
});

app.get('/api/v1/login', function (req: Request, res: Response) {
    res.send('Login');
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
