#!/usr/bin/env python3
"""Regenerate the palette source files for the 15 alternate color-scheme
forks of this theme (Nord, Dracula, Tokyo Night, Spacegray, Everforest
Light/Dark, Catppuccin Latte/Mocha/Macchiato, Material Light/Dark, Ubuntu
Light/Dark, Solarized Light/Dark).

This is the ONLY durable copy of each fork's exact palette values --
~/.themes/<Name>/gnome-shell/ is compiled OUTPUT, not source, and the
per-theme SASS edits this script re-applies were previously made (and
discarded) in disposable per-theme copies of this themes/ directory.
If a structural change lands in this repo's shared SASS (anything outside
_color-palette-default.scss and the tier block in _colors.scss) and needs
to reach the 15 forks too, this script is what makes that a 15-minute
rebuild instead of a from-scratch reconstruction.

Usage:
    SCRATCH=/some/scratch/dir
    for name in Nord Dracula Tokyo-Night Spacegray Everforest-Dark \\
                Everforest-Light Catppuccin-Latte Catppuccin-Mocha \\
                Catppuccin-Macchiato Material-Light Material-Dark \\
                Ubuntu-Light Ubuntu-Dark Solarized-Light Solarized-Dark; do
        cp -r themes "$SCRATCH/$name"   # this directory, themes/
    done
    python3 themes/generate-palette-forks.py "$SCRATCH"
    # then per theme (VARIANT is light or dark, matching the table below):
    cd "$SCRATCH/<Name>" && bash install.sh -d ~/.themes -n '<Name>' \\
        -c <VARIANT> -N
    # installs to ~/.themes/<Name>-<Light|Dark> -- rename, then replace
    # ~/.themes/<Name>/gnome-shell with the new build's gnome-shell dir
    # (that's the only part of install.sh's output this project uses --
    # GTK4 is hand-written separately per ~/.config/docs/candy.md).

VARIANT by theme (also encoded in each THEMES entry's "variant" key below):
    dark:  Nord, Dracula, Tokyo-Night, Spacegray, Everforest-Dark,
           Catppuccin-Mocha, Catppuccin-Macchiato, Material-Dark,
           Ubuntu-Dark, Solarized-Dark
    light: Everforest-Light, Catppuccin-Latte, Material-Light,
           Ubuntu-Light, Solarized-Light
"""
import os
import sys

SCRATCH = sys.argv[1] if len(sys.argv) > 1 else "./theme-rebuild-scratch"

