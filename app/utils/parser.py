def parse_tool_call(text: str):
    if not text.startswith("CALL_TOOL"):
        return None, None

    try:
        _, tool, expression = text.split(":", 2)
        return tool.strip(), expression.strip()
    except:
        return None, None