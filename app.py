import gradio as gr
from openai import OpenAI
import os

# Get OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Please set it in the Spaces secrets.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# System prompt
system_prompt = {
    "role": "system",
    "content": (
        "You are Cope AI, a chill and empathetic chatbot here to help people deal with stress, losses, or wild emotions—especially from gambling on pump.fun, that crazy casino meme coin site. "
        "Keep it real, toss in some humor, and maybe a few gambling or crypto references to lighten the mood. "
        "Offer practical coping tips when it makes sense, but don’t be preachy—sound like a friend who gets it."
    )
}

# Chat function
def cope_ai_chat(message, history):
    messages = [system_prompt]
    for entry in history or []:
        messages.append({"role": entry["role"], "content": entry["content"]})
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.9,
        max_tokens=150
    )
    return response.choices[0].message.content

# Gradio interface
with gr.Blocks(title="Cope AI") as demo:
    gr.Markdown("# Cope AI: Your Pump.fun Therapy Buddy")
    gr.Markdown("Feeling wrecked from a bad roll on pump.fun? Chat with me—I’ve got your back.")
    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox(placeholder="What’s messing with you today?", label="Spill it")
    clear = gr.Button("Clear Chat")

    def chat_handler(user_input, chat_history):
        bot_response = cope_ai_chat(user_input, chat_history)
        new_user_message = {"role": "user", "content": user_input}
        new_bot_message = {"role": "assistant", "content": bot_response}
        return (chat_history or []) + [new_user_message, new_bot_message], ""

    msg.submit(chat_handler, inputs=[msg, chatbot], outputs=[chatbot, msg])
    clear.click(lambda: [], None, chatbot, queue=False)

# Launch with Spaces-compatible settings (removed ssr)
demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
