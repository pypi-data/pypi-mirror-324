"""Centralized logging utilities for Python Release Master."""

import logging
from typing import Dict, Any, List, Optional

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.status import Status

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

class SafeLogger:
    """Thread-safe logger with rich formatting and safe markup handling."""
    
    _instance = None
    
    def __new__(cls):
        """Ensure singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize logger if not already initialized."""
        if not hasattr(self, 'initialized'):
            self.console = Console()
            self._status = None
            self.log = logging.getLogger("python_release_master")
            self.initialized = True
    
    def _escape_markup(self, text: str) -> str:
        """Escape rich markup in text safely.
        
        Args:
            text: Text to escape
        
        Returns:
            Escaped text safe for rich formatting
        """
        if not isinstance(text, str):
            text = str(text)
        return text.replace("[", "\\[").replace("]", "\\]")
    
    def _format_command(self, cmd: List[str], env: Optional[Dict[str, str]] = None) -> str:
        """Format command for display, safely handling environment variables.
        
        Args:
            cmd: Command parts
            env: Optional environment variables
        
        Returns:
            Formatted command string
        """
        cmd_str = " ".join(cmd)
        if env:
            # Only show non-sensitive environment variables
            safe_env = {
                k: v for k, v in env.items() 
                if not any(s in k.lower() for s in ["token", "key", "password", "secret", "auth"])
            }
            if safe_env:
                cmd_str += f"\nEnvironment: {safe_env}"
        return self._escape_markup(cmd_str)
    
    def start_operation(self, message: str) -> None:
        """Start a new operation with a status spinner.
        
        Args:
            message: Operation description
        """
        if self._status:
            self._status.stop()
        self._status = Status(message)
        self._status.start()
        self.log.info(message)
    
    def end_operation(self) -> None:
        """End the current operation."""
        if self._status:
            self._status.stop()
            self._status = None
    
    def command(self, cmd: List[str], env: Optional[Dict[str, str]] = None) -> None:
        """Log a command that will be executed.
        
        Args:
            cmd: Command parts
            env: Optional environment variables
        """
        self.console.print(f"[dim]$ {self._format_command(cmd, env)}[/dim]")
        self.log.debug("Executing command: %s", " ".join(cmd))
    
    def api_call(self, service: str, operation: str, params: Dict[str, Any]) -> None:
        """Log an API call that will be made.
        
        Args:
            service: Service name (e.g., "OpenAI")
            operation: Operation name
            params: Call parameters
        """
        # Remove sensitive parameters
        safe_params = {
            k: v for k, v in params.items() 
            if not any(s in k.lower() for s in ["token", "key", "password", "secret", "auth"])
        }
        self.console.print(
            f"[dim]{self._escape_markup(service)} API: {self._escape_markup(operation)}[/dim]"
        )
        if safe_params:
            self.console.print(f"[dim]Parameters: {self._escape_markup(str(safe_params))}[/dim]")
        self.log.debug("%s API call: %s %s", service, operation, safe_params)
    
    def success(self, message: str) -> None:
        """Log a success message.
        
        Args:
            message: Success message
        """
        self.end_operation()
        self.console.print(f"[green]✓[/green] {self._escape_markup(message)}")
        self.log.info(message)
    
    def warning(self, message: str) -> None:
        """Log a warning message.
        
        Args:
            message: Warning message
        """
        self.console.print(f"[yellow]![/yellow] {self._escape_markup(message)}")
        self.log.warning(message)
    
    def error(self, message: str) -> None:
        """Log an error message.
        
        Args:
            message: Error message
        """
        self.end_operation()
        self.console.print(f"[red]✗[/red] {self._escape_markup(message)}")
        self.log.error(message)
    
    def debug(self, message: str) -> None:
        """Log a debug message.
        
        Args:
            message: Debug message
        """
        self.log.debug(message)
    
    def panel(self, message: str, title: str, style: str = "green") -> None:
        """Display a message in a panel.
        
        Args:
            message: Panel content
            title: Panel title
            style: Panel style color
        """
        self.end_operation()
        self.console.print(Panel(
            self._escape_markup(message),
            title=f"[{style}]{self._escape_markup(title)}[/{style}]",
            border_style=style
        ))
    
    def validation_error(self, errors: List[Any], context: str) -> None:
        """Display validation errors in a panel.
        
        Args:
            errors: List of validation errors
            context: Error context
        """
        if not errors:
            return
        
        # Format error messages, escaping any rich markup
        error_messages = []
        for error in errors:
            msg = str(error)
            error_messages.append(self._escape_markup(msg))
        
        self.panel(
            "\n".join(error_messages),
            f"❌ {context} Failed",
            "red"
        )

# Global logger instance
logger = SafeLogger() 