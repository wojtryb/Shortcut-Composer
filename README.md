# Shortcut composer **v1.6.0**

[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
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
- [**`Rotation selector`**](https://github.com/wojtryb/Shortcut-Composer/wiki/Plugin-actions#rotation-selectors) - while key is pressed, displays a widget, which allows to set an angle-based property.

## Important links
> Download the [**`latest version`**](https://github.com/wojtryb/Shortcut-Composer/archive/refs/heads/main.zip) of the plugin, or visit its [**`github page`**](https://github.com/wojtryb/Shortcut-Composer).

---

- [Watch video tutorials 📺](https://www.youtube.com/playlist?list=PLeiJahtD9hCrtKRRYjdi-JqRtqyvH3xCG)
- [Read user manual 📄](https://github.com/wojtryb/Shortcut-Composer/wiki)
- [Join community discussion 👥](https://krita-artists.org/t/shortcut-composer-v1-2-2-plugin-for-pie-menus-multiple-key-assignment-mouse-trackers-and-more/55314)
- [Report a bug 🦗](https://github.com/wojtryb/Shortcut-Composer/issues)
- [Request a new feature 💡](https://github.com/wojtryb/Shortcut-Composer/discussions)
- [What's new in latest version? ⭐](https://github.com/wojtryb/Shortcut-Composer/releases)

## Changelog videos

[![PIE MENUS - introducing Shortcut Composer](https://user-images.githubusercontent.com/51094047/244950488-83bd44ff-87f6-4b95-82c7-0f5031bb1b8e.png)](https://www.youtube.com/watch?v=eHK5LBMNiU0 "Managing BRUSHES with Shortcut Composer 1.3")

[![PIE MENUS - introducing Shortcut Composer](https://github-production-user-asset-6210df.s3.amazonaws.com/51094047/238015603-3143fc2d-0fa7-4da1-868d-2ec054ccaeb3.png)](https://www.youtube.com/watch?v=Tkf2-U0OyG4 "PIE MENUS - introducing Shortcut Composer")

[![PIE MENUS - release video](https://github-production-user-asset-6210df.s3.amazonaws.com/51094047/238179887-87c00d86-0e65-46c2-94c4-52bb02c99501.png)](https://youtu.be/hrjBycVYFZM "PIE MENUS - introducing Shortcut Composer")

## Requirements
- Version of krita on plugin release: **5.2.9**
- Required version of krita: **5.2.2** or later

OS support state:
- [x] Windows (10, 11)
- [x] Linux (Ubuntu 20.04, 22.04)
- [ ] MacOS (Known bug of canvas losing focus after using PieMenu)
- [ ] Android (Does not support python plugins yet)

> **Note**
> On **Linux** the only officially supported version of Krita is **.appimage**, which ships with all required dependencies. Running the plugin on Krita installed from Snap or distribution repositories is not recommended as it may not work out of the box and may require extra dependency-related work.

## How to install or update the plugin:
Installation steps are THE SAME for installing the plugin for the first time and for updating it to the new version:

1. Download the plugin:
    - Use the direct link for [stable](https://github.com/wojtryb/Shortcut-Composer/archive/refs/heads/main.zip) or [development](https://github.com/wojtryb/Shortcut-Composer/archive/refs/heads/development.zip) release.
    - Alternatively, on [github page](https://github.com/wojtryb/Shortcut-Composer) switch from `main` to any of the unstable versions, click the green button `code` and pick the `download zip` option.
2. In krita's topbar, open **Tools > Scripts > Import Python Plugin From File** and pick the downloaded .zip file
3. Restart krita.
4. Set custom shortcuts in **Settings > Configure Krita > Keyboard Shortcuts** under **Scripts > Shortcut Composer: ...** sections. By intention, there are no default bindings.

> **Warning**
> Some keyboard buttons like **Space, R, Y, V, 1, 2, 3, 4, 5, 6** are reserved for Krita's Canvas Inputs. Assigning those keys to actions (including those from the plugin) may result in conflicts and abnormal behavior different for each OS. Either avoid those keys, or remove their bindings in **Settings > Configure Krita > Canvas Input Settings**.


## For krita plugin programmers
Some parts of plugin code solve general problems, which can apply outside of Shortcut Composer. Those solutions were placed in separate packages that can be copy-pasted into any other plugin and reused there.

They depend only on original [Krita API](https://api.kde.org/krita/html/classKrita.html) and PyQt5 with which krita is shipped.

- [Custom keyboard shortcut interface](./shortcut_composer/input_adapter/)
- [Config system](./shortcut_composer/config_system/)
- [Alternative Krita API](./shortcut_composer/api_krita/)
