import termcolor

INFO_COLOR = 'blue'   # Use to display additional information
ERROR_COLOR = 'red'   # Use when an expectation is not met
VALID_COLOR = 'green' # Use when something has been validated

def color_print(text, color):
  print(
        termcolor.colored(text, color=color, attrs=['bold']))
