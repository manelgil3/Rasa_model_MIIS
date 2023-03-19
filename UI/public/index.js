const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
const msgerAudioBtn = document.querySelector('.msger-audio-btn');
// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "https://www.upf.edu/documents/7283915/220614254/UPFt_rgb.png";
const PERSON_IMG = "https://cdn-icons-png.flaticon.com/512/3237/3237472.png";
const BOT_NAME = "EVA";
const PERSON_NAME = "JIM";

var userLang = 'en-GB';

botResponse("/greet") //init


msgerForm.addEventListener("submit", async event => {
    event.preventDefault();

    const msgText = msgerInput.value;
    if (!msgText) return;

    appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);

    const target_lang = 'en-GB';
    // const response = await translateText(msgText, target_lang)
    // console.log(response)
    // const translatedMsg = await response.text;
    // console.log(translatedMsg)

    translateText(msgText, target_lang)
        .then(data => {
            console.log(data);
            const translatedMsg = data.text;
            userLang = data.detectedSourceLang;
            botResponse(translatedMsg);
        })

    // Set msgerInput to null
    msgerInput.value = "";

});

function appendMessage(name, img, side, text) {
    //   Simple solution for small apps
    const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
}

function botResponse(msgText) {
    // Send user input to Rasa's endpoint
    fetch('http://localhost:5005/webhooks/rest/webhook', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: msgText,
            sender: 'user'
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            // Display Rasa's response in the chat
            translateText(data[0].text, userLang)
                .then(data => {
                    console.log("Translated msg from rasa: ",data);
                    const msgBot = data.text;
                    appendMessage(BOT_NAME, BOT_IMG, "left", msgBot);

                })
            //const msgBot = data[0].text;
            const buttons = data[0].buttons;
            const image = data[0].image;
            //appendMessage(BOT_NAME, BOT_IMG, "left", msgBot);
            // Generate buttons in the UI
            const buttonsContainer = document.createElement('div');
            if (buttons) {
                buttons.forEach((button) => {
                    const buttonElement = document.createElement('button');
                    buttonElement.textContent = button.title;
                    buttonElement.classList.add('inform-btn');
                    buttonElement.onclick = () => {
                        // Deactivate all buttons
                        document.querySelectorAll(".inform-btn").forEach((btn) => {
                            btn.disabled = true;
                            btn.classList.add("clicked");
                        });
                        const payload = button.payload;
                        //Show the payload
                        //appendMessage(PERSON_NAME, PERSON_IMG, "right", payload)
                        //Send a message to the bot with the payload
                        botResponse(payload);
                    };
                    buttonsContainer.appendChild(buttonElement);
                });
                msgerChat.appendChild(buttonsContainer);
                msgerChat.scrollTop += 500;
            }

        });
}


// Utils
function get(selector, root = document) {
    return root.querySelector(selector);
}

function formatDate(date) {
    const h = "0" + date.getHours();
    const m = "0" + date.getMinutes();

    return `${h.slice(-2)}:${m.slice(-2)}`;
}

function translateText(text, targetLang) {
    return fetch('/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `text=${encodeURIComponent(text)}&target_lang=${encodeURIComponent(targetLang)}`
    })
        .then(response => response.json())
        .then(data => {
            console.log("Translated function: ", data)
            return data;
        })
        .catch(error => {
            console.error(error);
            return 'An error occurred while translating the text.';
        });
}