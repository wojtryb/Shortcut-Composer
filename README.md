# Shortcut composer **v1.2.2**


[![python](https://img.shields.io/badge/Python-3.8-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-autopep8-333333.svg)](https://pypi.org/project/autopep8/)
[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![wojtryb website](https://img.shields.io/badge/YouTube-wojtryb-ee0000.svg?style=flat&logo=youtube)](https://youtube.com/wojtryb)
[![wojtryb twitter](https://img.shields.io/badge/Twitter-wojtryb-00aced.svg?style=flat&logo=twitter)](https://twitter.com/wojtryb)
[![wojtryb portfolio](https://img.shields.io/badge/Art_Portfolio-wojtryb-000000.svg?style=flat&logo=)](https://cara.app/wojtryb)

---

**`Extension`** for painting application [**`Krita`**](https://krita.org/), which allows to create custom, complex **`keyboard shortcuts`**.

The plugin adds new shortcuts of the following types:
- [**`Pie menu`**](https://github.com/wojtryb/Shortcut-Composer/wiki/Plugin-actions#pie-menus) - while key is pressed, displays a pie menu, which allows to pick values by hovering a mouse.
- [**`Cursor tracker`**](https://github.com/wojtryb/Shortcut-Composer/wiki/Plugin-actions#cursor-trackers) - while key is pressed, tracks a cursor, switching values according to cursor offset.
- [**`Canvas preview`**](https://github.com/wojtryb/Shortcut-Composer/wiki/Plugin-actions#canvas-previews) - Temporarily changes canvas elements while the key is pressed.
- [**`Multiple assignment`**](https://github.com/wojtryb/Shortcut-Composer/wiki/Plugin-actions#multiple-assignments) - repeatedly pressing a key, cycles between multiple values of krita property.
- [**`Temporary key`**](https://github.com/wojtryb/Shortcut-Composer/wiki/Plugin-actions#temporary-keys) - temporarily activates a krita property with long press or toggles it on/off with short press.

## Important links
> Download the [latest version ⬇️](https://github.com/wojtryb/Shortcut-Composer/archive/refs/heads/main.zip) of the plugin, or visit its [github page](https://github.com/wojtryb/Shortcut-Composer/archive/refs/heads/main.zip).

---
- [Watch video tutorials 📺](https://www.youtube.com/playlist?list=PLeiJahtD9hCrtKRRYjdi-JqRtqyvH3xCG)
- [Read user manual 📄](https://github.com/wojtryb/Shortcut-Composer/wiki)
- [Join community discussion 👥](https://krita-artists.org/t/shortcut-composer-v1-2-2-plugin-for-pie-menus-multiple-key-assignment-mouse-trackers-and-more/55314)
- [Report a bug 🦗](https://github.com/wojtryb/Shortcut-Composer/issues)
- [Request a new feature 💡](https://github.com/wojtryb/Shortcut-Composer/discussions)

## What's new in the latest release?

Watch the video below, or read the [changelog](https://github.com/wojtryb/Shortcut-Composer/releases).

[![PIE MENUS - introducing Shortcut Composer](https://github.com/wojtryb/Shortcut-Composer/assets/51094047/3143fc2d-0fa7-4da1-868d-2ec054ccaeb3)](https://www.youtube.com/watch?v=Tkf2-U0OyG4 "PIE MENUS - introducing Shortcut Composer")


## Requirements
- Version of krita on plugin release: **5.1.5**
- Required version of krita: **5.1.0**

OS support state:
- [x] Windows (10, 11)
- [x] Linux (Ubuntu 20.04, 22.04)
- [ ] MacOS (Known bug of canvas losing focus after using PieMenu)
- [ ] Android (Does not support python plugins yet)

> **Note**
> On **Linux** the only oficially supported version of Krita is **.appimage**, which ships with all required dependencies. Running the plugin on Krita installed from Snap or distribution repositories is not recommended as it may not work out of the box and may require extra dependency-related work.

## How to install or update the plugin:
Installation steps are THE SAME for installing the plugin for the first time and for updating it to the new version:

1. [Download](https://github.com/wojtryb/Shortcut-Composer/archive/refs/heads/main.zip) the plugin. Do not extract it.
2. In krita's topbar, open **Tools > Scripts > Import Python Plugin From File** and pick the downloaded .zip file
3. Restart krita.
4. Set custom shortcuts in **Settings > Configure Krita > Keyboard Shortcuts** under **Scripts > Shortcut Composer: Complex Actions** section. By intention, there are no default bindings.

> **Warning**
> Some keyboard buttons like **Space, R, Y, V, 1, 2, 3, 4, 5, 6** are reserved for Krita's Canvas Inputs. Assigning those keys to actions (including those from the plugin) may result in conflicts and abnormal behaviour different for each OS. Either avoid those keys, or remove their bindings in **Settings > Configure Krita > Canvas Input Settings**.


## For krita plugin programmers
Some parts of plugin code solve general problems, which can apply outside of Shortcut Composer. Those solutions were placed in separate packages that can be copy-pasted into any other plugin and reused there.

They depend only on original [Krita API](https://api.kde.org/krita/html/classKrita.html) and PyQt5 with which krita is shipped.

- [Custom keyboard shortcut interface](./shortcut_composer/input_adapter/)
- [Config system](./shortcut_composer/config_system/)
- [Alternative Krita API](./shortcut_composer/api_krita/)
