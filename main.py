import sys
import json
import os,glob
import string


def main():
    folder_path = "C:\\toscript"
    #process json files in folder
    for filename in glob.glob(os.path.join(folder_path, '*.json')):
        with open(filename, encoding="utf8") as f:
            data = json.load(f)
            tot_len = len(data['words'])
            for index, entry in enumerate(data['words']): #data contains list of dicts
                val = entry['value']
                if val == "":
                    continue
                case = is_only_punct(val) #process case val is empty punctuation
                if handle_space(data, index, case) or handle_punct(data, index, case, tot_len, val):
                #process cases val is space or punctuation
                    tot_len -= 1
                elif punct_and_word(val):
                #process case val consists of punctuation and word
                    handle_punct_and_word(data, index, val)

        #create new file with updated data
        new_file_name = append_sample(filename)
        json_obj = json.dumps(data, indent = 1, ensure_ascii=False)
        with open(new_file_name, 'w', encoding="utf8") as outfile:
            outfile.write(json_obj)

def append_sample(filename):
    """
    appends the string "sample" to file name
    :param filename
    :return: new filename
    """
    curr = filename.split(".")
    if len(curr) == 2:
        new = curr[0] + " - sample." + curr[1]
    elif len(curr) == 3:
        new = curr[0] + " - sample." + curr[1] + "." + curr[2]
    else:
        new = filename + ".illegal"
    return new

def is_only_punct(str):
    """
    Check which case we are at - one single whitespace or punctuation with space before/after
    :param str: word to check
    :return: "SPACE", "ONLY_PUNCT" according to matched case
    """
    if str == " ":
        return "SPACE"
    str = str.split()
    punct = string.punctuation + " " + "..." + "!?" + "?!"
    for s in str:
        if s not in punct:
            return "FALSE"
    return "ONLY_PUNCT"

def stripped_punct(str):
    """
    Strip input string from spaces
    :param str
    :return: stripped string from spaces
    """
    str = str.split()
    res = ""
    for index, s in enumerate(str):
        if s in string.punctuation:
            res += s
    return res

def handle_space(data, index, case):
    """
    Check if we are at SPACE case and handle accordingly
    :param data: dict with 2 keys - speakers and words.
    :param index: of current entry
    :param case: SPACE
    :return: TRUE if we are at currect case
    """
    # avoid access to illegal memory
    prev = -1 if index == 0 else data['words'][index - 1]['value']
    if case == "SPACE":
        if prev != -1 and prev[-1] != " ":
            data['words'][index - 1]['value'] += " "
        del (data['words'][index])
        return True


def handle_punct(data, index, case, tot_len, val):
    """
    Check if we are at ONLY_PUNCT case and handle accordingly
    :param data: dict with 2 keys - speakers and words.
    :param index: of current entry
    :param case: ONLY_PUNCT
    :param tot_len: len of total entries
    :param val: current entry's word
    :return: TRUE if we are at currect case
    """
    # avoid access to illegal memory
    prev = -1 if index == 0 else data['words'][index - 1]['value']
    next = -1 if index > tot_len - 2 else data['words'][index + 1]['value']
    if case == "ONLY_PUNCT":
        # we are not at start or end
        if prev != -1 and next != -1:
            # previous val's char is space, so we concat it
            if prev[-1] == " ":
                data['words'][index - 1]['value'] = prev[:-1]
            # handle special case where we have open parenthese
            if stripped_punct(val) == "(":
                data['words'][index + 1]['value'] = "(" + data['words'][index + 1]['value']
            else:
                data['words'][index - 1]['value'] += stripped_punct(val)
            # next word doesn't start with SPACE but current last char is space, so add SPACE to next
            if next[0] != " " and val[-1] == " ":
                data['words'][index + 1]['value'] = " " + data['words'][index + 1]['value']
        elif next == -1:
            data['words'][index - 1]['value'] += stripped_punct(val)
        del (data['words'][index])
        return True

def punct_and_word(str):
    """
    Check if we are at punctuation and word case and handle accordingly
    :param str: val to check
    :return: true if first char is space and second char is space
    """
    if str[0] in string.punctuation and str[1] == " ":
        for s in str:
            if s in string.ascii_letters:
                return True
    return False

def handle_punct_and_word(data, index, val):
    prev = -1 if index == 0 else data['words'][index - 1]['value']
    if prev != -1 and next != -1:
        # previous val's char is space, so we concat it
        if prev[-1] == " ":
            data['words'][index - 1]['value'] = prev[:-1]
        punct = val[0]
        curr = val[1:]
        data['words'][index]['value'] = curr
        data['words'][index-1]['value'] += punct


if __name__ == '__main__':
    main()



