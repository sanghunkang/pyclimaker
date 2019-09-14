# from .exceptions import InvalidBindingAttemptException
from .argprompts import PyCliArgPrompt

class PyCliMain():
    def __init__(self):
        self.MESSAGE_PROMPT_INVALID_COMMAND = "This is an invalid key"
        self.MESSAGE_EXIT = "Aborting the programme"
        self.help_message = "This is a help message"
        self.functions = {}
    
    def bind_function(self, function_prompt, cli_command):
        if isinstance(function_prompt, PyCliFunctionPrompt) == False:
            raise Exception("Invalid attempt to bind an invalid function_prompt") 
        
        self.functions[cli_command] = function_prompt
        # Modify help message

    def run(self):
        print(f"\033[1mStarting the programme\033[0m")

        # Prompt-command-excution loop
        while True:
            print(f"\033[1mEnter function(alias) you want to execute:\033[0m", end=" ")
            command = input()
            
            if command in self.functions.keys():
                self.functions[command].trigger()
            elif command == "help":
                print(self.help_message)
            elif command == "exit":
                print(self.MESSAGE_EXIT)
                break
            else:
                print(self.MESSAGE_PROMPT_INVALID_COMMAND)
            print()


class PyCliFunctionPrompt():
    def __init__(self, function, description):
        # Type checks
        if callable(function) == False:
            raise Exception("function must be a callable.")
        
        # Define helper variables
        if function.__defaults__ != None:
            argcount_non_defaults = function.__code__.co_argcount - len(function.__defaults__)
        else:
            argcount_non_defaults = function.__code__.co_argcount

        # Initialise attributes
        self.function = function
        self.description = description
        
        self.function_args = {} # Can be either defined by developers or inputted by users
        for i in range(function.__code__.co_argcount):
            if argcount_non_defaults < i:
                default_at_function = function.__defaults__[i]
            else:
                default_at_function = None
            
            self.function_args[function.__code__.co_varnames[i]] = {
                "is_predefined": False,
                "default_at_cli": None,
                "default_at_function": default_at_function
            }
        self.function_args_aliases = {key: key for key in self.function_args.keys()}
        
        # Properties to be filled by the developer
        self.arg_prompts = {}

    def bind_function_args_aliases(self, alias, arg_name):
        # Type checks
        if isinstance(alias, str) == False:
            raise TypeError("alias must be of type 'str'")

        if isinstance(arg_name, str) == False:
            raise TypeError("arg_name must be of type 'str'")

        # Runtime checks
        if arg_name not in self.function_args:
            raise Exception()

        self.function_args_aliases[alias] = arg_name

    def bind_default_cli_arg(self, arg_alias, arg_value, is_predefined):
        # Type checks
        if isinstance(arg_alias, str) == False:
            raise TypeError("arg_alias must be of type 'str'")

        if isinstance(is_predefined, bool) == False:
            raise Exception("is_predefined must be of type 'bool'")

        # Runtime checks
        if arg_alias not in self.function_args_aliases.keys():
            raise Exception("Invalid arg_name")
        
        arg_name = self.function_args_aliases[arg_alias]
        self.function_args[arg_name]["is_predefined"] = is_predefined
        self.function_args[arg_name]["default_at_cli"] = arg_value 
        
    def bind_arg_prompt(self, arg_prompt, command_to_bind):
        # Type checks
        if isinstance(arg_prompt, PyCliArgPrompt) == False:
            raise TypeError("arg_prompt must be of type <class 'PyCliArgPrompt'>")
        
        if isinstance(command_to_bind, str) == False:
            raise TypeError("command_to_bind must be of type 'str'")

        # Runtime checks 
        if command_to_bind not in self.function_args_aliases:
            # Any input that doesn't contribute to specifying argument to the function is considered invalid
            raise Exception("Invalid binding. ")

        if self.function_args[self.function_args_aliases[command_to_bind]]["is_predefined"]:
            raise Exception("Invalid attempt to overide predefined argument")

        if self.function_args_aliases[command_to_bind] in self.arg_prompts:
            raise Exception("Overring arg_prompt")

        self.arg_prompts[command_to_bind] = arg_prompt

    def trigger(self):
        # Do base prompting
        print(f"Executing function({self.function.__name__})")
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

        # Call the function
        try:
            self.function(**args_to_pass)
            print(f"Successfully executed function({self.function.__name__})")
        except Exception as e:
            print(e)
            print(f"An error occcured during execution of function({self.function.__name__})")


