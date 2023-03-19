const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
const msgerAudioBtn = document.querySelector('.msger-audio-btn');
const msgerRecordBtn = get(".msger-record-btn");
const recordedAudio = document.getElementById("recordedAudio");
// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "https://www.upf.edu/documents/7283915/220614254/UPFt_rgb.png";
const PERSON_IMG = "https://cdn-icons-png.flaticon.com/512/3237/3237472.png";
const BOT_NAME = "EVA";
const PERSON_NAME = "JIM";

var recordedBlobs = [];
let mediaRecorder;

var userLang = 'en-GB';

//botResponse("/welcome") //init


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

async function startRecording() {

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });

        // Listen for the 'dataavailable' event and save the recorded data
        mediaRecorder.ondataavailable = (event) => {
            console.log("PUSH data")
            recordedBlobs.push(event.data);
        };
        // Create a promise that resolves when the recording is stopped and all data is available
        const recordingStopped = new Promise((resolve) => {
            mediaRecorder.onstop = resolve;
        });
        // Start recording
        mediaRecorder.start();
        const recordButton = document.querySelector(".msger-record-btn");
        recordButton.innerText = "Stop Recording";
        // Wait for the recording to stop and all data to be available
        await recordingStopped;

        console.log('Recording stopped');
        console.log('Recorded blobs:', recordedBlobs);
    } catch (error) {
        console.error('Error starting recording:', error);
    }
}

msgerRecordBtn.addEventListener("click", () => {
    console.log("msgerRecordBtn event listener 1")
    if (mediaRecorder && mediaRecorder.state === "recording") {
        console.log("if (mediaRecorder && mediaRecorder.state === 'recording')")
        stopRecording();
    } else {
        startRecording();
        console.log("else (mediaRecorder && mediaRecorder.state === 'recording')")
    }
});

async function stopRecording() {
    console.log("stopRecording(1)")
    const target_lang = 'en-GB';
    mediaRecorder.stop();

    mediaRecorder.onstop = async () => {
        console.log("data available after MediaRecorder.stop() called.");
        console.log("stopRecording(2)")
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        console.log("stopRecording(3)")
        const recordButton = document.querySelector(".msger-record-btn");
        // Change button text to "Start Recording"
        recordButton.innerText = "Start Recording";
        console.log("stopRecording(4)")

        // Combine recorded chunks into a single Blob
        const superBuffer = new Blob(recordedBlobs, { type: "audio/webm" });

        // Transcribe the recorded audio
        const apiKey = "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"; // Replace with your OpenAI API key
        const transcriptionResult = await transcribeSpeech(superBuffer, apiKey);
        appendMessage(PERSON_NAME, PERSON_IMG, "right", transcriptionResult.text);

        if (transcriptionResult) {
            console.log("Transcription result:", transcriptionResult);
            // Do something with the transcription result, e.g., send it as a message
            translateText(transcriptionResult.text, target_lang)
                .then(data => {
                    console.log(data);
                    const translatedMsg = data.text;
                    userLang = data.detectedSourceLang;
                    botResponse(translatedMsg);
                })
        } else {
            console.log("An error occurred during transcription.");
        }

        // Reset the recordedBlobs array
        recordedBlobs = [];
    }
}


function saveRecording(blob) {
    console.log("save recording")
    recordedBlobs.push(blob);
    playRecordedAudio();
}



async function transcribeSpeech(audioBlob, OPENAI_API_KEY) {
    const formData = new FormData();
    formData.append("file", audioBlob, "audio.webm"); // Make sure the file has the correct extension
    formData.append("model", "whisper-1");
    console.log("Audio Blob:", audioBlob);
    console.log("Audio Blob MIME type:", audioBlob.type);
    // const a = document.createElement("a");
    // a.href = URL.createObjectURL(audioBlob);
    // a.download = "recorded_audio.mp3";
    // a.click();
    try {
        console.log("OPEN AI KEY")
        console.log(OPENAI_API_KEY)
        const response = await axios.post("https://api.openai.com/v1/audio/transcriptions", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
                "Authorization": `Bearer ${OPENAI_API_KEY}`,
            },
        });
        console.log("Response:", response.data);
        return response.data; // Return the transcription result
    } catch (error) {
        console.error("Error during ASR:", error.response || error);
        return null; // Return null in case of an error
    }
}

async function playRecordedAudio() {
    const superBuffer = new Blob(recordedBlobs, { type: "audio/wav" });

    const apiKey = "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"; // Replace with your OpenAI API key
    const target_lang = 'en-GB';

    // Transcribe the recorded audio
    const transcriptionResult = await transcribeSpeech(superBuffer, apiKey);
    if (transcriptionResult) {
        console.log("Transcription result:", transcriptionResult);
        // Do something with the transcription result, e.g., send it as a message
        translateText(transcriptionResult.text, target_lang)
            .then(data => {
                console.log(data);
                const translatedMsg = data.text;
                userLang = data.detectedSourceLang;
                botResponse(translatedMsg);
            })
    } else {
        console.log("An error occurred during transcription.");
    }
}


function stringifyMsgText(msgText) {
    if (typeof msgText === 'string') {
        // if msgText is already a string, return it as is
        return msgText;
    } else if (typeof msgText === 'object' && msgText !== null && 'text' in msgText) {
        // if msgText is an object with a 'text' property, return the value of 'text' as a string
        return String(msgText.text);
    } else {
        // otherwise, return an empty string
        return '';
    }
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
                    console.log("Translated msg from rasa: ", data);
                    const msgBot = data.text;
                    appendMessage(BOT_NAME, BOT_IMG, "left", msgBot);
                    speakTranslatedResponse(msgBot);

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

function speakTranslatedResponse(response) {
    // Translate response to user's language
    console.log("Data into speakTranslatedResponse: ", response);
    const translatedResponse = response;

    // Create a new SpeechSynthesisUtterance object
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(translatedResponse);

    // Set the voice and language
    const voice = synth.getVoices().find((v) => v.lang === userLang);
    console.log(voice)
    utterance.voice = voice;

    // Speak the response
    synth.speak(utterance);
}