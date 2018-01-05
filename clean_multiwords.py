import sys

def get_token(file):
    while True:
        line = file.readline()
        if not line:
            return None
        if line.strip():
            try:
                word = line.split("^")[1].split("/")[0]
                return word, line
            except Exception:
                continue
                
def get_untagged_token(file):
    while True:
        line = file.readline()
        
        if not line:
            return None
        
        line = line.strip()
        
        if not line:
            continue 
        
        return line


def get_sentence(file):
    sentence = []
    while True:
        token = get_token(file)
            
        if token is None:
            return sentence
        elif token[0] == ".":
            sentence.append(token)
            return sentence
        else:
            sentence.append(token)

def get_untagged_sentence(file):
    sentence = []
    
    while True:
        line = untagged.readline()
        
        if not line:
            return sentence
        
        line = line.strip()
        
        if not line:
            continue 
            
        sentence.append(line)
        if line == ".":
            return sentence


if __name__ == "__main__":
    tagged = open(sys.argv[1])
    untagged = open(sys.argv[2])
    result = open(sys.argv[3], "w")

    clean_sentences = set()
    while True:
        sentence = get_untagged_sentence(untagged)
        
        if not sentence:
            break
        
        for token in sentence:
            if len(token.split()) > 1:
                break
        else:
            clean_sentences.add(" ".join(sentence))


    while True:
        tokens = get_sentence(tagged)
        
        if not tokens:
            break
        
        sentence =  " ".join([token[0] for token in tokens])
        if sentence in clean_sentences:
            for token in tokens:
                result.write(token[1])
    
    tagged.close()
    untagged.close()
    result.close()
