array = [1,2]

def subsets(array):
  sets = [[]]
  for i in array:
    new_sets = []
    for set in sets:
      new_sets.append(set + [i])
    sets.extend(new_sets)
  return sets

print(subsets(array))