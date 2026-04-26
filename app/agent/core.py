# from app.llm.gemini_client import get_client
# from app.agent.memory import Memory
# from app.agent.prompt import SYSTEM_PROMPT
# from app.utils.parser import parse_tool_call
# from app.tools.calculator import calculate
# from config.settings import MODEL_NAME


# class Agent:
#     def __init__(self):
#         self.client = get_client()
#         self.memory = Memory()

#         self.tools = {
#             "calculator": calculate
#         }

#     def run(self, user_input: str) -> str:
#         self.memory.add_user(user_input)

#         context = self.memory.get_context()
#         full_prompt = SYSTEM_PROMPT + "\n" + context + f"\nUSER: {user_input}"

#         response = self.client.models.generate_content(
#             model=MODEL_NAME,
#             contents=full_prompt
#         )

#         text = response.text.strip()

#         tool_name, tool_input = parse_tool_call(text)

#         if tool_name and tool_name in self.tools:
#             tool_result = self.tools[tool_name](tool_input)

#             follow_up = self.client.models.generate_content(
#                 model=MODEL_NAME,
#                 contents=f"Tool result: {tool_result}. Give final answer."
#             )

#             final_text = follow_up.text.strip()
#             self.memory.add_agent(final_text)
#             return final_text

#         self.memory.add_agent(text)
#         return text
from app.agent.memory import Memory
from app.agent.prompt import SYSTEM_PROMPT
from app.utils.parser import parse_tool_call
from app.tools.calculator import calculate
from app.llm.gemini_client import call_model  # now using OpenRouter


class Agent:
    def __init__(self):
        self.memory = Memory()

        self.tools = {
            "calculator": calculate
        }

    def run(self, user_input: str) -> str:
        # store user input
        self.memory.add_user(user_input)

        # build context
        context = self.memory.get_context()
        full_prompt = SYSTEM_PROMPT + "\n" + context + f"\nUSER: {user_input}"

        # call model
        text = call_model(full_prompt).strip()

        # check tool call
        tool_name, tool_input = parse_tool_call(text)

        if tool_name and tool_name in self.tools:
            tool_result = self.tools[tool_name](tool_input)

            # send result back to model
            final_text = call_model(
                f"Tool result: {tool_result}. Give final answer."
            ).strip()

            self.memory.add_agent(final_text)
            return final_text

        # normal response
        self.memory.add_agent(text)
        return text