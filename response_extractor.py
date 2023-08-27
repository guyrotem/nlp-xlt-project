def extract_result(text):
    lines = text.split('\n')
    last_line = lines[len(lines) - 1]
    return last_line.replace('Answer: ', '')
