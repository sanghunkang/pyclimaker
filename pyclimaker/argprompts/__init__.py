from .. import utils

import os



class PyCliArgPrompt():
    def __init__(self):
        pass

    def trigger(self):
        # Do base prompting
        print(f"\033[1mPlease enter the argument:\033[0m", end=" ")
        arg = input()
        # if input which triggers binded action is givern

        print(f"Selected argument: {arg}")
        return arg

class PyCliFileSelectionPrompt(PyCliArgPrompt):
    def __init__(self, target_directory):
        self.max_len_filelist = 5
        self.target_directory = target_directory

    def trigger(self):
        filenames = os.listdir(self.target_directory)
        padding = 0
        while True:

            # Display filenames
            if padding != 0:
                print(0, "...See previous filenames")
            for index in range(padding, min(padding+self.max_len_filelist, len(filenames))):
                print(index - padding + 1, filenames[index])
            if padding + self.max_len_filelist <= len(filenames):
                print(self.max_len_filelist+1, "...See following filenames")

            print(f"\033[1mPlease enter index of the filename:\033[0m", end=" ")
            arg = input()
            
            # Check input validity
            if arg.isdigit() == False:
                utils.log_warning("Invalid input. Must an integer between A <= X <= Y")
                continue
            # NOTE elif CANCEL COMMANDS


            # Handle index argument
            if padding != 0 and int(arg) == 0:
                padding -= self.max_len_filelist
            elif padding + self.max_len_filelist <= len(filenames) and int(arg) == self.max_len_filelist+1:
                padding += self.max_len_filelist
            elif 1 <= int(arg) and int(arg) <= self.max_len_filelist:
                arg_index= int(arg) + padding - 1 
                print(f"Selected argument: {filenames[arg_index]}")
                return filenames[arg_index]
            else:
                utils.log_warning("Invalid input. Must an integer between A <= X <= Y")
                
        


