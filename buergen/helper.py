from sys import stdout

def yes_or_no(msg):
    """
    """

    valid = {"yes": True, "y":True, "no": False, "n":False}
    prompt = " [y/n] "

    while True:
        stdout.write(msg + prompt)
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        else:
            stdout.write("Please respond with 'y' or 'n'.")


