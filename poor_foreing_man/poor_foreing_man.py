"""Display a graph of letters frequency"""
import pprint
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def main():
    text = input("Text: ")
    
    graph = {}

    #Register all letters in the text
    for l in text:
        l = l.lower()
        if l.isalpha():
            graph[l] = graph.get(l, []) + [l]
    
    #Register all letters aren't in the text    
    for l in ALPHABET:
        graph[l] = graph.get(l, [])
        
    #Formated print
    pp = pprint.PrettyPrinter(width=1000)
    pp.pprint(graph)

if __name__ == "__main__":
    main()
