import os

class T6LogReader:
    def __init__(self, log_path: str = None) -> None:
        if log_path:
            self.log_path = log_path
        else:
            self.log_path = os.path.join(os.environ["LOCALAPPDATA"], "Plutonium", "console.log")

        if not os.path.exists(self.log_path):
            raise FileNotFoundError(f"Log file not found at {self.log_path}")

    def read_last_line(self) -> str | list:
        try:
            with open(self.log_path, 'r', encoding='utf-8') as file:
                lines = file.readlines() 
                return lines[len(lines) - 1]
        except Exception as e:
            return [f"Error reading log file: {e}"]
        
    def read_last_lines(self, number_of_lines: int = 10) -> str | list:
        try:
            with open(self.log_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            return lines[-number_of_lines:] if len(lines) >= number_of_lines else lines

        except Exception as e:
            return [f"Error reading log file: {e}"]

    def search_command(self, command: str, prefix: str = "]") -> list:
        try:
            with open(self.log_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                matching_lines = [line.strip() for line in lines if f"{prefix}{command}" in line]
            return matching_lines if matching_lines else [f"No occurences of '{command}' found"]

        except Exception as e:
            return [f"Error searching log file: {e}"]