# Each theme: accents (red,pink,purple,blue,teal,green,yellow,orange) as single
# hex (used for both -light/-dark sides per the dark-only/light-only
# convention established originally), grey ramp (19 stops, light->dark),
# white, black, default (=primary accent), buttons (close,max,min),
# tiers (overview_bg, background, surface, base, base_alt, card, menu,
# osd, scrim, scrim_alt, titlebar, titlebar_backdrop, popover, panel_solid)
THEMES = {
    "Nord": dict(
        variant="dark",
        accents=dict(red="#BF616A", pink="#B48EAD", purple="#B48EAD", blue="#88C0D0",
                     teal="#8FBCBB", green="#A3BE8C", yellow="#EBCB8B", orange="#D08770"),
        white="#ECEFF4", black="#2E3440", default="#88C0D0",
        button_close="#BF616A", button_max="#A3BE8C", button_min="#D08770",
        grey=["#ECEFF4","#E5E9F0","#D8DEE9","#CDD3DE","#C2C8D3","#B7BDC8","#ADB3BE",
              "#9CA3B0","#8892A1","#4C566A","#434C5E","#3B4252","#363D4C","#323847",
              "#2E3440","#2A303C","#262B36","#222731","#1E222B"],
        tiers=dict(overview_bg="#2E3440", background="#2E3440", surface="#3B4252",
                   base="#3B4252", base_alt="#434C5E", card="#3B4252", menu="#3B4252",
                   osd="#2E3440", scrim="#3B4252", scrim_alt="#434C5E", titlebar="#2E3440",
                   titlebar_backdrop="#2E3440", popover="#434C5E", panel_solid="#2E3440"),
    ),
    "Dracula": dict(
        variant="dark",
        accents=dict(red="#FF5555", pink="#FF79C6", purple="#BD93F9", blue="#8BE9FD",
                     teal="#8BE9FD", green="#50FA7B", yellow="#F1FA8C", orange="#FFB86C"),
        white="#F8F8F2", black="#282A36", default="#BD93F9",
        button_close="#FF5555", button_max="#50FA7B", button_min="#FFB86C",
        grey=["#F8F8F2","#E9E9F2","#D6D6E8","#C3C3DD","#B0B0D2","#9D9DC7","#8A8ABC",
              "#7779A8","#6272A4","#565A7D","#4A4D68","#44475A","#3D3F50","#363846",
              "#2F313C","#282A36","#232530","#1E1F29","#191A22"],
        tiers=dict(overview_bg="#282A36", background="#282A36", surface="#343746",
                   base="#343746", base_alt="#44475A", card="#343746", menu="#343746",
                   osd="#282A36", scrim="#343746", scrim_alt="#44475A", titlebar="#282A36",
                   titlebar_backdrop="#282A36", popover="#44475A", panel_solid="#282A36"),
    ),
    "Tokyo-Night": dict(
        variant="dark",
        accents=dict(red="#f7768e", pink="#bb9af7", purple="#bb9af7", blue="#7aa2f7",
                     teal="#73daca", green="#9ece6a", yellow="#e0af68", orange="#ff9e64"),
        white="#c0caf5", black="#1a1b26", default="#7aa2f7",
        button_close="#f7768e", button_max="#9ece6a", button_min="#ff9e64",
        grey=["#c0caf5","#b4bee8","#a9b1d6","#9aa5ca","#8b99be","#7c8cb1","#6e7fa5",
              "#5f7299","#565f89","#414868","#363c56","#292e42","#24283a","#20232f",
              "#1e2030","#1a1b26","#191a22","#16161e","#131318"],
        tiers=dict(overview_bg="#1a1b26", background="#1a1b26", surface="#16161e",
                   base="#16161e", base_alt="#292e42", card="#16161e", menu="#16161e",
                   osd="#1a1b26", scrim="#16161e", scrim_alt="#292e42", titlebar="#16161e",
                   titlebar_backdrop="#1a1b26", popover="#292e42", panel_solid="#1a1b26"),
    ),
    "Spacegray": dict(
        variant="dark",
        accents=dict(red="#ec5f67", pink="#c594c5", purple="#c594c5", blue="#6699cc",
                     teal="#5fb3b3", green="#99c794", yellow="#ffcc66", orange="#ea9560"),
        white="#e0e0e0", black="#222222", default="#5fb3b3",
        button_close="#ec5f67", button_max="#99c794", button_min="#ea9560",
        grey=["#e0e0e0","#cccccc","#b4b7b4","#a3a3a3","#949494","#868686","#787878",
              "#6a6a6a","#5c5c5c","#4d4d4d","#454545","#3d3d3d","#363636","#2e2e2e",
              "#292929","#222222","#1e1e1e","#1a1a1a","#161616"],
        tiers=dict(overview_bg="#222222", background="#222222", surface="#2b2b2b",
                   base="#2b2b2b", base_alt="#383838", card="#2b2b2b", menu="#2b2b2b",
                   osd="#222222", scrim="#2b2b2b", scrim_alt="#383838", titlebar="#222222",
                   titlebar_backdrop="#222222", popover="#383838", panel_solid="#222222"),
    ),
    "Everforest-Dark": dict(
        variant="dark",
        accents=dict(red="#e67e80", pink="#d699b6", purple="#d699b6", blue="#7fbbb3",
                     teal="#83c092", green="#a7c080", yellow="#dbbc7f", orange="#e69875"),
        white="#d3c6aa", black="#2d353b", default="#a7c080",
        button_close="#e67e80", button_max="#a7c080", button_min="#e69875",
        grey=["#d3c6aa","#c5b998","#b7ac89","#a89e7d","#9da9a0","#8f9a91","#818b82",
              "#737c73","#667066","#5f6a5f","#565e58","#475258","#3f494e","#3d484d",
              "#343f44","#2d353b","#282f34","#23292e","#1e2327"],
        tiers=dict(overview_bg="#2d353b", background="#2d353b", surface="#343f44",
                   base="#343f44", base_alt="#3d484d", card="#343f44", menu="#343f44",
                   osd="#2d353b", scrim="#343f44", scrim_alt="#3d484d", titlebar="#2d353b",
                   titlebar_backdrop="#2d353b", popover="#3d484d", panel_solid="#2d353b"),
    ),
    "Everforest-Light": dict(
        variant="light",
        accents=dict(red="#f85552", pink="#df69ba", purple="#df69ba", blue="#3a94c5",
                     teal="#35a77c", green="#8da101", yellow="#dfa000", orange="#f57d26"),
        white="#f8f3e0", black="#2d353b", default="#8da101",
        button_close="#f85552", button_max="#8da101", button_min="#f57d26",
        grey=["#f8f3e0","#f2ecd8","#eee6cf","#e6dcc7","#ddd2bb","#d3c7ad","#c5b998",
              "#b7ac89","#a89e7d","#9da9a0","#8a988e","#78877c","#66766a","#556358",
              "#475258","#3d484d","#343f44","#2d353b","#262d32"],
        tiers=dict(overview_bg="#f2ecd8", background="#f8f3e0", surface="#f2ecd8",
                   base="#f2ecd8", base_alt="#e6dcc7", card="#f2ecd8", menu="#f2ecd8",
                   osd="#f8f3e0", scrim="#f2ecd8", scrim_alt="#e6dcc7", titlebar="#f8f3e0",
                   titlebar_backdrop="#f8f3e0", popover="#e6dcc7", panel_solid="#f8f3e0"),
    ),
    "Catppuccin-Latte": dict(
        variant="light",
        accents=dict(red="#d20f39", pink="#ea76cb", purple="#8839ef", blue="#1e66f5",
                     teal="#179299", green="#40a02b", yellow="#df8e1d", orange="#fe640b"),
        white="#eff1f5", black="#11111b", default="#8839ef",
        button_close="#d20f39", button_max="#40a02b", button_min="#fe640b",
        grey=["#eff1f5","#e6e9ef","#dce0e8","#ccd0da","#bcc0cc","#acb0be","#9ca0b0",
              "#8c8fa1","#7c7f93","#6c6f85","#5c5f77","#4c4f69","#41435a","#363850",
              "#2b2d46","#20223c","#191a2e","#141524","#11111b"],
        tiers=dict(overview_bg="#e6e9ef", background="#eff1f5", surface="#e6e9ef",
                   base="#e6e9ef", base_alt="#dce0e8", card="#e6e9ef", menu="#e6e9ef",
                   osd="#eff1f5", scrim="#e6e9ef", scrim_alt="#dce0e8", titlebar="#eff1f5",
                   titlebar_backdrop="#eff1f5", popover="#dce0e8", panel_solid="#eff1f5"),
    ),
    "Catppuccin-Mocha": dict(
        variant="dark",
        accents=dict(red="#f38ba8", pink="#f5c2e7", purple="#cba6f7", blue="#89b4fa",
                     teal="#94e2d5", green="#a6e3a1", yellow="#f9e2af", orange="#fab387"),
        white="#eff1f5", black="#11111b", default="#cba6f7",
        button_close="#f38ba8", button_max="#a6e3a1", button_min="#fab387",
        grey=["#cdd6f4","#bac2de","#a6adc8","#9399b2","#7f849c","#6c7086","#626880",
              "#585b70","#4d5066","#45475a","#3a3c4e","#313244","#2a2b3c","#24253a",
              "#1e1e2e","#1a1a26","#181825","#15151f","#11111b"],
        tiers=dict(overview_bg="#181825", background="#1e1e2e", surface="#181825",
                   base="#181825", base_alt="#313244", card="#181825", menu="#181825",
                   osd="#11111b", scrim="#181825", scrim_alt="#313244", titlebar="#1e1e2e",
                   titlebar_backdrop="#1e1e2e", popover="#313244", panel_solid="#1e1e2e"),
    ),
    "Catppuccin-Macchiato": dict(
        variant="dark",
        accents=dict(red="#ed8796", pink="#f5bde6", purple="#c6a0f6", blue="#8aadf4",
                     teal="#8bd5ca", green="#a6da95", yellow="#eed49f", orange="#f5a97f"),
        white="#eff1f5", black="#181926", default="#c6a0f6",
        button_close="#ed8796", button_max="#a6da95", button_min="#f5a97f",
        grey=["#cad3f5","#b8c0e0","#a5adcb","#939ab7","#8087a2","#6e738d","#646980",
              "#5b6078","#51556a","#494d64","#3e415a","#363a4f","#2f3244","#292c3d",
              "#24273a","#20222f","#1e2030","#1a1b28","#181926"],
        tiers=dict(overview_bg="#1e2030", background="#24273a", surface="#1e2030",
                   base="#1e2030", base_alt="#363a4f", card="#1e2030", menu="#1e2030",
                   osd="#181926", scrim="#1e2030", scrim_alt="#363a4f", titlebar="#24273a",
                   titlebar_backdrop="#24273a", popover="#363a4f", panel_solid="#24273a"),
    ),
    "Material-Light": dict(
        variant="light",
        accents=dict(red="#B3261E", pink="#7D5260", purple="#6750A4", blue="#4C5C92",
                     teal="#4A6363", green="#43A047", yellow="#F9A825", orange="#E8710A"),
        white="#FFFBFE", black="#1C1B1F", default="#6750A4",
        button_close="#B3261E", button_max="#43A047", button_min="#E8710A",
        grey=["#FFFBFE","#F4EFF4","#E7E0EC","#DDD8DD","#D0CBD1","#C3BEC4","#B6B1B8",
              "#A9A4AB","#938F99","#7E7A83","#6A666F","#625B71","#544F5A","#464248",
              "#38353A","#2B282D","#211E24","#1C1B1F","#17161A"],
        tiers=dict(overview_bg="#E7E0EC", background="#FFFBFE", surface="#FFFBFE",
                   base="#E7E0EC", base_alt="#DDD8DD", card="#FFFBFE", menu="#E7E0EC",
                   osd="#FFFBFE", scrim="#E7E0EC", scrim_alt="#DDD8DD", titlebar="#FFFBFE",
                   titlebar_backdrop="#FFFBFE", popover="#E7E0EC", panel_solid="#FFFBFE"),
    ),
    "Material-Dark": dict(
        variant="dark",
        accents=dict(red="#F2B8B5", pink="#EFB8C8", purple="#D0BCFF", blue="#B0C6FF",
                     teal="#A8CFCA", green="#A6D6A6", yellow="#F5CB5C", orange="#FFB77C"),
        white="#FFFBFE", black="#1C1B1F", default="#D0BCFF",
        button_close="#F2B8B5", button_max="#A6D6A6", button_min="#FFB77C",
        grey=["#E6E1E5","#D9D4D9","#CCC7CC","#BFBABF","#B2ADB2","#A5A0A5","#989399",
              "#8B868C","#938F99","#79757F","#6D6977","#49454F","#403C46","#37333D",
              "#2E2B33","#262329","#211E24","#1C1B1F","#17161A"],
        tiers=dict(overview_bg="#49454F", background="#1C1B1F", surface="#1C1B1F",
                   base="#49454F", base_alt="#544F5A", card="#1C1B1F", menu="#49454F",
                   osd="#1C1B1F", scrim="#49454F", scrim_alt="#544F5A", titlebar="#1C1B1F",
                   titlebar_backdrop="#1C1B1F", popover="#49454F", panel_solid="#1C1B1F"),
    ),
    "Ubuntu-Light": dict(
        variant="light",
        accents=dict(red="#E01B24", pink="#C24D8B", purple="#77216F", blue="#1C71D8",
                     teal="#1AA0A0", green="#0E8420", yellow="#E5A50A", orange="#E95420"),
        white="#FFFFFF", black="#262626", default="#E95420",
        button_close="#E01B24", button_max="#0E8420", button_min="#E95420",
        grey=["#ffffff","#fafafa","#f3f3f3","#ebebeb","#e0e0e0","#d4d4d4","#c7c7c7",
              "#b8b8b8","#a8a8a8","#949494","#7e7e7e","#676767","#525252","#404040",
              "#363636","#303030","#2c2c2c","#262626","#1e1e1e"],
        tiers=dict(overview_bg="#f3f3f3", background="#fafafa", surface="#ffffff",
                   base="#f3f3f3", base_alt="#ebebeb", card="#ffffff", menu="#f3f3f3",
                   osd="#fafafa", scrim="#f3f3f3", scrim_alt="#ebebeb", titlebar="#ebebeb",
                   titlebar_backdrop="#fafafa", popover="#ffffff", panel_solid="#ebebeb"),
    ),
    "Ubuntu-Dark": dict(
        variant="dark",
        accents=dict(red="#E01B24", pink="#C24D8B", purple="#77216F", blue="#1C71D8",
                     teal="#1AA0A0", green="#0E8420", yellow="#E5A50A", orange="#E95420"),
        white="#fafafa", black="#262626", default="#E95420",
        button_close="#E01B24", button_max="#0E8420", button_min="#E95420",
        grey=["#e6e6e6","#d9d9d9","#cccccc","#bfbfbf","#b2b2b2","#a3a3a3","#949494",
              "#858585","#737373","#616161","#525252","#454545","#3a3a3a","#383838",
              "#333333","#303030","#2c2c2c","#262626","#1e1e1e"],
        tiers=dict(overview_bg="#303030", background="#262626", surface="#303030",
                   base="#303030", base_alt="#383838", card="#303030", menu="#303030",
                   osd="#262626", scrim="#303030", scrim_alt="#383838", titlebar="#383838",
                   titlebar_backdrop="#262626", popover="#303030", panel_solid="#383838"),
    ),
    "Solarized-Light": dict(
        variant="light",
        accents=dict(red="#dc322f", pink="#d33682", purple="#6c71c4", blue="#268bd2",
                     teal="#2aa198", green="#859900", yellow="#b58900", orange="#cb4b16"),
        white="#fdf6e3", black="#002b36", default="#268bd2",
        button_close="#dc322f", button_max="#859900", button_min="#cb4b16",
        grey=["#fdf6e3","#f6efd9","#eee8d5","#e4ddc8","#d5cdb5","#c2b89f","#aca189",
              "#93a1a1","#839496","#73898b","#657b83","#586e75","#4a5c63","#3b4a50",
              "#2c3a40","#073642","#05303b","#032a35","#002b36"],
        tiers=dict(overview_bg="#eee8d5", background="#fdf6e3", surface="#eee8d5",
                   base="#eee8d5", base_alt="#e4dcc5", card="#eee8d5", menu="#eee8d5",
                   osd="#fdf6e3", scrim="#eee8d5", scrim_alt="#e4dcc5", titlebar="#fdf6e3",
                   titlebar_backdrop="#fdf6e3", popover="#eee8d5", panel_solid="#fdf6e3"),
    ),
    "Solarized-Dark": dict(
        variant="dark",
        accents=dict(red="#dc322f", pink="#d33682", purple="#6c71c4", blue="#268bd2",
                     teal="#2aa198", green="#859900", yellow="#b58900", orange="#cb4b16"),
        white="#fdf6e3", black="#002b36", default="#268bd2",
        button_close="#dc322f", button_max="#859900", button_min="#cb4b16",
        grey=["#93a1a1","#8b9a9a","#839496","#778a8c","#6c8183","#657b83","#5d7178",
              "#586e75","#4f636a","#47585f","#3e4d53","#354247","#2c373c","#223034",
              "#182a2f","#0e3038","#073642","#042e38","#002b36"],
        tiers=dict(overview_bg="#073642", background="#002b36", surface="#073642",
                   base="#073642", base_alt="#0a4552", card="#073642", menu="#073642",
                   osd="#002b36", scrim="#073642", scrim_alt="#0a4552", titlebar="#002b36",
                   titlebar_backdrop="#002b36", popover="#073642", panel_solid="#002b36"),
    ),
}

