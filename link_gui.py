import json
import os
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


class DroidMCPInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Droid MCP - 1-Click Linker")
        self.root.geometry("400x200")
        self.root.eval('tk::PlaceWindow . center')

        self.label = tk.Label(
            root,
            text="🤖 Droid MCP\n\n1-Click Install for VS Code (Cline).",
            font=("Arial", 12),
            pady=20
        )
        self.label.pack()

        self.btn = tk.Button(
            root,
            text="🔗 Link to Cline",
            command=self.link_mcp,
            font=("Arial", 11, "bold"),
            bg="#007ACC",
            fg="black",
            padx=20,
            pady=10
        )
        self.btn.pack()

    def get_cline_config_path(self):
        if sys.platform == "darwin":
            return Path.home() / "Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"
        elif sys.platform == "win32":
            return Path(os.getenv('APPDATA')) / "Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"
        return None

    def link_mcp(self):
        # 1. Capture the EXACT absolute paths automatically
        project_path = str(Path(__file__).parent.absolute())
        current_python_exe = sys.executable
        config_path = self.get_cline_config_path()

        if not config_path:
            messagebox.showerror("Error", "OS not supported for auto-link yet.")
            return

        # 2. Build the Bulletproof Config
        mcp_config = {
            "command": current_python_exe,
            "args": ["-m", "src.main"],
            "env": {
                "PYTHONPATH": project_path,
                "PYTHONUNBUFFERED": "1",
                "PYTHONIOENCODING": "utf-8"
            }
        }

        try:
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = {"mcpServers": {}}
            else:
                config_path.parent.mkdir(parents=True, exist_ok=True)
                data = {"mcpServers": {}}

            if "mcpServers" not in data:
                data["mcpServers"] = {}

            # 3. Inject configuration with the CORRECT name
            data["mcpServers"]["droid-mcp"] = mcp_config

            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            messagebox.showinfo(
                "Success! 🎉",
                "Droid MCP linked successfully!\nNo manual config needed. Just restart VS Code."
            )
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DroidMCPInstaller(root)
    root.mainloop()
