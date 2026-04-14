import gradio as gr
from agent import chat


def respond(message, history):
    return chat(message)


demo = gr.ChatInterface(
    fn=respond,
    title="☕ Youran Coffee - AI Customer Service",
    description="Ask about our menu, prices, hours — or place an order and reserve a seat!",
    examples=["What drinks do you have?", "Check latte inventory", "Order 2 mochas", "Reserve a table for 2 tomorrow at 3pm"],
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
