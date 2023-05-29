def asterisks(n):
  list = []
  for i in range(1, n + 1): # a cada iteração do for, será adicionado * multiplicado pelo indice atual.
    list.insert(i,"*" * i)
  return list

print(asterisks(6))

