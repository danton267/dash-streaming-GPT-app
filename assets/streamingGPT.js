window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        streaming_GPT: async function streamingGPT(n_clicks, prompt) {
            
            // id of the window we want to write the response to
            // you may use dynamically created id's here if you have multiple windows 
            // eg "#response-window-${element_id}"
            const responseWindow = document.querySelector("#response-window");
            
            // Send the messages to the server to get the streaming response
            // if you have more parameters python side, you can add them to the body
            // eg. body: JSON.stringify({ prompt, parameter1, parameter2 }),
            const response = await fetch("/streaming-chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ prompt }),
            });
          
            // Create a new TextDecoder to decode the streamed response text
            const decoder = new TextDecoder();
          
            // Set up a new ReadableStream to read the response body
            const reader = response.body.getReader();
            let chunks = "";
            
            // Read the response stream as chunks and append them to the chat log
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                chunks += decoder.decode(value);
                responseWindow.innerHTML = chunks;
            }
            
            // return false to enable the submit button again (disabled=false)
            return false;
          }
    }
});