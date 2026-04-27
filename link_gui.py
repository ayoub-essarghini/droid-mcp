# MIT License — Copyright (c) 2024 Ayoub ES SARGHINI
import json
import os
import shutil
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from PIL import Image, ImageDraw, ImageTk

BG = "#0D0D0F"
DARWIN = sys.platform == "darwin"


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def _sf(size, bold=False):
    family = "SF Pro Display" if DARWIN else "Segoe UI"
    return (family, size, "bold") if bold else (family, size)


def make_rounded_image(color, size=(300, 48), radius=10):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    draw.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=(r, g, b, 255))
    return ImageTk.PhotoImage(img)


class CanvasButton:
    def __init__(
        self,
        parent,
        text,
        icon_photo,
        bg_color,
        hover_color,
        command,
        width=420,
        height=52,
    ):
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.width = width
        self.height = height

        self.canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg="#121212",
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )

        self._draw_bg(bg_color)

        self.icon_id = None
        if icon_photo:
            self.icon_id = self.canvas.create_image(
                22, height // 2, image=icon_photo, anchor="center"
            )

        text_x = 44 if icon_photo else width // 2
        text_anchor = "w" if icon_photo else "center"
        self.text_id = self.canvas.create_text(
            text_x,
            height // 2,
            text=text,
            font=_sf(13, bold=True),
            fill="white",
            anchor=text_anchor,
        )

        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

    def _draw_bg(self, color):
        self.canvas.delete("bg")
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle(
            [0, 0, self.width - 1, self.height - 1],
            radius=12,
            fill=(r, g, b, 255),
        )
        self._bg_photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, image=self._bg_photo, anchor="nw", tags="bg")
        self.canvas.tag_lower("bg")

    def _on_enter(self, e):
        self._draw_bg(self.hover_color)

    def _on_leave(self, e):
        self._draw_bg(self.bg_color)

    def _on_click(self, e):
        self._draw_bg(self.hover_color)

    def _on_release(self, e):
        self._draw_bg(self.bg_color)
        self.command()

    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)


class DroidMCPInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Droid MCP")
        try:
            _icon = Image.open(resource_path("assets/mcp_logo.png"))
            self._icon_photo = ImageTk.PhotoImage(_icon)
            self.root.iconphoto(True, self._icon_photo)
        except Exception:
            pass
        self.root.geometry("560x600")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.main_frame = tk.Frame(self.root, bg=BG)
        self.main_frame.pack(fill="both", expand=True)

        self._build_header()
        self._build_description()
        self._build_divider()
        self._build_buttons()
        self._build_footer()

        self.root.update_idletasks()
        w, h = 560, 600
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    def _build_header(self):
        header = tk.Frame(self.main_frame, bg=BG)
        header.pack(fill="x", pady=(36, 0), padx=40)

        row = tk.Frame(header, bg=BG)
        row.pack(anchor="center")

        try:
            mcp_img = Image.open(resource_path("assets/mcp_logo.png"))
            mcp_img = mcp_img.resize((96, 96), Image.Resampling.LANCZOS)
            self.mcp_photo = ImageTk.PhotoImage(mcp_img)
            tk.Label(row, image=self.mcp_photo, bg=BG).pack(side="left", padx=(0, 20))
        except Exception:
            tk.Label(row, text="🤖", font=("Helvetica", 64), bg=BG).pack(side="left", padx=(0, 20))

        text_col = tk.Frame(row, bg=BG)
        text_col.pack(side="left", anchor="w")

        tk.Label(
            text_col,
            text="Droid MCP",
            font=_sf(26, bold=True),
            bg=BG,
            fg="#FFFFFF",
            anchor="w",
        ).pack(anchor="w")

        tk.Label(
            text_col,
            text="AI-powered Android automation bridge",
            font=_sf(12),
            bg=BG,
            fg="#6B7280",
            anchor="w",
        ).pack(anchor="w", pady=(4, 0))

    def _build_description(self):
        outer = tk.Frame(self.main_frame, bg=BG)
        outer.pack(fill="x", padx=40, pady=24)

        card = tk.Frame(outer, bg="#161618", bd=0)
        card.pack(fill="x")

        tk.Frame(card, bg="#3B82F6", height=2).pack(fill="x")

        inner = tk.Frame(card, bg="#161618")
        inner.pack(fill="x", padx=20, pady=16)

        features = [
            ("◉", "Screen reader", "Read live UI state from any Android app"),
            ("◉", "Touch control", "Tap, swipe, and type without hardcoding"),
            ("◉", "Debug bridge", "Inspect logs and app state dynamically"),
        ]

        for icon, title, desc in features:
            row = tk.Frame(inner, bg="#161618")
            row.pack(fill="x", pady=4)

            tk.Label(
                row,
                text=icon,
                font=("Helvetica", 8),
                bg="#161618",
                fg="#3B82F6",
                width=3,
            ).pack(side="left")

            text_col = tk.Frame(row, bg="#161618")
            text_col.pack(side="left", fill="x", expand=True)

            tk.Label(
                text_col,
                text=title,
                font=_sf(11, bold=True),
                bg="#161618",
                fg="#E5E7EB",
                anchor="w",
            ).pack(fill="x")
            tk.Label(
                text_col,
                text=desc,
                font=_sf(10),
                bg="#161618",
                fg="#6B7280",
                anchor="w",
            ).pack(fill="x")

    def _build_divider(self):
        div_frame = tk.Frame(self.main_frame, bg=BG)
        div_frame.pack(fill="x", padx=40, pady=(0, 4))

        tk.Frame(div_frame, bg="#1F2937", height=1).pack(fill="x")

        tk.Label(
            div_frame,
            text="CONNECT YOUR EDITOR",
            font=_sf(9, bold=True),
            bg=BG,
            fg="#4B5563",
            pady=10,
        ).pack()

    def _build_buttons(self):
        btn_outer = tk.Frame(self.main_frame, bg=BG)
        btn_outer.pack(fill="x", padx=40)

        try:
            cline_img = Image.open(resource_path("assets/cline_logo.png")).resize(
                (22, 22), Image.Resampling.LANCZOS
            )
            self.cline_photo = ImageTk.PhotoImage(cline_img)
        except Exception:
            self.cline_photo = None

        try:
            claude_img = Image.open(resource_path("assets/claude_logo.png")).resize(
                (22, 22), Image.Resampling.LANCZOS
            )
            self.claude_photo = ImageTk.PhotoImage(claude_img)
        except Exception:
            self.claude_photo = None

        btn_width = 480

        cline_btn = CanvasButton(
            btn_outer,
            text="  Link to VS Code  (Cline)",
            icon_photo=self.cline_photo,
            bg_color="#1D6ED4",
            hover_color="#2563EB",
            command=lambda: self.link_config(self.get_cline_path(), "VS Code (Cline)"),
            width=btn_width,
            height=52,
        )
        cline_btn.pack(pady=(0, 10))

        claude_btn = CanvasButton(
            btn_outer,
            text="  Link to Claude Code",
            icon_photo=self.claude_photo,
            bg_color="#B45309",
            hover_color="#D97706",
            command=self.link_claude_code,
            width=btn_width,
            height=52,
        )
        claude_btn.pack()

    def _build_footer(self):
        footer_frame = tk.Frame(self.main_frame, bg=BG)
        footer_frame.pack(side="bottom", fill="x", pady=20)

        tk.Frame(footer_frame, bg="#1F2937", height=1).pack(fill="x", padx=40)

        tk.Label(
            footer_frame,
            text="Made with ❤  by Ayoub ES SARGHINI  ·  @ayoub-essarghini",
            font=_sf(9),
            bg=BG,
            fg="#374151",
            pady=10,
        ).pack()

    def get_cline_path(self):
        cline_rel = (
            "Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"
        )
        if sys.platform == "darwin":
            return Path.home() / "Library/Application Support" / cline_rel
        elif sys.platform == "win32":
            return Path(os.getenv("APPDATA")) / cline_rel
        return None

    def get_server_exe_path(self):
        server_filename = "droid-mcp-server.exe" if sys.platform == "win32" else "droid-mcp-server"

        if getattr(sys, "frozen", False):
            if sys.platform == "darwin" and ".app/Contents/MacOS" in sys.executable:
                base_dir = Path(sys.executable).parents[3]
            else:
                base_dir = Path(sys.executable).parent
        else:
            base_dir = Path(__file__).parent.absolute() / "dist"

        return str(base_dir / server_filename)

    def link_config(self, config_path, app_name):
        if not config_path:
            messagebox.showerror("Error", f"OS not supported for {app_name} auto-link yet.")
            return

        server_exe_path = self.get_server_exe_path()

        if not os.path.exists(server_exe_path):
            messagebox.showerror(
                "Missing Server Executable",
                f"Could not find the server executable at:\n{server_exe_path}\n\n"
                f"Ensure '{os.path.basename(server_exe_path)}' is in the same folder "
                "as this installer.",
            )
            return

        mcp_config = {
            "command": server_exe_path,
            "args": [],
            "env": {"PYTHONUNBUFFERED": "1"},
        }

        try:
            if config_path.exists():
                with open(config_path, encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = {"mcpServers": {}}
            else:
                config_path.parent.mkdir(parents=True, exist_ok=True)
                data = {"mcpServers": {}}

            data.setdefault("mcpServers", {})
            data["mcpServers"]["droid-mcp"] = mcp_config

            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            messagebox.showinfo(
                "Linked Successfully",
                f"Droid MCP linked to {app_name}.\n\nRestart {app_name} to apply changes.",
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to configure {app_name}:\n{e}")

    def get_project_root(self):
        if getattr(sys, "frozen", False):
            if sys.platform == "darwin" and ".app/Contents/MacOS" in sys.executable:
                return str(Path(sys.executable).parents[3])
            return str(Path(sys.executable).parent)
        return str(Path(__file__).parent.absolute())

    def get_python_cmd(self):
        project_root = self.get_project_root()
        for candidate in [
            Path(project_root) / "venv" / "bin" / "python3",
            Path(project_root) / "venv" / "bin" / "python",
        ]:
            if candidate.exists():
                return str(candidate)
        return shutil.which("python3") or shutil.which("python")

    def link_claude_code(self):
        claude_json = Path.home() / ".claude.json"
        if not claude_json.exists():
            messagebox.showerror(
                "Claude Code Not Found",
                "~/.claude.json not found.\n\nInstall Claude Code first:\nhttps://claude.ai/code",
            )
            return

        python_cmd = self.get_python_cmd()
        if not python_cmd:
            messagebox.showerror("Python Not Found", "Could not find a Python interpreter.")
            return

        project_root = self.get_project_root()
        mcp_entry = {
            "type": "stdio",
            "command": python_cmd,
            "args": ["-m", "src.server.mcp_server"],
            "env": {
                "PYTHONUNBUFFERED": "1",
                "PYTHONPATH": project_root,
            },
        }

        try:
            with open(claude_json, encoding="utf-8") as f:
                data = json.load(f)

            data.setdefault("mcpServers", {})
            data["mcpServers"]["droid-mcp"] = mcp_entry

            with open(claude_json, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            messagebox.showinfo(
                "Linked Successfully",
                "Droid MCP linked to Claude Code (user scope).\n\n"
                "Restart Claude Code to apply changes.",
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to write ~/.claude.json:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DroidMCPInstaller(root)
    root.mainloop()
