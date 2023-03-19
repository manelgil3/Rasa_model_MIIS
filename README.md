# Instructions

*Make sure you have set up the Rasa on your system or server.*

## Integration

- Step 1: Since this Chat UI communicates with the Rasa server using `rest` channel, make sure you have added `rest` channel in the `credentials.yml` file
- Once you have developed your bot and you are ready to integrate the bot with the UI, you can start the Rasa server using the below command
  ```
  rasa run -m models --enable-api --cors "*" --debug
  ```
- If you have custom actions, you can start the action server using the below command
    ```
    rasa run actions --cors "*" --debug
    ```
- If module utils fail to import run the command below
    ```
    export PYTHONPATH=/directory/to/Rasa_model_MIIS/rasa_model/actions/:$PYTHONPATH
    ```
- To visualize the chatbot in you local machine run this command below on inside the path = UI
    ```
    node main.js
    ```
- In order to install all necessary packages do:
    ```
    npm install <package>
    ```