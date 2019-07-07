# Magic the Gathering (MtG) Sideboard Map
This repository contains a python script able to generate `.tex` and `.pdf` files from a decklist and its sideboard guide in `.json` format. The goals are to generate an easily printable document for players and to enable content creators to be able to deliver fine-tuned decklists rather than spending large amounts of time on formatting. A brief example demonstrating how it works is given below.

All code in this repository is released under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).

## Example
The snippet below shows how to clone the repository and the use the included python script to generate a sideboarding document in `.pdf` format for an example deck included in this repository.

```bash
$ git clone https://github.com/thinks/mtg_sideboard_map.git
$ cd mtg_sideboard_map/python
$ python generate_tex.py -sb ../example/example_sb_map.json -tex ../example/example.tex -pdflatex "C:/Users/tommy/AppData/Local/Programs/MiKTeX 2.9/miktex/bin/x64/pdflatex.exe" -pdf_dir ../example
```

This will generate a file called `example.pdf` in the example folder. There are two ways to generate the `.pdf` file. The simplest is to install `pdflatex.exe` somewhere on your local machine and give the path to the script, as shown above. The script will then use that executable to generate a `.pdf` directly. If for some reason `pdflatex.exe` is not present (signalled by omitting the `-pdflatex` and `-pdf_dir` flags), the contents of the `.tex` file (`example.tex` in this case) can be pasted into an online LaTeX resource, such as [https://www.overleaf.com](https://www.overleaf.com), and the `.pdf` can be downloaded from there.

## Input
Here is a brief description of the simple `.json` format use to pass the decklist and sideboard guide to the script. An example of a complete input file can be found [here](https://github.com/thinks/mtg_sideboard_map/blob/master/example/example_sb_map.json).

```cpp
{
  "title": "My Cool Deckname",
  "author": "Tommy Hinks",
  "date": "May 4, 2018",
  "decklist": {
    // Listing of cards in the maindeck on the format "name" : quantity
    "maindeck": {
      "Entomb": 4,
      "Faithless Looting": 4,
      "Animate Dead": 4,
      "Exhume": 4,
      ...
    },
    // Listing of cards in the sideboard on the format "name" : quantity
    "sideboard": {
      "Archetype of Endurance": 1,
      "Elesh Norn, Grand Cenobite": 1,    
      "Iona, Shield of Emeria": 1,
      ...
    }
  },
  // Optional shorter names for cards more suitable for two-column formatting.
  "screen_names": {
    "Archetype of Endurance": "Archetype",
    "Elesh Norn, Grand Cenobite": "Elesh Norn",
    ...
  },   
  // List of matchups for which sideboarding advice is given.
  "matchups": {
    // Sideboard configurations for a particular matchup.
    "Delver": {
      "notes": "Important things to remember in the matchup.",
      // If sideboarding is the same regardless of whether we are on the play/draw use the 'play_and_draw' key.
      "play_and_draw": {
        // Cards to bring in.
        "in": {
          "Thoughtseize": 2,
          "Wear/Tear": 1,
          ...
        },
        // Cards to take out.
        "out": {
          "Chancellor of the Annex": 3,
          ...
        }
      }
    },
    "Burn": {
      "notes": "Don't get bolted!",
      // Sideboarding on the play.
      "play": {
        "in": {
          "Reverent Silence": 3,
          "Serenity": 2,
          ...
        },
        "out": {
          "Cabal Therapy": 4,
          "Ashen Rider": 1,
          ...
        }
      },
      // Sideboarding on the draw.
      "draw": {
        "in": {
          "Serenity": 2,
          "Wear/Tear": 1,
          ...
        },
        "out": {
          "Dark Ritual": 3,
          ...
        }
      }
    }, 
    ...
}
```