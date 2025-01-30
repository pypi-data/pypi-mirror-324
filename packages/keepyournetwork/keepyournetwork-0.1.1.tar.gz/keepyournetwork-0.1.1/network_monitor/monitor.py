import psutil
import time
import platform
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.style import Style
from datetime import datetime
from typing import Dict, Tuple, Optional

class NetworkMonitor:
    """A powerful network monitoring tool that provides real-time network statistics."""
    
    def __init__(self):
        """Initialize the NetworkMonitor with necessary attributes."""
        self.console = Console()
        self.previous_net_io = None
        self.start_time = datetime.now()
        self.total_bytes_sent = 0
        self.total_bytes_recv = 0
        self.max_speed_up = 0
        self.max_speed_down = 0
        self.system_info = self._get_system_info()
        
    def _get_system_info(self) -> Dict[str, str]:
        """Get system information for monitoring context."""
        info = {
            'os': platform.system(),
            'os_version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'hostname': platform.node()
        }
        
        if info['os'] == 'Windows':
            info['windows_edition'] = platform.win32_edition()
        
        return info
    
    def get_network_usage(self) -> Tuple[Dict[str, float], Dict[str, int]]:
        """Get current network usage statistics."""
        try:
            net_io = psutil.net_io_counters()
            
            if self.previous_net_io is None:
                self.previous_net_io = net_io
                return {"upload": 0.0, "download": 0.0}, self._get_stats_dict(net_io)
            
            # Calculate speeds
            time_elapsed = 1.0  # Assumed time elapsed is 1 second
            upload_speed = (net_io.bytes_sent - self.previous_net_io.bytes_sent) / time_elapsed
            download_speed = (net_io.bytes_recv - self.previous_net_io.bytes_recv) / time_elapsed
            
            # Update maximum speeds
            self.max_speed_up = max(self.max_speed_up, upload_speed)
            self.max_speed_down = max(self.max_speed_down, download_speed)
            
            # Update totals
            self.total_bytes_sent = net_io.bytes_sent
            self.total_bytes_recv = net_io.bytes_recv
            
            # Store current values for next iteration
            self.previous_net_io = net_io
            
            return {
                "upload": upload_speed,
                "download": download_speed
            }, self._get_stats_dict(net_io)
            
        except Exception as e:
            self.console.print(f"[red]Error getting network usage: {str(e)}[/red]")
            return {"upload": 0.0, "download": 0.0}, self._get_empty_stats()
    
    def _get_stats_dict(self, net_io: Optional[psutil._common.snetio] = None) -> Dict[str, int]:
        """Convert network IO stats to dictionary format."""
        if net_io is None:
            return self._get_empty_stats()
        
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
            "errin": net_io.errin,
            "errout": net_io.errout,
            "dropin": net_io.dropin,
            "dropout": net_io.dropout
        }
    
    def _get_empty_stats(self) -> Dict[str, int]:
        """Return empty statistics dictionary."""
        return {
            "bytes_sent": 0,
            "bytes_recv": 0,
            "packets_sent": 0,
            "packets_recv": 0,
            "errin": 0,
            "errout": 0,
            "dropin": 0,
            "dropout": 0
        }
    
    def format_speed(self, bytes_per_sec: float) -> str:
        """Format speed values with appropriate units."""
        units = ['B/s', 'KB/s', 'MB/s', 'GB/s']
        unit_index = 0
        
        while bytes_per_sec >= 1024 and unit_index < len(units) - 1:
            bytes_per_sec /= 1024
            unit_index += 1
        
        return f"{bytes_per_sec:.2f} {units[unit_index]}"
    
    def format_bytes(self, bytes_val: int) -> str:
        """Format byte values with appropriate units."""
        units = ['B', 'KB', 'MB', 'GB']
        unit_index = 0
        
        while bytes_val >= 1024 and unit_index < len(units) - 1:
            bytes_val /= 1024
            unit_index += 1
        
        return f"{bytes_val:.2f} {units[unit_index]}"
    
    def create_speed_table(self, speeds: Dict[str, float], stats: Dict[str, int]) -> Table:
        """Create a table displaying current speed information."""
        table = Table(
            show_header=True,
            header_style="bold magenta",
            title="Network Speed Monitor",
            title_style="bold blue",
            border_style="bright_blue"
        )
        
        table.add_column("Direction", style="cyan", justify="center")
        table.add_column("Current Speed", style="green", justify="right")
        table.add_column("Maximum Speed", style="yellow", justify="right")
        table.add_column("Total Data", style="blue", justify="right")
        
        # Add upload row with arrow
        table.add_row(
            "⬆️ Upload",
            self.format_speed(speeds["upload"]),
            self.format_speed(self.max_speed_up),
            self.format_bytes(stats["bytes_sent"])
        )
        
        # Add download row with arrow
        table.add_row(
            "⬇️ Download",
            self.format_speed(speeds["download"]),
            self.format_speed(self.max_speed_down),
            self.format_bytes(stats["bytes_recv"])
        )
        
        return table
    
    def create_stats_table(self, stats: Dict[str, int]) -> Table:
        """Create a table displaying detailed network statistics."""
        table = Table(
            show_header=True,
            header_style="bold magenta",
            title="Network Statistics",
            title_style="bold blue",
            border_style="bright_blue"
        )
        
        table.add_column("Metric", style="cyan", justify="left")
        table.add_column("Sent", style="green", justify="right")
        table.add_column("Received", style="yellow", justify="right")
        
        # Add statistics rows
        table.add_row(
            "Packets",
            f"{stats['packets_sent']:,}",
            f"{stats['packets_recv']:,}"
        )
        
        table.add_row(
            "Errors",
            f"{stats['errout']:,}",
            f"{stats['errin']:,}"
        )
        
        table.add_row(
            "Dropped",
            f"{stats['dropout']:,}",
            f"{stats['dropin']:,}"
        )
        
        return table
    
    def create_session_info(self) -> Panel:
        """Create a panel displaying session information."""
        duration = datetime.now() - self.start_time
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        seconds = duration.seconds % 60
        
        # Calculate average speeds
        avg_upload = self.total_bytes_sent / max(1, duration.seconds)
        avg_download = self.total_bytes_recv / max(1, duration.seconds)
        
        return Panel(
            f"[yellow]Session Duration:[/yellow] {hours:02d}:{minutes:02d}:{seconds:02d}\n"
            f"[green]Start Time:[/green] {self.start_time.strftime('%H:%M:%S')}\n"
            f"[cyan]Average Upload:[/cyan] {self.format_speed(avg_upload)}\n"
            f"[cyan]Average Download:[/cyan] {self.format_speed(avg_download)}\n"
            f"[magenta]System:[/magenta] {self.system_info['os']} {self.system_info['machine']}\n"
            f"[magenta]Host:[/magenta] {self.system_info['hostname']}",
            title="Session Information",
            title_align="center",
            border_style="bright_blue",
            padding=(1, 2)
        )
    
    def monitor(self):
        """Start the network monitoring process."""
        try:
            self.console.clear()
            
            # Display title and instructions
            self.console.print("\n[bold blue]🌐 KeepYourNetwork Monitor[/bold blue]", justify="center")
            self.console.print("[dim]Press Ctrl+C to exit and view summary[/dim]\n", justify="center")
            
            # Create layout
            layout = Layout()
            layout.split_column(
                Layout(name="speed", ratio=2),
                Layout(name="bottom", ratio=3)
            )
            layout["bottom"].split_row(
                Layout(name="stats"),
                Layout(name="session")
            )
            
            # Start live display
            with Live(
                layout,
                refresh_per_second=2,
                screen=True,
                console=self.console
            ) as live:
                while True:
                    speeds, stats = self.get_network_usage()
                    
                    layout["speed"].update(self.create_speed_table(speeds, stats))
                    layout["stats"].update(self.create_stats_table(stats))
                    layout["session"].update(self.create_session_info())
                    
                    time.sleep(0.5)
                    
        except KeyboardInterrupt:
            self.console.clear()
            self.console.print("\n[yellow]Monitoring stopped![/yellow]")
            
            # Calculate final statistics
            duration = datetime.now() - self.start_time
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60
            seconds = duration.seconds % 60
            
            # Display summary
            self.console.print(Panel(
                f"[green]Total Monitoring Time:[/green] {hours:02d}:{minutes:02d}:{seconds:02d}\n"
                f"[cyan]Total Upload:[/cyan] {self.format_bytes(self.total_bytes_sent)}\n"
                f"[cyan]Total Download:[/cyan] {self.format_bytes(self.total_bytes_recv)}\n"
                f"[yellow]Maximum Upload Speed:[/yellow] {self.format_speed(self.max_speed_up)}\n"
                f"[yellow]Maximum Download Speed:[/yellow] {self.format_speed(self.max_speed_down)}\n"
                f"[magenta]System:[/magenta] {self.system_info['os']} {self.system_info['machine']}\n"
                f"[magenta]Session Start:[/magenta] {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}",
                title="📊 Session Summary",
                title_align="center",
                border_style="bright_blue",
                padding=(1, 2)
            ))
            
        except Exception as e:
            self.console.print(f"\n[red]Error occurred: {str(e)}[/red]") 