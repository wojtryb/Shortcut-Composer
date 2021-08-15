# Temporary and pernament tool switching with one button - krita add-on

## Installation:
### Krita 5:
- on github, click the green button 'code' and pick 'download zip'. Do not extract it.
- go to *Tools > Scripts > Import Python Plugin From File* and pick the downloaded .zip file
- restart krita.

### Krita 4:
- on github, click the green button 'code' and pick 'download zip'. Do not extract it.
- go to *Tools > Scripts > Import Python Plugin* and pick the downloaded .zip file
- restart krita.
- activate the addon: *Settings > Configure Krita... > Python Plugin Manager > Tool Modifiers (ON).*
- restart krita again.

## Usage:
- Add-on allows to use a single keyboard button to switch to a tool permanently or temporarily.
- Long-pressing a button will cause the given tool to switch back to freehand brush tool as soon, as the key is released.
- Short-pressing a button works as a toggle between the given tool and freehand brush tool
- A keyboard binding can be set from krita in *Settings > Configure Krita > Keyboard shortcuts > search: (toggle)

## Tools supported by default:
### Functions:
- Eraser
- Preserve alpha
### Named tools:
- Freehand selection
- Transform tool
- Move tool
- Line tool
- Gradient tool
### Custom tools (easier to change):
- Custom tool 1: Rectangular selection tool
- Custom tool 2: Contiguous selection tool
- Custom tool 3: Reference images tool

## Changing supported tools:
### Fast way:
- Go to resource folder (Settings > Manage Resources > Open Resource Folder)
- Open file pyKrita/toolModifiers/SETUP.py
- Replace any of the three bottom TOOLS with krita name of the tool you want to set up
- (List of available names - coming)

### Proper way:
- in importCode/devinedActions.py add a dictionary item with {kritaName : humanName}
- in pyKrita/toolModifiers.desktop create a keyboard shortcut using humanName

## Limitations
- used keyboard shortcut should consist of a single key (don't add ctrl, shift... )
- while long-pressed, pressing ctrl or shift to modify tools behaviour may not work and collide with other shortcuts
- impact on krita performance is not yet fully tested. 
