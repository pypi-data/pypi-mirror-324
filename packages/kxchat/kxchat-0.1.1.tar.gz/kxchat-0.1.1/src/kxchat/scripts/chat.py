import click
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


def start_chat(
    repo: str,
    revision: str = "main",
    temperature: float = 0.7,
    top_p: float = 0.95,
    top_k: int = 50,
    **kwargs,
):
    click.echo("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        repo,
        revision=revision,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        # attn_implementation="flash_attention_2",
    )
    tokenizer = AutoTokenizer.from_pretrained(repo, revision=revision)
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

    def _show_manual():
        click.echo(click.style(f"{'=' * 38} START CHAT {'=' * 38}"))
        click.echo(
            click.style(
                "Commands:                                                                               ",
                bg="white",
            )
        )
        click.echo(
            click.style(
                "  clear: clear the chat history                                                         ",
                bg="white",
            )
        )
        click.echo(
            click.style(
                "  exit: exit the chat                                                                   ",
                bg="white",
            )
        )

    _show_manual()

    history = []
    while True:
        print("-" * 88)
        user_uttr = input("You: ")
        history.append({"role": "user", "content": user_uttr})

        if user_uttr == "exit":
            break
        elif user_uttr == "clear":
            _show_manual()
            history = []
            continue

        asst_uttr = pipe(
            history,
            max_new_tokens=256,
            return_full_text=False,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            **kwargs,
        )[0]["generated_text"]
        history.append({"role": "assistant", "content": asst_uttr})
        print("-" * 88)
        click.echo(click.style(f"Assistant: {asst_uttr}", fg="blue"))
