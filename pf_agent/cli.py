"""Main CLI interface using Typer"""

import typer
from typing import Optional, Annotated
from pathlib import Path
from rich.console import Console
from rich.table import Table

from .domain.services import LicenseService
from .tools.scheduler import start_scheduler
from .simulators.pingfed_mock import run_simulator
from .agents.crew import route_intent

app = typer.Typer(
    name="pf-agent",
    help="PingFederate Ops Agent - License Management CLI",
    add_completion=False
)
console = Console()

@app.callback()
def main() -> None:
    """PingFederate Ops Agent - License Management with AI"""
    # Start the scheduler when any command is run
    start_scheduler()


@app.command()
def run(
    query: Annotated[str, typer.Argument(help="Natural language query")],
    instance: Annotated[Optional[str], typer.Option("--instance", help="Target instance ID")] = None,
    no_nl: Annotated[bool, typer.Option("--no-nl", help="Skip natural language processing")] = False
) -> None:
    """Run a natural language command using CrewAI intent routing"""
    try:
        if no_nl:
            # Default to license get if no NL processing
            _show_license_status(instance)
        else:
            result = route_intent(query, instance)
            console.print(result)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


# License management commands
license_app = typer.Typer(name="license", help="License management commands")
app.add_typer(license_app)


@license_app.command()
def get(
    instance: Annotated[Optional[str], typer.Option("--instance", help="Specific instance ID")] = None
) -> None:
    """Get license information from cache"""
    _show_license_status(instance)


@license_app.command()
def apply(
    instance: Annotated[str, typer.Option("--instance", help="Target instance ID")],
    file: Annotated[Path, typer.Option("--file", help="License file path")]
) -> None:
    """Apply a new license to an instance"""
    try:
        if not file.exists():
            console.print(f"[red]License file not found: {file}[/red]")
            raise typer.Exit(1)
            
        service = LicenseService()
        result = service.apply_license(instance, str(file))
        
        console.print("[green]License applied successfully![/green]")
        console.print(f"Instance: {result.instance_id}")
        console.print(f"New expiry: {result.expiry_date}")
        console.print(f"Status: {result.status}")
        
        # Show simulated Slack notification
        if result.status in ['WARNING', 'EXPIRED']:
            days = result.days_to_expiry
            console.print(f"\n[yellow][SLACK] PF License {result.status}: instance={instance} expires in {days}d ({result.expiry_date})[/yellow]")
        else:
            console.print(f"\n[green][SLACK] PF License updated: instance={instance} expires {result.expiry_date} (Status: {result.status})[/green]")
            
    except Exception as e:
        console.print(f"[red]Error applying license: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def refresh() -> None:
    """Manually trigger license refresh for all instances"""
    try:
        console.print("[blue]Starting manual license refresh...[/blue]")
        service = LicenseService()
        results = service.refresh_all()
        
        # Show summary
        warnings = [r for r in results if r['status'] == 'WARNING']
        expired = [r for r in results if r['status'] == 'EXPIRED']
        
        console.print(f"[green]Refresh completed: {len(results)} instances processed[/green]")
        
        if warnings:
            console.print(f"[yellow]⚠️  {len(warnings)} instances with warnings[/yellow]")
            for w in warnings:
                console.print(f"[yellow][SLACK] PF License WARNING: instance={w['instance_id']} expires in {w['days_to_expiry']}d ({w['expiry_date']})[/yellow]")
                
        if expired:
            console.print(f"[red]🚨 {len(expired)} instances expired[/red]")
            for e in expired:
                console.print(f"[red][SLACK] PF License EXPIRED: instance={e['instance_id']} expired {abs(e['days_to_expiry'])}d ago ({e['expiry_date']})[/red]")
                
    except Exception as e:
        console.print(f"[red]Error during refresh: {e}[/red]")
        raise typer.Exit(1)


# Simulator commands
simulate_app = typer.Typer(name="simulate", help="PingFederate API simulator")
app.add_typer(simulate_app)


@simulate_app.command()
def up(
    port: Annotated[int, typer.Option("--port", help="Port to run simulator on")] = 8080
) -> None:
    """Start the PingFederate API simulator"""
    console.print(f"[blue]Starting PingFederate API simulator on port {port}...[/blue]")
    console.print("[green]Available endpoints:[/green]")
    for i in range(1, 6):
        console.print(f"  - http://localhost:{port}/pf{i}/license (GET/PUT)")
        console.print(f"  - http://localhost:{port}/pf{i}/license/agreement (GET/PUT)")
    
    run_simulator(port)


def _show_license_status(instance_id: Optional[str] = None) -> None:
    """Helper to display license status in a table"""
    try:
        service = LicenseService()
        
        if instance_id:
            records = [service.get_license(instance_id)]
        else:
            records = service.get_all_licenses()
            
        if not records:
            console.print("[yellow]No license data found. Run 'pf-agent refresh' first.[/yellow]")
            return
            
        # Create rich table
        table = Table(title="PingFederate License Status")
        table.add_column("Instance", style="cyan", no_wrap=True)
        table.add_column("Env", style="magenta")
        table.add_column("Issued To", style="green")
        table.add_column("Product", style="blue")
        table.add_column("Expiry", style="yellow")
        table.add_column("Days", justify="right")
        table.add_column("Status", style="bold")
        table.add_column("Last Synced", style="dim")
        
        for record in records:
            # Color code status
            status_style = {
                'OK': '[green]OK[/green]',
                'WARNING': '[yellow]WARNING[/yellow]', 
                'EXPIRED': '[red]EXPIRED[/red]'
            }.get(record['status'], record['status'])
            
            table.add_row(
                record['instance_id'],
                record['env'],
                record['issued_to'],
                record['product'],
                record['expiry_date'][:10],  # Just date part
                str(record['days_to_expiry']),
                status_style,
                record['last_synced_at'][:16].replace('T', ' ')  # Readable timestamp
            )
            
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error retrieving license data: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
