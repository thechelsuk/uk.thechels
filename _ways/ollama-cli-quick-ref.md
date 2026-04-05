---
layout: post
title: How to use Ollama from the terminal
seo: Ways - How to use Ollama from the terminal
tag: ways
permalink: /ways/ollama-cli-quick-ref
date: 2026-04-01

---

Just for testing LLMs locally to see what the fuss is about, here is a short cheat sheet on using Ollama in the terminal. For this example I've used the Qwen 3.5 4B model, but it can be replaced with any model one has installed.

For more details, see the [Ollama documentation](https://ollama.com/docs/cli).

## Basics

- List installed models
  - `ollama list`
- Show model info
  - `ollama show qwen3.5-4b`
- Pull a model
  - `ollama pull qwen3.5-4b`
- Remove a model
  - `ollama rm qwen3.5-4b`
- List running models / server status
  - `ollama ps`

## Chat & generate

- Simple one‑off prompt
  - `ollama run qwen3.5-4b "Explain this Python error"`
- Interactive chat session
  - `ollama run qwen3.5-4b`
    - Type messages, press Enter
    - `Ctrl+C` to stop generation or exit
- Pass a system / role prompt
  - `ollama run qwen3.5-4b -s "You are a coding assistant."`

## Using files

- Prompt from a file
  - `ollama run qwen3.5-4b --file prompt.txt`
- Pipe input
  - `cat code.py | ollama run qwen3.5-4b`

## Server & API

- Start the Ollama server manually
  - `ollama serve`
- Chat via HTTP API
  - `curl http://localhost:11434/api/chat -d '{ "model": "qwen3.5-4b", "messages": [{"role": "user", "content": "Hello"}] }'`

## Managing models

- Create a model from a Modelfile
  - `ollama create my-model -f Modelfile`
- Copy / tag a model
  - `ollama cp qwen3.5-4b my-qwen-dev`
- Upgrade a model to latest
  - `ollama pull qwen3.5-4b` (re-pulls & updates)

## Useful flags

- Set temperature
  - `ollama run qwen3.5-4b -t 0.2`
- Set max tokens
  - `ollama run qwen3.5-4b -m 512`
- JSON output (useful for tools)
  - `ollama run qwen3.5-4b --format json "Explain this code"`
