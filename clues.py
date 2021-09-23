import queue

clues = queue.Queue()

text = [('You remember seeing a lot of books. It was quiet.', 'snell'), ('Next, you went to a place with a lot of computers', 'khoury'), ('What is the student center called?' , 'curry')]

for pair in text:
  clues.put(pair)
