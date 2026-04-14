from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from knowledge import SYSTEM_PROMPT
from tools import check_inventory, create_order, reserve_seat

TOOLS = [check_inventory, create_order, reserve_seat]

llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, TOOLS, prompt)
agent_executor = AgentExecutor(agent=agent, tools=TOOLS)

# 多轮对话：按 session_id 维护独立历史
_histories: dict[str, InMemoryChatMessageHistory] = {}


def get_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in _histories:
        _histories[session_id] = InMemoryChatMessageHistory()
    return _histories[session_id]


agent_with_history = RunnableWithMessageHistory(
    agent_executor,
    get_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)


def chat(message: str, session_id: str = "default") -> str:
    resp = agent_with_history.invoke(
        {"input": message},
        config={"configurable": {"session_id": session_id}},
    )
    return resp["output"]


if __name__ == "__main__":
    print("悠然咖啡客服（输入 quit 退出）")
    while True:
        user_input = input("\n你: ")
        if user_input.strip().lower() == "quit":
            break
        print(f"客服: {chat(user_input)}")
