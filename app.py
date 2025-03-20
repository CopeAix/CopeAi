import gradio as gr
from openai import OpenAI
import os

# Get OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Please set it in the Spaces secrets.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# System prompts in English and Chinese
system_prompt_en = {
    "role": "system",
    "content": (
        "You are Cope AI, a chill and empathetic chatbot here to help people deal with stress, losses, or wild emotions—especially from trading meme coins. "
        "Keep it real, toss in some humor, and maybe a few crypto references to lighten the mood. "
        "Offer practical coping tips when it makes sense, but don’t be preachy—sound like a friend who gets it."
    )
}

system_prompt_cn = {
    "role": "system",
    "content": (
        "你是Cope AI，一个冷静又善解人意的聊天机器人，专门帮助人们应对压力、损失或激烈的情绪波动——尤其是因为交易迷因币。 "
        "保持真实，带点幽默，可以偶尔提到一些加密货币梗来缓解气氛。 "
        "在合适的时候提供实际的应对建议，但别显得太说教——就像一个真正懂你的朋友。"
    )
}

# Chat function
def cope_ai_chat(message, history, lang="en"):
    system_prompt = system_prompt_en if lang == "en" else system_prompt_cn
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
    gr.Markdown("# Cope AI: Your Meme Coin Therapy Buddy / 你的迷因币疗愈伙伴")
    gr.Markdown("Feeling wrecked from a bad meme coin trade? Chat with me—I’ve got your back. / 迷因币交易亏大了？来聊聊，我懂你。")
    lang_toggle = gr.Dropdown(choices=["English", "中文"], value="English", label="Language / 语言")
    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox(placeholder="What’s messing with you today? / 今天啥事让你烦？", label="Spill it / 吐槽吧")
    clear = gr.Button("Clear Chat / 清空聊天")

    def chat_handler(user_input, chat_history, lang_choice):
        lang = "en" if lang_choice == "English" else "cn"
        bot_response = cope_ai_chat(user_input, chat_history, lang)
        new_user_message = {"role": "user", "content": user_input}
        new_bot_message = {"role": "assistant", "content": bot_response}
        return (chat_history or []) + [new_user_message, new_bot_message], ""

    msg.submit(chat_handler, inputs=[msg, chatbot, lang_toggle], outputs=[chatbot, msg])
    clear.click(lambda: [], None, chatbot, queue=False)

# Launch with Spaces-compatible settings
demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
