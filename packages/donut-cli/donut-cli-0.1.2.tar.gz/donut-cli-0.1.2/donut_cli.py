import argparse
import torch, re
from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import os
import logging
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")


# Suppress Hugging Face warnings
logging.getLogger("transformers").setLevel(logging.ERROR)

# Suppress PyTorch warnings
logging.getLogger("torch").setLevel(logging.ERROR)

# Optionally suppress Hugging Face tokenizers warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"


# Load model and processor
MODEL_NAME = "bbadraa99/donut"
device = "cuda" if torch.cuda.is_available() else "cpu"
            
processor = DonutProcessor.from_pretrained(MODEL_NAME, use_fast=True)
model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME).to(device)

def process_image(image_path):
    # Load and preprocess image
    image = Image.open(image_path).convert("RGB")
    pixel_values = processor(image, return_tensors="pt").pixel_values.to(device)

    # prepare decoder inputs
    task_prompt = "<s_donut>"
    decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids
    decoder_input_ids = decoder_input_ids.to(device)
    
    # autoregressively generate sequence
    outputs = model.generate(
        pixel_values,
        decoder_input_ids=decoder_input_ids,
        max_length=model.config.decoder.max_length,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        num_beams=2,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
    )

    # turn into JSON
    seq = processor.batch_decode(outputs.sequences)[0]
    seq = seq.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
    seq = re.sub(r"<.*?>", "", seq, count=1).strip()  # remove first task start token
    seq = processor.token2json(seq)

    return seq["class"]

def main():
    parser = argparse.ArgumentParser(description="DONUT Model CLI for Document Understanding")
    parser.add_argument("image", type=str, help="Path to the input document image")

    args = parser.parse_args()
    result = process_image(args.image)
    
    print("\nDocument type: ", result)

if __name__ == "__main__":
    main()
