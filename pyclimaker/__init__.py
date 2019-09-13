class PyCliMain():
    def __init__(self):
        self.MESSAGE_PROMPT = "Enter command you want to execute: "
        self.MESSAGE_PROMPT_INVALID_COMMAND = "This is an invalid key"
        self.MESSAGE_EXIT = "Aborting the programme"
        self.cli_commmands = {
            # "help": help_command,
            # "exit": exit_command
        }
    
    def add_cli_command(self, cli_command):
        if isinstance(cli_command, PyCliFunctionPrompt):
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

class PyCliFunctionPrompt():
    def __init__(self, function, description):
        if callable(function) == False: # What really matters is if some variable does some operations
            raise Exception("Invalid argument. function must be a type of callable.")
        
        argcount_non_defaults = function.__code__.co_argcount - len(function.__defaults__)
        
        # Initialisation
        self.function = function
        self.function_args = {} # Can be either defined by developers or inputted by users
        for i in range(function.__code__.co_argcount):
            if argcount_non_defaults < i: #function.__defaults__[i]  else None
                default_at_function = function.__defaults__[i]
            else:
                default_at_function = None
            
            self.function_args[function.__code__.co_varnames[i]] = {
                "is_predefined": False,
                "default_at_cli": None,
                "default_at_function": default_at_function
            }

        self.function_args_aliases = {key: key for key in self.function_args.keys()}
        self.description = description
        
        # Properties to be filled by the developer
        self.arg_prompts = {}

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
        if isinstance(arg_prompt, PyCliArgPrompt) == False:
            raise Exception("Invalid argument. arg_prompt must be a type of PyCliArgPrompt (or its inheritance?)")
        
        if isinstance(command_to_bind, str) == False:
            # NOTE MAYBE I CAN LOOSEN THE RESTIRCTION TO ACCEPT TYPES LIKE INTS
            raise Exception()
            
        if command_to_bind not in self.function_args_aliases:
            # Any input that doesn't contribute to specifying argument to the function is considered invalid

            raise Exception("Invalid binding. ")

        if self.function_args_aliases[command_to_bind] in self.arg_prompts:
            raise Exception("Overring arg_prompt")

        self.arg_prompts[command_to_bind] = arg_prompt

    def trigger(self):
        # Do base prompting
        args_to_pass = {}
        
        # Prepare arguments to pass using CLI defaults and functions defaults
        for arg_name, arg_value in self.function_args.items():
            if arg_value["default_at_cli"] != None:
                arg_value_to_pass = arg_value["default_at_cli"]
            elif arg_value["default_at_function"] != None:
                arg_value_to_pass = arg_value["default_at_function"]
            else:
                arg_value_to_pass = None

            args_to_pass[arg_name] = arg_value_to_pass

        # Prepare arguments using user inputs
        for arg_name, arg_prompt in self.arg_prompts.items():
            args_to_pass[arg_name] = arg_prompt.trigger()

        self.function(**args_to_pass)


class PyCliArgPrompt():
    def __init__(self, message):
        self.message = message
    
    def execute(self):
        # Do base prompting

        # if input which triggers binded action is givern
        pass