This plugin provides a symbol layer that renders MIL-STD-2525E / NATO APP-6E-compliant symbols. Symbols can be defined per layer, or specified based on a natural language description like "friendly mechanized infantry platoon."

# Installation

This plugin depends on the `military_symbol` Python module, which 

# Usage 

Once the plugin is activated, a new symbol layer type called "military symbol" will be available. The following fields are available for customizing the display:

- Size: This is tied to the overall symbol size, and determines how large the icon will be on the map. This can be data-defined to create changes to the size per feature.
- SIDC: This is the numeric code that specifies the symbol per the MIL-STD-2525E / NATO APP-6E standard. This can be data-defined to create changes per feature in order to do things like render the symbol type specified in a feature's fields.
- Field is name: If checked, this tells the plugin to interpret "SIDC" above as a natural-language description. This can be data-defined per feature as well. Note that the guessing of symbols based on names may be imprecise due to the limitations of the underlying [`military_symbol` Python library.](https://github.com/nwroyer/Python-Military-Symbols). 
- Style: Whether the symbol is drawn in the light, medium, dark, or unfilled style as specified in the standard.
- Draw halo: Whether to draw a colored "halo" around each symbol to make it stand out better on backgrounds with little contrast. Due to the limitations of the underlying library, this halo is currently fixed-width.
- Halo color: The color of the halo to draw, if a halo is drawn at all.

 