import gradio as gr
from agent import chat


def respond(message, history):
    # Gradio ChatInterface 传入 history 但我们用 LangChain 自己管
    return chat(message)


demo = gr.ChatInterface(
    fn=respond,
    title="☕ 悠然咖啡 智能客服",
    description="可以问菜单、价格、营业时间，也可以下单和预约座位！",
    examples=["你们有什么饮品？", "帮我查一下拿铁还有多少", "我要点 2 杯摩卡", "预约明天下午 3 点 2 人座位"],
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
