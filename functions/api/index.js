const express = require("express");

const PORT = 3000;
// const PSACLE_USERNAME = '';
// const PSACLE_PASSWORD = '';
// const PSACLE_HOST = '';
// const PSACLE_DATABASE = '';

const app = express();
app.use(express.json());

app.post("/", function (req, res) {
    const data = (req.body);
    console.log(data);
    res.send(`Data received: ${JSON.stringify(data)}`);
});

app.listen(PORT, function (err) {
    console.log(`Server is running on: ${PORT}`);
    if (err) {
        console.log(err);
    }
    return;
});
