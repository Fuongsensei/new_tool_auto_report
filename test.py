from converter.converter import ConvertDictToChainString


converter : ConvertDictToChainString = ConvertDictToChainString()
print(converter.to_chain_str({3601183:3,3212020:1}))