# Text to Astromech integration for Home Assistant (R2D2 Beep Boop Sounds)

Generate Astromech sounds in Home Assistant!

You have the choice between these voices:

- __Astromech__: Each letter in your TTS message is assigned to a sound. You can check the sounds here: https://github.com/MomsFriendlyRobotCompany/ttastromech/tree/master/ttastromech/sounds
- __Astromech (short)__: The TTS message gets hashed into a 6 letter word, which is then forwarded to the Astromech voice. This helps with long TTS messages that are generated for example by Assist.

***

## Installation using HACS

This component is available via HACS as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories) which is the recommended method of installation.

1. Add custom repository to HACS
1. Search for "Astromech"
1. Install integration
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Astromech TTS"

## Manual Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `astromech`.
1. Download _all_ the files from the `custom_components/astromech/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Astromech TTS"


## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

## Special thanks

- `ttastromech` for the awesome python library: https://github.com/MomsFriendlyRobotCompany/ttastromech
- https://github.com/hug33k/PyTalk-R2D2 on which `ttastromech` is based on
- Leylosh's Scratch project for the sounds used by the libraries above (https://scratch.mit.edu/projects/766189/)