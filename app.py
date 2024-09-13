from flask import Flask, request, jsonify, render_template, redirect, url_for
from gpt import chatgpt_single_request_with_tokens, GPTVersion

app = Flask(__name__)

# List to store the conversation history
conversation_history = []

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    global conversation_history
    if request.method == 'POST':
        user_message = request.form['message']
        conversation_history.append({"role": "user", "content": user_message})

        # Call the GPT function
        gpt_response = chatgpt_single_request_with_tokens(
            message=[msg['content'] for msg in conversation_history],
            gpt_version=GPTVersion.GPT_3_5_TURBO,  # Replace with the appropriate GPT version
            temperature=0.1
        )

        # Append GPT response to the conversation history
        conversation_history.append({"role": "assistant", "content": gpt_response['content']})

        return redirect(url_for('chat'))

    return render_template('chat.html', conversation_history=conversation_history)


@app.route('/hello')
def hello():
    name = request.args.get('name', 'World')  # Default to 'World' if no name is provided
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    app.run()