def write_palette(name, t):
    path = f"{SCRATCH}/{name}/src/sass/_color-palette-default.scss"
    a = t["accents"]
    grey_labels = ["050","100","150","200","250","300","350","400","450","500",
                   "550","600","650","700","750","800","850","900","950"]
    grey_lines = "\n".join(f"$grey-{lbl}: {hexv};" for lbl, hexv in zip(grey_labels, t["grey"]))
    content = f"""// {name} palette (recolor of Gruvbox Material Default Theme Color Palette)

// Red
$red-light: {a['red']};
$red-dark: {a['red']};

// Pink
$pink-light: {a['pink']};
$pink-dark: {a['pink']};

// Purple
$purple-light: {a['purple']};
$purple-dark: {a['purple']};

// Blue
$blue-light: {a['blue']};
$blue-dark: {a['blue']};

// Teal
$teal-light: {a['teal']};
$teal-dark: {a['teal']};

// Green
$green-light: {a['green']};
$green-dark: {a['green']};

// Yellow
$yellow-light: {a['yellow']};
$yellow-dark: {a['yellow']};

// Orange
$orange-light: {a['orange']};
$orange-dark: {a['orange']};

// Grey
{grey_lines}

// White
$white: {t['white']};

// Black
$black: {t['black']};

// Theme
$default-light: {t['default']};
$default-dark: {t['default']};

// Button
$button-close: {t['button_close']};
$button-max: {t['button_max']};
$button-min: {t['button_min']};
"""
    with open(path, "w") as f:
        f.write(content)

