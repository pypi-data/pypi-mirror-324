# kxchat

`kxchat` is a conversational AI application that leverages state-of-the-art natural language processing models to facilitate interactive chat experiences. It allows users to load models from specified repositories and engage in dynamic conversations.

## Table of Contents

- [kxchat](#kxchat)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
  - [Features](#features)
  - [Development](#development)

## Installation

kxchat requires Python 3.11 or higher.

Use `pip`/`uv`

```bash
pip install kxchat
```

```bash
uv add kxchat
```

## Quick Start

To start a chat room using a model from a specific repository, run the following command:

```bash
kxchat room <repo> [--revision <revision>]
```

- `<repo>`: The URL or path to the repository containing the model.
- `--revision <revision>`: The specific revision of the model to use (default is "main").

Example:

```bash
kxchat room meta-llama/Meta-Llama-3.1-8B-Instruct
```


## Features

- **Dynamic Model Loading:** Load models from any specified repository and revision.
- **Interactive Chat:** Engage in real-time conversations with the AI.
- **Command Line Interface:** Simple and intuitive CLI for easy interaction.

## Development

To set up a development environment, install the development dependencies:

```bash
uv sync --dev
```
