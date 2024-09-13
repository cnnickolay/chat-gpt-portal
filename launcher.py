import gpt
from gpt import GPTVersion

def main():
    dialogue_history = []
    message = ""
    total_tokens = 0
    print("Enter your message (type '/send' to submit): ")

    while True:
        try:
            line = input()
        except EOFError:
            break

        if line.strip() == "/send":
            if message.strip() != "":
                dialogue_history.append({"role": "user", "content": message.strip()})
                print("Sending message to GPT...")
                response = gpt.chatgpt_single_request_with_tokens([m['content'] for m in dialogue_history], GPTVersion.GPT_4, 0.1)
                total_tokens += response['tokens']
                dialogue_history.append({"role": "assistant", "content": response['content']})

                # Visual demarcation
                print("\n--- Response from GPT ---")
                print("GPT: ", response['content'])
                print("--- End of Response ---\n")
                print("Tokens used: ", response['tokens'])
                print("Total tokens used: ", total_tokens)

                # Reset message for the next input
                message = ""
                print("Enter your message (type '/send' to submit): ")
            else:
                print("No message to send. Please enter a message before using '/send'.")

        elif line.strip().lower() == 'exit':
            break
        else:
            message += line + "\n"  # Append the line to the message

if __name__ == "__main__":
    main()

