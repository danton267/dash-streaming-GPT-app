import openai
import dash
from dash import (
    html,
    dcc,
    Input,
    Output,
    State,
    clientside_callback,
    ClientsideFunction,
)
from flask import request, Response

openai.api_key = open("key.txt", "r").read().strip("\n")

app = dash.Dash(__name__)


app.layout = html.Div(
    [
        html.H1("OpenAi Dash streaming MVP"),
        dcc.Input(id="text-prompt", placeholder="Ask a question"),
        html.Button("Submit", id="submit-prompt"),
        html.H2("OpenAI text stream"),
        html.P(
            id="response-window",
            style={"max-width": "600px"},
        ),
    ]
)


def send_messages(prompt):
    """OpenAI API call. You may choose parameters here but `stream=True` is required."""
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        stream=True,
        max_tokens=2024,
        temperature=0.5,
    )


# if you are creating a multipage app, you won't be able to import app object because of circular imports
# so unless you create the route in the same file where you define your Dash app
# you can simply use app = dash.get_app() to get the Dash app instance in any other page
@app.server.route("/streaming-chat", methods=["POST"])
def streaming_chat():
    user_prompt = request.json["prompt"]

    # prompt engineering/data augmentation can be performed here
    # important thing is that this is happening on the backend, so that the users can't tamper with this
    # JS front-end only handles the response, and nothing else
    chat_completion_prompt = [
        {
            "role": "system",
            "content": "Answer the following question as a pirate. Respond in markdown format. Question:\n",
        },
        {"role": "user", "content": user_prompt},
    ]

    def response_stream():
        yield from (
            line.choices[0].delta.get("content", "")
            for line in send_messages(chat_completion_prompt)
        )

    return Response(response_stream(), mimetype="text/response-stream")


# JS callback to send the question to the flask API, at the end it enables the submit button
clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="streaming_GPT"),
    Output("submit-prompt", "disabled"),
    Input("submit-prompt", "n_clicks"),
    State("text-prompt", "value"),
    prevent_initial_call=True,
)


# Clears the input field after the user clicks submit, and disables submit button
clientside_callback(
    """
    function updateQuestionFields(n_clicks) {
        return [ "", true ];
    }
    """,
    Output("text-prompt", "value"),
    Output("submit-prompt", "disabled", allow_duplicate=True),
    Input("submit-prompt", "n_clicks"),
    prevent_initial_call=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
