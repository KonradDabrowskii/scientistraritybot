import json

def load_nfts(file_name):
    with open(file_name, "r") as f:
        return json.load(f)

nfts = load_nfts("metadata.json")

def rarity_score(nft):
    total_percent = sum([float(attr["percent"].strip('%')) for attr in nft["meta"]["attributes"]])
    return total_percent

ranked_nfts = sorted(nfts, key=rarity_score)

print("Ranked NFTs:")
for i, nft in enumerate(ranked_nfts):
    print(f"{i + 1}. {nft['meta']['name']} - Rarity score: {rarity_score(nft)}")