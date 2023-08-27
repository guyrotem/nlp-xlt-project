import dataclasses
import json
import codecs


def dump(qa, result):
    with codecs.open("output/{}.json".format(qa.index), "w", "utf-16") as outfile:
        qa_dict = dataclasses.asdict(qa)
        result_dict = dataclasses.asdict(result)
        combined_dict = {
            "qa": qa_dict,
            "result": result_dict,
        }
        content = json.dumps(combined_dict, indent=2, ensure_ascii=False)
        outfile.write(content)
