import os
from rich import print as rprint

def printart(filename):
    art = """
 ██████  ██████  ██████  ███████ ██████   █████  ███████ ███████  ██████  ███    ██  █████  
██      ██    ██ ██   ██ ██      ██   ██ ██   ██ ██      ██      ██    ██ ████   ██ ██   ██ 
██      ██    ██ ██   ██ █████   ██████  ███████ ███████ █████   ██    ██ ██ ██  ██ ███████ 
██      ██    ██ ██   ██ ██      ██   ██ ██   ██      ██ ██      ██ ▄▄ ██ ██  ██ ██ ██   ██ 
 ██████  ██████  ██████  ███████ ██████  ██   ██ ███████ ███████  ██████  ██   ████ ██   ██ 
                                                                     ▀▀                     
                                                                                         
"""

    lines = art.splitlines()

    # Get terminal width
    try:
        columns, _ = os.get_terminal_size()
    except OSError:
        # Default width if terminal size cannot be determined
        columns = 80

    for line in lines:
        rprint(f"[red]{line.center(columns)}[/red]")
    
    intro = "Welcome to CodebaseQnA - Your Personal Codebase Assistant! I am Codey and I'll be here to answer any questions about your codebase: " + filename + "!"
    print(f"{intro.center(columns)}")
    rprint("[bright_red]Press Q to quit![/bright_red]".center(columns))