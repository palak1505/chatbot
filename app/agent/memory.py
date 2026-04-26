class Memory:
    def __init__(self):
        self.history = []

    def add_user(self, message):
        self.history.append({"role": "user", "content": message})

    def add_agent(self, message):
        self.history.append({"role": "assistant", "content": message})

    def get_context(self):
        context = ""
        for msg in self.history:
            role = msg["role"]
            content = msg["content"]
            context += f"{role.upper()}: {content}\n"
        return context