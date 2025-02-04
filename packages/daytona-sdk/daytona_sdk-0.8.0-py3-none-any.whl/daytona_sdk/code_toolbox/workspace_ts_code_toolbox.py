import base64

class WorkspaceTsCodeToolbox:
    def get_run_command(self, code: str) -> str:
        base64_code = base64.b64encode(code.encode()).decode()
        return f"python3 -c \"exec(__import__('base64').b64decode('{base64_code}').decode())\""
