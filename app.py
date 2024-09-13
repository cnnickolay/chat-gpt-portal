import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from gpt import chatgpt_single_request_with_tokens, GPTVersion

app = Flask(__name__)

# Read the URL from the environment variable
CHAT_URL = os.getenv('CHAT_URL', '/chat')

@app.route(CHAT_URL, methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        user_message = data.get('message')
        conversation_history = data.get('conversation_history', [])
        conversation_history.append({"role": "user", "content": user_message})

        # Call the GPT function
        gpt_response = chatgpt_single_request_with_tokens(
            message=[msg['content'] for msg in conversation_history],
            gpt_version=GPTVersion.GPT_4,  # Replace with the appropriate GPT version
            temperature=0.1
        )

        # Append GPT response to the conversation history
        conversation_history.append({"role": "assistant", "content": gpt_response['content']})

        return jsonify(conversation_history=conversation_history)

    return render_template('chat.html', chat_url=CHAT_URL)


if __name__ == '__main__':
    app.run()
