from pyclimaker import PyCliFunctionPrompt

def foo(x, following_message="the following message"):
    print(f"This function prints the input:{x} with {following_message}")




command_foo = PyCliFunctionPrompt(
    function= foo,
    description="This is the foo function"
)
# command_foo.add_arg_prompt(prompt_arg_foo)


# prompt_arg_foo = PyCLIArgPrompt(
#     message=
# )