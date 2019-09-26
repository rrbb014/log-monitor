class JaccardSimilarityBasedDetector:
    def measure(self, sentence1, sentence2):
        sentence1_words = set(sentence1.split())
        sentence2_words = set(sentence2.split())
        
        intersection = sentence1_words.intersection(sentence2_words)
        union = sentence1_words.union(sentence2_words)
        
        similarity = len(intersection) / len(union)
        return similarity
