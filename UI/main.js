const express = require('express');
const http = require('http');
const path = require('path');
const deepl = require('deepl-node');

const authKey = "017bb4a0-954d-54c9-09fd-30e123255439:fx"; //process.env['DEEPL_AUTH_KEY'];
const serverUrl = "https://api-free.deepl.com/"; //process.env['DEEPL_SERVER_URL'];
const translator = new deepl.Translator(authKey, { serverUrl: serverUrl });



// Body-parser used to expose data in POST requests
var bodyparser = require('body-parser')
// The data is 'urlencoded', so use that middleware
var urlparser = bodyparser.urlencoded({ extended: false })

const port = 3000; // process.env['PORT']

const app = express();
const server = http.createServer(app);

app.use(express.static(path.join(__dirname, 'public')));

// Route that responds to GET requests with our html page
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

// Route that responds to POST requests to '/user'
app.post('/translate', urlparser, (req, res) => {
    // Syntax is req.body.[name], where [name] is the attribute we want data of.
    //res.send("<html>Hello, "+req.body.username+"!<html>")


    // Handle the incoming POST request here
    const text = req.body.text;
    var target_lang = req.body.target_lang;
    if (target_lang == 'en') {
        target_lang = 'en-GB'
    } else if (target_lang == 'pt') {
        target_lang = 'pt-PT'
    }
    // You can now process the text and target_lang parameters and return a response
    // to the client using res.send()


    translator
        .getUsage()
        .then((usage) => {
            console.log(usage);
            return translator.translateText(text, null, target_lang);
        })
        .then((result) => {
            const translatedText = result.text;
            console.log(translatedText);
            res.send(result)
        })
        .catch((error) => {
            console.error(error);
            res.status(500).send({ error: 'An error occurred while translating the text.' });
            process.exit(1);
        });


    // translator.translateText(text, null, target_lang)
    // .then((result) => {
    //   const translatedText = result.text;
    //   res.send({ translatedText });
    // })
    // .catch((error) => {
    //   console.error(error);
    //   res.status(500).send({ error: 'An error occurred while translating the text.' });
    // });

    console.log("\n\n req.body is:  \n\n", req.body);

});

server.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
