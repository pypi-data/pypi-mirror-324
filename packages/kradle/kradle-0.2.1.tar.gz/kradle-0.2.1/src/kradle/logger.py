from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.logging import RichHandler
from rich import box
import logging
import sys
from typing import Optional, Dict, Any
from datetime import datetime

class KradleLogger:
    def __init__(self):
        self.console = Console()
        self._setup_logging()
        
    def _setup_logging(self):
        """Configure logging with Rich handler for beautiful formatting"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=[
                RichHandler(
                    rich_tracebacks=True,
                    markup=True,
                    show_time=False
                )
            ]
        )
        # Keep Flask debug logs clean
        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.handlers = []
        werkzeug_handler = logging.StreamHandler(sys.stdout)
        werkzeug_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(message)s',
            '%H:%M:%S'
        ))
        werkzeug_logger.addHandler(werkzeug_handler)
        werkzeug_logger.setLevel(logging.INFO)
        
    def display_startup_banner(self, config: Dict[str, Any]):
        """Display a beautiful startup banner with server information"""
        self.console.clear()
        
        # Create welcome message
        welcome_text = Text()
        welcome_text.append("Kradle Agent Server", style="bold cyan")
        welcome_text.append(" is ready!", style="green")
        self.console.print("\n", welcome_text, "\n")
        
        # Display agent info
        agent_text = Text()
        agent_text.append("Agent: ", style="bright_white")
        agent_text.append(f"{config.get('agent_slug')}", style="cyan")
        agent_text.append(f" (Port {config.get('port')})", style="dim")
        self.console.print(agent_text)
        
        # URLs Panel with clean formatting
        url_text = Text()
        
        # Local URL
        url_text.append("\n→ Local:    ", style="bright_white")
        url_text.append(f"http://localhost:{config.get('port')}/{config.get('agent_slug')}\n", style="cyan")
        
        # Public URL (if available)
        agent_url = config.get('agent_url', '')
        if 'pinggy.link' in agent_url:
            url_text.append("→ Public:   ", style="bright_white")
            url_text.append(f"{agent_url}\n", style="green")
            
        # Challenge Dashboard
        url_text.append("→ Dashboard: ", style="bright_white")
        url_text.append("https://app.kradle.ai/workbench/challenges", style="blue")
        
        self.console.print(Panel(
            url_text,
            title="[bold]Access URLs",
            border_style="bright_black",
            box=box.ROUNDED,
            padding=(1, 2)
        ))
        
        # Tips footer
        self.console.print("\n[dim]Press Ctrl+C to stop the server[/dim]")
        print()  # Add spacing for upcoming logs

    def log_success(self, message: str):
        """Log a success message"""
        self.console.print(f"✓ {message}", style="green")

    def log_error(self, message: str, error: Optional[Exception] = None):
        """Log an error message with optional exception details"""
        self.console.print(f"✕ {message}", style="red")
        if error:
            self.console.print(f"  → {str(error)}", style="red dim")

    def log_warning(self, message: str):
        """Log a warning message"""
        self.console.print(f"! {message}", style="yellow")

    def log_info(self, message: str):
        """Log an informational message"""
        self.console.print(f"○ {message}", style="blue")

    def log_debug(self, message: str):
        """Log a debug message"""
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            self.console.print(f"· {message}", style="dim")

    def log_api_call(self, method: str, endpoint: str, status: int):
        """Log an API call with color-coded status"""
        status_color = "green" if 200 <= status < 300 else "red"
        method_width = 6  # Consistent width for method
        self.console.print(
            f"  {method:<{method_width}} {endpoint} [{status_color}]{status}[/]",
            style="dim"
        )

    def on_shutdown(self):
        """Display shutdown message"""
        self.console.print("\n[yellow]Shutting down Kradle Agent Server...[/yellow]")