def patch_colors(name, t):
    path = f"{SCRATCH}/{name}/src/sass/_colors.scss"
    with open(path) as f:
        lines = f.readlines()
    tiers = t["tiers"]
    replacements = {
        "$overview-bg:": f"$overview-bg:                           if($variant == 'light', {tiers['overview_bg']}, {tiers['overview_bg']});\n",
        "$background:": f"$background:                            if($variant == 'light', {tiers['background']}, {tiers['background']});\n",
        "$surface:": f"$surface:                               if($variant == 'light', {tiers['surface']}, {tiers['surface']});\n",
        "$base:": f"$base:                                  if($variant == 'light', {tiers['base']}, {tiers['base']});\n",
        "$base-alt:": f"$base-alt:                              if($variant == 'light', {tiers['base_alt']}, {tiers['base_alt']});\n",
        "$card:": f"$card:                                  if($variant == 'light', {tiers['card']}, {tiers['card']});\n",
        "$menu:": f"$menu:                                  if($variant == 'light', {tiers['menu']}, {tiers['menu']});\n",
        "$osd:": f"$osd:                                   if($variant == 'light', {tiers['osd']}, {tiers['osd']});\n",
        "$scrim:": f"$scrim:                                 if($variant == 'light', {tiers['scrim']}, {tiers['scrim']});\n",
        "$scrim-alt:": f"$scrim-alt:                             if($variant == 'light', {tiers['scrim_alt']}, {tiers['scrim_alt']});\n",
        "$titlebar:": f"$titlebar:                              if($variant == 'light', {tiers['titlebar']}, {tiers['titlebar']});\n",
        "$titlebar-backdrop:": f"$titlebar-backdrop:                     if($variant == 'light', {tiers['titlebar_backdrop']}, {tiers['titlebar_backdrop']});\n",
        "$popover:": f"$popover:                               if($variant == 'light', {tiers['popover']}, {tiers['popover']});\n",
    }
    tooltip_done = False
    panel_done = False
    out = []
    for line in lines:
        stripped = line.strip()
        matched = False
        for key, newline in replacements.items():
            if stripped.startswith(key):
                out.append(newline)
                matched = True
                break
        if matched:
            continue
        if stripped.startswith("$tooltip:") and not tooltip_done:
            out.append(f"$tooltip:                               if($variant == 'dark', rgba(darken({tiers['background']}, 3%), 0.9), rgba(darken({tiers['background']}, 3%), 0.9));\n")
            tooltip_done = True
            continue
        if stripped.startswith("$panel-solid:") and not panel_done:
            out.append(f"$panel-solid:                           if($topbar  == 'dark', \t{tiers['panel_solid']}, {tiers['panel_solid']}); // for Unity panel which doesn't allow translucent colors\n")
            panel_done = True
            continue
        out.append(line)
    with open(path, "w") as f:
        f.writelines(out)

for name, t in THEMES.items():
    write_palette(name, t)
    patch_colors(name, t)
    print(f"wrote {name}")
