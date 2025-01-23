from nltk.corpus import wordnet as wn

# Ensure you have the WordNet data


# Function to retrieve synset by offset
def synset_by_offset(offset: str | int, pos='n'):
    """
    Retrieve a WordNet synset using its offset and part of speech.

    :param offset: Offset ID of the synset (integer).
    :param pos: Part of speech (e.g., 'n' for noun, 'v' for verb).
    :return: The corresponding Synset object.
    """
    if isinstance(offset, str):
        offset = int(offset)
    synset = wn.synset_from_pos_and_offset(pos, offset)
    return synset.lemmas()[0].name()


if __name__ == "__main__":
    # NOTE: first run use the following to download the WordNet data
    # import nltk
    # nltk.download('wordnet')

    # Example usage
    offset = 2747177  # Replace with the desired offset
    pos = 'n'  # Part of speech: 'n' (noun), 'v' (verb), 'a' (adjective), 'r' (adverb)
    synset = synset_by_offset(offset, pos)
    print(f"Synset: {synset}")
    # print(f"Definition: {synset.definition()}")

    # # Get other tags (synonyms or lemmas)
    # tags = [lemma.name() for lemma in synset.lemmas()]
    # print(f"Tags: {tags}")
