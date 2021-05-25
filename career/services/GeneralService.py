def get_translation_word(which_lg, keyword):
    with open('example.json', 'r') as myfile:
        data = myfile.read()


def is_integer(param):
    try:
        x = int(param)
        return True
    except:
        return False
