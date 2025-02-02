import typer
from rich.console import Console
from rich.table import Table
from datetime import datetime
import getpass
import random
from .database import DatabaseManager
from .security import SecurityManager

app = typer.Typer(help="Secure Password Manager CLI")
console = Console()
db = DatabaseManager()
security = SecurityManager()

def generate_secure_password(length: int = 16, no_special: bool = False) -> str:
    """Generate password with guaranteed complexity"""
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower = "abcdefghijklmnopqrstuvwxyz"
    digits = "0123456789"
    special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one of each required type
    password = [
        random.SystemRandom().choice(upper),
        random.SystemRandom().choice(lower),
        random.SystemRandom().choice(digits)
    ]
    
    if not no_special:
        password.append(random.SystemRandom().choice(special))
        length = max(length, 12)  # Minimum length for complex passwords
    else:
        length = max(length, 8)
    
    # Fill remaining characters
    chars = upper + lower + digits
    if not no_special:
        chars += special
    
    password += [
        random.SystemRandom().choice(chars)
        for _ in range(length - len(password))
    ]
    
    random.SystemRandom().shuffle(password)
    return ''.join(password)

def get_master_key() -> bytes:
    """Prompt for master password and return encryption key"""
    try:
        password = getpass.getpass("Enter master password: ")
        return db.verify_master_password(password)
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def init():
    """Initialize the password manager with a master password"""
    try:
        typer.echo("Set up your master password (minimum 12 characters with mix of upper/lower case, numbers, and symbols)")
        while True:
            password = getpass.getpass("Enter new master password: ")
            confirm = getpass.getpass("Confirm master password: ")
            
            if password != confirm:
                typer.echo("Passwords do not match!", err=True)
                continue
                
            if not security.check_password_complexity(password):
                typer.echo("Password does not meet complexity requirements!", err=True)
                continue
                
            db.initialize_master_password(password)
            typer.echo("✅ Master password set up successfully!")
            return
            
    except Exception as e:
        typer.echo(f"Initialization failed: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def save(
    website: str = typer.Option(..., prompt=True),
    email: str = typer.Option(..., prompt=True),
    password: str = typer.Option(None, "--password", "-p"),
    generate: bool = typer.Option(False, "--generate", "-g")
):
    """Save new password entry"""
    master_key = get_master_key()
    
    if generate and not password:
        password = generate_secure_password()
    elif not password:
        password = getpass.getpass("Enter password: ")
    
    db.save_password_entry(master_key, website, email, password)
    typer.echo("✅ Entry saved successfully!")

@app.command()
def list(
    website: str = typer.Option(None, "--website", "-w"),
    show_password: bool = typer.Option(False, "--show-password", "-s")
):
    """List password entries"""
    master_key = get_master_key()
    entries = db.get_password_entries(master_key, website)
    
    if not entries:
        typer.echo("No entries found")
        return
    
    table = Table(title="Password Entries")
    table.add_column("ID", justify="right")
    table.add_column("Website")
    table.add_column("Email")
    table.add_column("Password")
    table.add_column("Created At")

    for entry in entries:
        password = db.decrypt_password(master_key, entry.encrypted_password) if show_password else "*******"
        table.add_row(
            str(entry.id),
            entry.website,
            entry.email,
            password,
            entry.created_at.strftime("%Y-%m-%d %H:%M")
        )
    
    console.print(table)

@app.command()
def generate(
    length: int = typer.Option(16, "--length", "-l", min=8),
    no_special: bool = typer.Option(False, "--no-special")
):
    """Generate a secure password"""
    password = generate_secure_password(length, no_special)
    typer.echo(f"Generated password: {password}")

if __name__ == "__main__":
    app()