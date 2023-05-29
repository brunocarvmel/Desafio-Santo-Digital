array = [3, 8, 50, 5, 1, 18, 12]

def minor_pairs(array):
  array.sort() # obrigatório colocar o array em ordem crescente
  minor_difference = 0
  pairs = []
  
  for i in range(len(array) - 1):
    difference = abs(array[i] - array[i+1]) # calcula a diferença do elemento atual e proximo e torna esse valor absoluto
    if minor_difference == 0 or difference<minor_difference: # se essa diferença for menor do que a menor diferença, entao minor_difference deve receber esse valor e a lista pairs deve receber os valores da atual posição do array
      minor_difference = difference
      pairs = [(array[i], array[i+1])]
    elif difference == minor_difference: # e se essa diferença for igual com a que ja existe, adiciona esses outros valores em pairs tambem
      pairs.append((array[i],array[i+1]))
      
  return pairs

print(minor_pairs(array))
      
    
  