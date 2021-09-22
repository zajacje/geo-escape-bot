import queue

clues = queue.Queue()

text = [('West village H acronym?', 'WVH'), ('What is the CS building?', 'Khoury'), ('What is the student center called?' , 'Curry')]

for pair in text:
  clues.put(pair)
