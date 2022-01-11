# Liga

**Add ligatures to any programming font!**

This script copies the ligatures (glyphs and rendering information) from [FiraCode](https://github.com/tonsky/FiraCode) into any other TrueType or OpenType font.

This repo contains a [Fontforge python script](ligate.py) that you can use to add the FiraCode ligatures to any font, as well as submodules for some popular programming fonts and [another script](build.sh) for ligating all of them at once.

Pre-ligated versions are available under [releases](https://github.com/EzequielRamis/liga/releases).

## Requirements

**Using the Fonts**: See the [FiraCode README](https://github.com/tonsky/FiraCode) for a list of supported editors.

**Script**: This script requires FontForge python bindings. For Debian/Ubuntu they are available in `python-fontforge` package. For Arch, OpenSUSE and NixOS, they are included in the `fontforge` package. For macOS, they are available via brew (`brew install fontforge`).

It also requires a python library called `glyphsLib`.

## Using the Script

### Automatic

Use automatic mode to easily convert a font family.

1. Generate a script and configuration template with:

   ```
   $ scripts/generate_build.sh "FONT_FAMILY_NAME"
   ```

   For example:

   ```
   $ scripts/generate_build.sh "Space Mono"
   ```

2. Put the family font(s) into `input/FONT_FAMILY_NAME`
3. Go to `fonts/FONT_FAMILY_NAME`
4. Edit `config.py` to disable ligatures you don't want, change glyphs scale factor, and/or enable any (non-ligature) characters you want from FiraCode in addition to the ligatures.
5. Edit `build.sh` to edit the output family font name, the output directory, the ligatures' weight and many more settings.
6. Return to the git root directory
7. Run
   ```
   $ fonts/FONT_FAMILY_NAME/build.sh
   ```
   The ligated fonts will be located in the `output` directory.

### Manual

1.  Move/copy the font you want to ligate into `input` (or somewhere else convenient).
2.  Edit `config_sample.py` to disable any ligatures you don't want, etc.
3.  Run the script:

    ```
    $ python ligate.py path/to/input/font.ttf
        --output-dir=path/to/output/dir/ \
        --output-name='Name of Ligated Font'
    ```

    For exmaple:

    ```
    $ python ligate.py input/Hack/Hack-Regular.ttf
        --output-dir='output/Ligated Hack' \
        --output-name='Liga Hack'
    ```

    Which will produce `output/Ligated Hack/LigaHack-Regular.ttf`.

The font weight will be inherited from the original file; the font name will be replaced with whatever you specified in `--output-name`. You can also use `--prefix` instead, in which case the original name will be preserved and whatever you put in `--prefix` will be prepended to it.

`ligate.py` supports some additional command line options to, for example, change which font ligatures are copied from or enable copying of individual character glyphs; run `python ligate.py --help` to list them.

## Credit

This repo is a redesign of the [ToxicFrog/Ligaturizer](https://github.com/ToxicFrog/Ligaturizer) implementation because, principally, it does not work with the Firacode's ligatures above v3.1, missing incredible features like infinite arrow combinations.

## Contributions

Contributions always welcome! Please submit a Pull Request, or create an Issue if you have an idea for a feature/enhancement (or bug).
