# Magic the Gathering (MtG) Sideboard Map
This repository contains a [python script](https://github.com/thinks/mtg_sideboard_map/blob/master/python/generate_tex.py) for generating `.tex` and `.pdf` files from a decklist and its sideboard guide provided in `.json` format. The goals are to generate an easily printable document for players and to enable content creators to be able to deliver fine-tuned decklists rather than spending large amounts of time on formatting. A brief example demonstrating how it works is given below, followed by a description of the input format.

All code in this repository is released under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).

## Example
The script uses `.tex` as an intermediary representation before finalizing the results to `.pdf`. The snippet below shows how to generate a `.tex` file for an [example deck](https://github.com/thinks/mtg_sideboard_map/blob/master/example/example_sb_map.json) using the script. Ready-made results can be found in the [example folder](https://github.com/thinks/mtg_sideboard_map/tree/master/example).
```bash
$ git clone https://github.com/thinks/mtg_sideboard_map.git
$ cd mtg_sideboard_map/python
$ python generate_tex.py -sb ../example/example_sb_map.json -tex ../example/example.tex
```
Using a third-party application, such as `pdflatex.exe`, the file `example.tex` (preview [here](https://github.com/thinks/mtg_sideboard_map/blob/master/example/example.tex)) can be converted to a `.pdf` file. Having access to this intermediary format allows users to fine-tune the `.tex` file before the final step of creating the `.pdf` file. Also, in some cases it might be easier to use an online resource, such as [https://www.overleaf.com](https://www.overleaf.com), rather than installing `pdflatex.exe` on the local machine. 

However, in the case where `pdflatex.exe` is available on the local machine the script can be instructed to use it to directly generate a `.pdf` file, as shown below.
```bash
$ git clone https://github.com/thinks/mtg_sideboard_map.git
$ cd mtg_sideboard_map/python
$ python generate_tex.py -sb ../example/example_sb_map.json -tex ../example/example.tex -pdflatex "C:/Users/tommy/AppData/Local/Programs/MiKTeX 2.9/miktex/bin/x64/pdflatex.exe" -pdf_dir ../example
```
This will generate a file called `example.pdf` (preview [here](https://github.com/thinks/mtg_sideboard_map/blob/master/example/example.pdf)) in the example folder. 

## Input
Here is a brief description of the simple `.json` format use to pass the decklist and sideboard guide to the script. Note that the comments have been added for clarity here and should be omitted when creating an actual `.json` file. An example of a complete input file can be found [here](https://github.com/thinks/mtg_sideboard_map/blob/master/example/example_sb_map.json).

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
  // Optional shorter names for cards (more suitable for two-column formatting).
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
