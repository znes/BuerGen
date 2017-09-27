from sys import stdout


def yes_or_no(msg):
    """ Simple yes or no question asks for user input

    Attributes
    ----------
    msg : str
        Question to be asked.

    Returns
    -------
    bool
        True if positive false otherwise.
    """

    valid = {"yes": True, "y": True, "no": False, "n": False}
    prompt = " [y/n] "

    while True:
        stdout.write("QUESTION: " + msg + prompt)
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        else:
            stdout.write("Please respond with 'y' or 'n'.")
