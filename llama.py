import click, torch, logging, os

os.environ['TRANSFORMERS_CACHE'] = '/home/joberant/NLP_2223/guyrotem1/.cache'
from transformers import AutoTokenizer, AutoModelForCausalLM
from load_file import load_csv


def init_logger():
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s | %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


@click.command()
@click.option("--force-cpu", type=bool, default=False)
def main(force_cpu: bool):
    init_logger()
    logging.info(f"cuda available: {torch.cuda.is_available()}")

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    # if force_cpu:
    device = "cpu"

    if device == "cpu":
        logging.warning("Running on CPU!! Operations may be slow")

    # MODEL_NAME = "lmsys/vicuna-7b-v1.3"
    # MODEL_NAME = "LearnItAnyway/llama-7b-hf-28q_4bit-128g_WVU"
    # MODEL_NAME = "daryl149/llama-2-7b-chat-hf"
    MODEL_NAME = "bigscience/bloom-7b1"

    logging.info("Loading tokenizer & model..")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    logging.info(f"Moving model to {device}..")
    model = model.to(device)

    en = load_csv('data/mgsm_en.csv')

    with torch.no_grad():
        for idx, prompt in enumerate(en):
            MAX_LENGTH = 100
            # print("PROCESSING {} {}".format(idx, prompt))

            inputs = tokenizer(prompt, return_tensors="pt")
            generate_ids = model.generate(
                inputs.input_ids.to(device), max_length=MAX_LENGTH
            )
            decoding = tokenizer.batch_decode(
                generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )

            print("{},{}".format(idx, decoding[0]))


if __name__ == "__main__":
    main()
