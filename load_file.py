def load_csv(file_name):
    with open(file_name) as csv:
        content = csv.read()
        rows = content.split("\n")
        ret = []
        for row in rows[1:]:
            first_comma = row.find(',')
            last_comma = len(row) - row[::-1].find(',')
            sentence = row[first_comma+1:last_comma - 1]
            ret.append(sentence.replace('"', ''))

    return ret
