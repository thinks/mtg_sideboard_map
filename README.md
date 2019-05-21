# MtG Sideboard Map
This repository contains a python scripts able to generate a markdown file (such as the one you are reading now) of a decklist and its sideboarding plans from a JSON file. 

## Cloning
```bash
git clone https://github.com/thinks/mtg_sideboard_map.git
```

## Usage
The snippet below shows how to clone the repository and the use the python script to generate a markdown file from one of the sideboard maps in this repository.

```bash
$ git clone https://github.com/thinks/mtg_sideboard_map.git
$ cd mtg_sideboard_map/python
$ python generate_markdown.py -sb ../decks/br_reanimator/sideboard_map.json -md ../decks/br_reanimator/README.md
```
