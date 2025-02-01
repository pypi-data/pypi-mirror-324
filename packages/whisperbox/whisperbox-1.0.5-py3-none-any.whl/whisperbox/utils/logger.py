from rich.console import Console
from rich.theme import Theme
from rich.style import Style
from datetime import datetime
from typing import Optional
import sys
from rich.table import Table
from ..core.config import config

# Custom theme for consistent colors
THEME = Theme({
    'info': 'cyan',
    'warning': 'yellow', 
    'error': 'red',
    'success': 'green',
    'debug': 'dim blue',
    'timestamp': 'dim white',
    'recording': 'bold red',
    'transcribing': 'bold yellow',
    'done': 'bold green',
    'save': 'green',
    'header': 'bold magenta'  # Added header style
})

class Logger:
    def __init__(self):
        self.console = Console(theme=THEME)
        self.debug_mode = False
        self.ui_callback = None
        
    def set_ui_callback(self, callback):
        """Set a callback function that will be called with log messages for UI display."""
        self.ui_callback = callback
        
    def _format_message(self, message: str, style: Optional[str] = None) -> str:
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[timestamp]{timestamp}[/timestamp] {message}"
        if style:
            formatted = f"[{style}]{message}[/{style}]\n"
        return formatted
        
    def _log_to_ui(self, message: str):
        """Send log message to UI if callback is set."""
        if self.ui_callback:
            timestamp = datetime.now().strftime("%H:%M:%S")
            ui_message = f"{timestamp} {message}\n"
            self.ui_callback(ui_message)
        
    def info(self, message: str):
        """Log an informational message"""
        self.console.print(self._format_message(message, "info"))
        self._log_to_ui(f"ℹ️ {message}")
        
    def warning(self, message: str):
        """Log a warning message"""
        self.console.print(self._format_message(f"⚠️  {message}\n", "warning"))
        self._log_to_ui(f"⚠️ {message}")
        
    def error(self, message: str):
        """Log an error message"""
        self.console.print(self._format_message(f"❌ {message}", "error"))
        self._log_to_ui(f"❌ {message}")
        
    def success(self, message: str):
        """Log a success message"""
        self.console.print(self._format_message(f"✅ {message}", "success"))
        self._log_to_ui(f"✅ {message}")
        
    def done(self, message: str):
        """Log a done message"""
        self.console.print(self._format_message(f"🎉 {message}", "done"))
        self._log_to_ui(f"🎉 {message}")
        
    def debug(self, message: str):
        """Log a debug message (only in debug mode)"""
        if self.debug_mode:
            self.console.print(self._format_message(f"🔍 {message}", "debug"))
            self._log_to_ui(f"🔍 {message}")
            
    def recording(self, message: str):
        """Log a recording-related message"""
        self.console.print(self._format_message(f"🎤 {message}", "recording"))
        self._log_to_ui(f"🎤 {message}")
        
    def transcribing(self, message: str):
        """Log a transcription-related message"""
        self.console.print(self._format_message(f"📝 {message}", "transcribing"))
        self._log_to_ui(f"📝 {message}")
        
    def save(self, message: str):
        """Log a save-related message"""
        self.console.print(self._format_message(f"💾 {message}", "save"))
        self._log_to_ui(f"💾 {message}")
        
    def status(self, message: str):
        """Update the current status"""
        self.console.print(self._format_message(message))
        self._log_to_ui(message)

    def header(self, message: str):
        """Log a header message that stands out"""
        self.console.print(f"\n[header]═══ {message} ═══[/header]\n")
        self._log_to_ui(f"\n═══ {message} ═══\n")
        
    def clear(self):
        """Clear the console and UI log if available"""
        self.console.clear()
        if self.ui_callback:
            self.ui_callback("", clear=True)  # Special flag to clear the log

    def print_header(self):
        """Print the app header."""
        self.clear()
        self.console.print("\n[bold blue]🎙️  WhisperBox[/bold blue]")
        
    def print_instructions(self):
        """Print usage instructions."""

        # Print commands
        self.console.print("\n[cyan]Commands:[/cyan]")
        for cmd, details in config.commands.items():
            if isinstance(details, dict) and 'description' in details:
                self.console.print(f"  [cyan]{cmd:<8}[/cyan] {details['description']}")
        
        self.console.print()

    def show_recording_status(self, is_recording: bool, is_paused: bool):
        """Show the current recording status."""
        if is_recording:
            status = "⏸️  Paused" if is_paused else "🔴  Recording..."
            style = "warning" if is_paused else "recording"
        else:
            status = "⏹️  Ready"
            style = "success"
            
        self.console.print(self._format_message(status, style))
        
    def show_audio_sources(self, mic: str, system: Optional[str] = None):
        """Display current audio sources."""
        self.info(f"Using microphone: {mic}")
        if system:
            self.info(f"System audio: {system}")

    def print_help(self):
        """Print detailed help information."""
        self.clear()
        self.print_header()
        
        # Commands section with table
        self.console.print("\n[bold cyan]Available Commands:[/bold cyan]")
        cmd_table = Table(show_header=False, padding=(0, 2))
        cmd_table.add_column(style="cyan", justify="left")
        cmd_table.add_column(style="white", justify="left")
        
        for cmd, details in config.commands.items():
            if isinstance(details, dict) and 'description' in details:
                cmd_table.add_row(cmd, details['description'])
        self.console.print(cmd_table)
        
        # Features and tips remain the same
        self.console.print("\n[bold cyan]Recording Features:[/bold cyan]")
        self.console.print("  • Records from both microphone and system audio (if available)")
        self.console.print("  • Automatically transcribes after recording stops")
        self.console.print("  • Provides AI-powered summary and analysis")
        self.console.print("  • Saves recordings to the 'recordings' directory")
        
        self.console.print("\n[bold cyan]Tips:[/bold cyan]")
        self.console.print("  • Install BlackHole for system audio capture")
        self.console.print("  • Use 'devices' command to check audio inputs")
        self.console.print("  • Configure Whisper model in config for better accuracy")
        
        self.console.print("\nPress Enter to return to main screen...")

# Global logger instance
log = Logger() 