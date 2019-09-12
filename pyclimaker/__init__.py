class PyCLIMain():
    def __init__(self):
        self.MESSAGE_PROMPT = "Enter command you want to execute: "
        self.MESSAGE_PROMPT_INVALID_COMMAND = "This is an invalid key"
        self.MESSAGE_EXIT = "Aborting the programme"
        self.cli_commmands = {
            # "help": help_command,
            # "exit": exit_command
        }
    
    def add_cli_command(self, cli_command):
        if isinstance(cli_command, PyCLICommand):
            self.cli_commmands[cli_command.command] = cli_command
        else:
            raise Exception

    def build(self):
        # Generate help message ... ?
        # Generate prompt-command-excution loop
        while True:
            print(self.MESSAGE_PROMPT)
            command = input()
            if command == "exit":
                print(self.MESSAGE_EXIT)
            elif command in self.cli_commmands.keys():
                self.cli_commmands[command].run()

            else:
                print(self.MESSAGE_PROMPT_INVALID_COMMAND)

            




class PyCLICommand():
    def __init__(self, function):
        # Define command name
        # Add help message
        self.command = ""
        self.help_message = ""
        
        self.function = None
        self.function_args = {} # Can be either defined by developers or inputted by users
        self.function_args_aliases = {}
        self.valid_inputs = []

        # Initialisation with internal methods 
        self.bind_function(function)

    def bind_function(self, function):
        if callable(function) == False: # What really matters is if some variable does some operations
            raise Exception("Invalid argument. function must be a type of callable.")
        
        self.function = function
        self.function_args = {}
        argcount_non_defaults = len(function.__code__.co_argcount - function.__defaults__)
        for index in range(function.__code__.co_argcount):
            key = function.__code__.co_varnames[index]
            value_default_at_function = argcount_non_defaults <= index? function.__defaults__[index]: None

            self.function_args[key] = {
                "is_predefined": False,
                "default_at_cli": None,
                "default_at_function": value_default_at_function
            }

        self.function_args_aliases = {key: key for key in self.function_args.keys()}

    def bind_function_args_aliases(self, alias, arg_name):
        if isinstance(alias, str) == False:
            raise Exception()
        if arg_name not in self.function_args:
            raise Exception()

    def bind_default_arguments(self, arg_alias, arg_value, is_predefined):
        if arg_alias not in self.function_args_aliases.keys():
            raise Exception("Invalid arg_name")
        
        arg_name = self.function_args_aliases[arg_alias]
        self.function_args[arg_name].is_predefined = is_predefined
        self.function_args[arg_name].arg_value = default_at_cli
        
    def bind_arg_prompt(self, arg_prompt, command_to_bind):
        if isinstance(arg_prompt, PyCLIArgPrompt) == False:
            raise Exception("Invalid argument. arg_prompt must be a type of PyCLIArgPrompt (or its inheritance?)")
        
        if isinstance(command_to_bind, str) == False:
            # NOTE MAYBE I CAN LOOSEN THE RESTIRCTION TO ACCEPT TYPES LIKE INTS
            raise Exception()
            
        if command_to_bind not in self.valid_commands:
            # Any input that doesn't contribute to specifying argument to the function is considered invalid

            raise Exception("Invalid binding. ")



    def execute(self):
        # Do base prompting

        # if input which triggers binded action is givern
        for prompt in self.prompts:
            prompt.execute

        pass


class PyCLIArgPrompt():
    def __init__(self, message):
        self.message = message
    
    def execute(self):
        # Do base prompting

        # if input which triggers binded action is givern