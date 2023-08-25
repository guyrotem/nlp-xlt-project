import dataclasses
import json


def dump(qa, result):
    with open("output/{}.json".format(qa.index), "w") as outfile:
        qa_dict = dataclasses.asdict(qa)
        result_dict = dataclasses.asdict(result)
        combined_dict = {
            "qa": qa_dict,
            "result": result_dict,
        }
        content = json.dumps(combined_dict)
        outfile.write(content)
