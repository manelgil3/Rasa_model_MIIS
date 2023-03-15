const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
const msgerAudioBtn = document.querySelector('.msger-audio-btn');
const audioChunks = [];


// Icons made by Freepik from www.flaticon.com
//const BOT_IMG = "https://image.flaticon.com/icons/svg/327/327779.svg";
const BOT_IMG = "https://upload.wikimedia.org/wikipedia/commons/e/e4/Rasa_nlu_horizontal_purple.svg";
//const PERSON_IMG = "https://image.flaticon.com/icons/svg/145/145867.svg";
const PERSON_IMG = "https://www.upf.edu/documents/7283915/220614254/UPFt_rgb.png";
const BOT_NAME = "BOT";
const PERSON_NAME = "JIM";

msgerForm.addEventListener("submit", event => {
    event.preventDefault();

    const msgText = msgerInput.value;
    if (!msgText) return;

    appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
    msgerInput.value = "";

    // Send user input to Rasa's endpoint and display response in chat
    botResponse(msgText);
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

// function botResponse() {
//     const r = random(0, BOT_MSGS.length - 1);
//     const msgText = BOT_MSGS[r];
//     const delay = msgText.split(" ").length * 100;

//     setTimeout(() => {
//         appendMessage(BOT_NAME, BOT_IMG, "left", msgText);
//     }, delay);
// }

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
            // Display Rasa's response in the chat
            const msgBot = data[0].text;
            const buttons = data[0].buttons;
            appendMessage(BOT_NAME, BOT_IMG, "left", msgBot);
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
                        appendMessage(PERSON_NAME, PERSON_IMG, "right", payload)
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


