from pyclimaker import PyCliMain, PyCliFunctionPrompt
from pyclimaker.argprompts import PyCliArgPrompt, PyCliFileSelectionPrompt

def foo(x):
    print(f"A boring function which simply prints out input, which is: {x}")

def bar(x, following_message="the following message"):
    print(f"This function prints the input: {x} with {following_message}")

def spam(filepath):
    with open(filepath, "r", encoding="utf8") as f:
        print(f.read())

def fwmua(x1, x2):
    """function_with_multiple_unpredefined_arguments"""
    print(f"x1 is selected as {x1}, and x2 is selected as {x2}")

command_foo = PyCliFunctionPrompt(function=foo, description="This is the foo function")
command_foo.bind_default_cli_arg(arg_alias="x", arg_value="THE INPUT", is_predefined=True)

command_bar = PyCliFunctionPrompt(function=bar, description="This is the bar function")
command_bar.bind_default_cli_arg(arg_alias="x", arg_value="THE INPUT", is_predefined=True)
# command_bar.bind_default_cli_arg(arg_alias="following_message", arg_value="shorter fm", is_predefined=True)
command_bar.bind_arg_prompt(PyCliArgPrompt(), "following_message")

command_spam = PyCliFunctionPrompt(function=spam, description="This is the spam function")
command_spam.bind_arg_prompt(PyCliFileSelectionPrompt(target_directory="./"), "filepath")

command_fwmua = PyCliFunctionPrompt(function=fwmua, description="This is the function_with_multiple_unpredefined_arguments")
command_fwmua.bind_arg_prompt(PyCliArgPrompt(), "x1")
command_fwmua.bind_arg_prompt(PyCliArgPrompt(), "x2")

main = PyCliMain()
main.bind_function(command_foo, "foo")
main.bind_function(command_bar, "bar")
main.bind_function(command_spam, "spam")
main.bind_function(command_fwmua, "fwmua")
main.run()