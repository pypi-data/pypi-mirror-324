from time import gmtime, strftime
class Logging:
    def __init__(self, len=30):
        self.colors = {
            "Black": '\033[30m',
            "Red": '\033[31m',
            "Green": '\033[32m',
            "Yellow": '\033[33m',
            "Blue": '\033[34m',
            "Purple": '\033[35m',
            "Cyan": '\033[36m',
            "White": '\033[37m',
            "BBlack": '\033[90m',
            "BRed": '\033[91m',
            "BGreen": '\033[92m',
            "BYellow": '\033[93m',
            "BBlue": '\033[94m',
            "BPurple": '\033[95m',
            "BCyan": '\033[96m',
            "BWhite": '\033[97m'
        }
        self.__ENDC = '\033[0m'       # Normal Terminal Color
        self.__BOLD = '\033[1m'       # Bold
        self.__UNDERLINE = '\033[4m'  # Underline

        # Default minimum length for formatting
        self.len = max(30, len)
        
        self.logColourDeafults = {
            "header": self.colors['BPurple'],
            "info": self.colors['BCyan'],
            "warning": self.colors['BYellow'],
            "error": self.colors['BRed'],
            "success": self.colors['BGreen'],
            "beans": self.colors['BBlue'],
            "input": self.colors['Yellow'],
        }
        
        

    def __str__(self):
        return f"""
        This is a logging system.
        There is only 1 parameter and its not required:
        - Length, deafult = 30 (values under 30 will not be accepted)
        Your Value is: {self.len}
        """
    
    def __creator(self, title, colour, text, bold=False, underlined=False, enditem='\n'):
        """
        underlined and bold are for the actual text, not for the header
        """
        try:
            time = strftime("[%d/%m/%y %H:%M:%S] ", gmtime())  # Format the time
            title = title.upper() 
            # Calculate number of dots needed, the -1 is to stop it from growing
            dots = (self.len - (len(title) + len(time))) - 1

            # Ensure the length is dynamically adjusted if needed
            prefix_length = len(f"{time}{title}{'.' * dots}:")
            if prefix_length > self.len:
                self.len = prefix_length

            # Recalculate dots after adjusting self.len
            dots = (self.len - (len(title) + len(time))) #- 1
            dotString = '.' * dots

            # Define color and text styles
            end = self.__ENDC
            bold = self.__BOLD              if bold         else ''
            underlined = self.__UNDERLINE   if underlined   else ''

            # Full prefix with color
            prefix = f"{colour}{time}{title}{dotString}:{end} "
            continuation_prefix = ' ' * (self.len + 2) # 2 for the extra space to make the wrapped text look nicer

            # Break the text into lines
            wrapped_lines = []
            line_length = 160 - self.len  # Adjust line length to account for prefix
            words = text.split(' ')  # Only remove trailing spaces if necessary
            current_line = ""

            for word in words:
                if len(current_line) + len(word) + 1 > line_length:
                    wrapped_lines.append(current_line)
                    current_line = word
                else:
                    if current_line:
                        current_line += " "
                    current_line += word
            wrapped_lines.append(current_line)

            # Format the message with wrapped lines
            formatted_text = f"{prefix}{underlined}{bold}{wrapped_lines[0]}{end}"
            for line in wrapped_lines[1:]:
                formatted_text += f"\n{continuation_prefix}{line}"

            print(formatted_text, end=enditem)
            return True
        except Exception as e:
            return e



    
    def header(self, text, bold=False, underlined=False):
        self.__creator(
            title="header",
            colour=self.logColourDeafults['header'], 
            text=text,
            bold=bold,
            underlined=underlined
        )

    def info(self, text, bold=False, underlined=False):
        self.__creator(
            title="info", 
            colour=self.logColourDeafults['info'], 
            text=text,
            bold=bold,
            underlined=underlined
        )

    def warning(self, text, bold=False, underlined=False):
        self.__creator(
            title="warning", 
            colour=self.logColourDeafults['warning'], 
            text=text,
            bold=bold,
            underlined=underlined
        )

    def error(self, text, bold=False, underlined=False):
        self.__creator(
            title="error", 
            colour=self.logColourDeafults['error'], 
            text=text,
            bold=bold,
            underlined=underlined
        )

    def success(self, text, bold=False, underlined=False):
        self.__creator(
            title="success", 
            colour=self.logColourDeafults['success'], 
            text=text,
            bold=bold,
            underlined=underlined
        )
    
    def beans(self, text, bold=False, underlined=False):
        self.__creator(
            title='beans',
            colour=self.logColourDeafults['beans'],
            text=text,
            bold=bold,
            underlined=underlined
        )
    
    def input(self, text, bold=False, underlined=False):
        self.__creator(
            title='input',
            colour=self.logColourDeafults['input'],
            text=text,
            bold=bold,
            underlined=underlined,
            enditem='' # Make the end of the print empty to be able to input on the same line 
        )
        choice = input() # I don't know how this still works lmao
        return choice
    
    def set_colour(self, method: str, colour: str):
        """
        Lets you change the colour for an already existing method
        """
        if colour not in self.colors.keys():
            if colour not in self.colors.values():
                self.error("Invalid colour name/code")
                self.info(f"All of the deafult colours names: {', '.join(self.colors.keys())}")
                self.info(f"All of the deafult colours codes: {self.colors.values()}")
                return
        
        methods = ['info', 'success', 'error', 'warning', 'beans', 'input', 'header']
        if method.lower() not in methods:
            self.error("Invalid method name")
            self.info(f"All method names: {''.join(methods)}")
            return
        
        if not colour.startswith('\033['):
            if colour in self.colors.keys():
                colour = self.colors[colour]
            
        self.logColourDeafults[method] = colour





