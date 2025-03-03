from .plugin import MilitarySymbolPlugin

def classFactory(iface):
    return MilitarySymbolPlugin(iface)

