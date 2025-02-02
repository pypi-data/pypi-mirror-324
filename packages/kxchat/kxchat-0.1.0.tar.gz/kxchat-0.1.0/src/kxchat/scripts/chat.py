import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


def start_chat_room(repo: str, revision: str = "main"):
    model = AutoModelForCausalLM.from_pretrained(
        repo,
        revision=revision,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        # attn_implementation="flash_attention_2",
    )
    tokenizer = AutoTokenizer.from_pretrained(repo, revision=revision)
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

    history = []
    while True:
        user_uttr = input("You: ")
        history.append({"role": "user", "content": user_uttr})

        if user_uttr == "exit":
            break
        elif user_uttr == "clear":
            history = []
            continue

        asst_uttr = pipe(
            history,
            max_new_tokens=256,
            return_full_text=False,
            temperature=0.7,
            top_p=0.95,
            top_k=50,
        )[0]["generated_text"]
        history.append({"role": "assistant", "content": asst_uttr})
        print(f"Assistant: {asst_uttr}")
