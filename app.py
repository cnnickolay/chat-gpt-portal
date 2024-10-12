import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from gpt import chatgpt_single_request_with_tokens, GPTVersion, BACKWARDS_MAP

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

        # Use the backwards map to convert model name to enum
        model_name = data.get('model', 'gpt-4o')  # Default to 'gpt-4o' if not provided
        gpt_version = BACKWARDS_MAP.get(model_name, GPTVersion.GPT_4)

        print(gpt_version)

        # Call the GPT function with the extracted model
        gpt_response = chatgpt_single_request_with_tokens(
            message=[msg['content'] for msg in conversation_history],
            gpt_version=gpt_version,
            temperature=0.1
        )

        # Append GPT response to the conversation history
        conversation_history.append({"role": "assistant", "content": gpt_response['content']})

        return jsonify(conversation_history=conversation_history)

    return render_template('chat.html', chat_url=CHAT_URL)


@app.route('/models', methods=['GET'])
def list_models():
    models = [version.value for version in GPTVersion]
    return jsonify(models=models)


if __name__ == '__main__':
    app.run()
