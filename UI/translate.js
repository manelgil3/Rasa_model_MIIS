const deepl = require('deepl-node');

const authKey = "017bb4a0-954d-54c9-09fd-30e123255439:fx"; //process.env['DEEPL_AUTH_KEY'];
const serverUrl = "https://api-free.deepl.com/"; //process.env['DEEPL_SERVER_URL'];
const translator = new deepl.Translator(authKey, { serverUrl: serverUrl });

translator
    .getUsage()
    .then((usage) => {
        console.log(usage);
        return translator.translateText('Hola que tal? Espero que este muy bien :P', null, 'en-GB');
    })
    .then((result) => {
        console.log(result.text); // Bonjour, le monde !
    })
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });

module.exports={translator}