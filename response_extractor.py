def extract_result(text):
    lines = text.split('\n')
    last_line = lines[len(lines) - 1]
    split = last_line.split('#### ')
    if len(split) > 1:
        return split[1]
    else:
        return last_line