class CustomLog(Logging):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dColour = None
        self.dTitle = None
        self.dBold = None
        self.dUnderlined = None
    
    def __str__(self):
        return f"""
        This is a modified version of Logging() that allows you to create your own log
        Use the set_deafult() method to change the deafults of the logs, or just use the custom_log() method with all the parameters
        You can add your own colours
        All of the deafult colours: {', '.join(self.colors.keys())}
        'B' stands for Bright
        """

    def add_color(self, name, code):
        """
        Add a custom color to the colors dictionary.
        """
        
        if not name or not code.startswith('\033['):
            self.error("Invalid color name or code. Ensure the code is an ANSI escape sequence.")
            pass
        self.colors[name] = code

    def custom_log(
            self,
            text,  
            title = None, 
            color = None, 
            bold = False, 
            underlined = False
        ):
        """
        Custom log method that allows you to specify a title and color.
        Falls back to the default color if no color is provided.
        """
        try:
            color = color or self.dColour  # Use provided color or fall back to default
            if color not in self.colors:
                self.error(f"Invalid color '{color}'. Available colors: {', '.join(self.colors.keys())}")
            
            title = title           if title        else self.dTitle
            color = color           if color        else self.dColour
            bold = bold             if bold         else self.dBold
            underlined = underlined if underlined   else self.dUnderlined
            
            
            self._Logging__creator(  # Accessing the protected method from the parent class
                title = title,
                colour = self.colors[color],
                text = text,
                bold = bold,
                underlined = underlined
            )
        except Exception as e:
            self.error("Make sure you have ran the set_default method first")
            self.error(f"If that is the case your error is: {e}")


    def set_default_custom(
            self, 
            title: str, 
            color: str, 
            bold: bool = False, 
            underlined: bool = False
        ):
        
        """
        Set default log parameters: title, color, bold, and underlined.
        """
        
        try:
            # Validate title
            if not title or not isinstance(title, str):
                self.error("Invalid title: Title must be a non-empty string.")
                return False

            # Validate color
            if color not in self.colors:
                self.error(f"Invalid color '{color}'. Available colors: {', '.join(self.colors.keys())}")
                return False

            # Validate bold and underlined as booleans
            if not isinstance(bold, bool):
                self.error("Invalid bold parameter: Must be a boolean.")
                return False
            if not isinstance(underlined, bool):
                self.error("Invalid underlined parameter: Must be a boolean.")
                return False

            # Set default values
            self.dColour = color
            self.dTitle = title
            self.dBold = bold
            self.dUnderlined = underlined

            # Log success
            return True
        except Exception as e:
            # Log the error and re-raise it
            self.error(f"Failed to set default settings: {e}")
            raise
    
    
    def view_deafult(self):
        self.info(f"Default settings: Title='{self.dTitle}', Color='{self.dColour}', Bold={self.dBold}, Underlined={self.dUnderlined}")

        

if __name__ == '__main__':
    # Make sure to define the class
    mylogger = Logging()
    print(mylogger)
    mylogger.header("Header")
    mylogger.info("Info")
    mylogger.warning("Warning")
    mylogger.error("Error")
    mylogger.success("Success")
    mylogger.beans("Beans")
    mylogger.info("This is a very long log message that is going to spill over to the next line and needs to be properly indented for better readability.")
    mylogger.info("This is info")
    mylogger.set_colour('info', 'BBlack')
    mylogger.info("This is the new info")
    num = mylogger.input("This is an input, please enter a number: ")
    mylogger.info(f"The user has entered: {num}")
    
    customLogger = CustomLog()
    print(customLogger)
    customLogger.set_default_custom(title="beansareyummy", color='Blue')
    customLogger.view_deafult()
    customLogger.custom_log("This is a custom log")
    customLogger.info("The deafult length has been adjusted to suit the longest log")

    