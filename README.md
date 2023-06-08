# Streaming Text from OpenAI API sample app

You can get the API key from [OpenAI](https://platform.openai.com/account/api-keys), and then create `key.txt` file in the root directory of this project (you may also choose to use environment variables).

This app was made using Python 3.9.0

## How it works

1. User types in the prompt
2. User presses send button
    1. This triggers clientside callback JS function
    2. JS function makes a `await fetch("/streaming-chat"` request to the Dash server
        1. in Dash, we create `@app.server.route("/streaming-chat", methods=["POST"])` route to receive response from the JS function
        2. We retrieve all parameters from the request, process them, and send them to the OpenAI API
        3. We return `Response yield object` to the JS function
    3. JS function processess the response and starts appending incoming text to the `innerHTML` of the `response window element`

I also added a second clientside callback which disables the submit button so that it can not be pressed while the request is being processed.


## JS development tricks

ChatGPT is your friend, there is nothing it won't be able to help/teach you when it comes to JS.

Whenever you are changing the JS code, it is good idea to "flush" your browser cache otherwise sometimes you might not see changes done in your code reflected in your browser because it cached the old version of the code and refuses to load the new one.

- Windows users can press `CTRL + F5`

- Mac users can press `CMD + SHIFT + R`

And by doing this you will force your browser to load the new version of the code.
