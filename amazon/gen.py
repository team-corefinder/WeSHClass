import json, re

def dataset():
  with open('amazon-coreclass-1000.jsonl') as input_file:
    with open('dataset.txt', 'w') as output_file:
      for line in input_file:
        j = json.loads(line)
        output_file.write(f'{j["reviewText"]}\n')

def to_line(k, v):
  return '\t'.join([k] + list(v.keys())) + '\n'

def find_leaves(taxo):
  result = []
  for k, v in taxo.items():
    if not v:
      result.append(k)
    else:
      result += find_leaves(v)
  return result

def hier():
  with open('taxonomy.json') as input_file:
    taxo = json.load(input_file)
    with open('label_hier.txt', 'w') as output_file:
      output_file.write(to_line('ROOT', taxo))
      for k, v in taxo.items():
        output_file.write(to_line(k, v))
        for kk, vv in v.items():
          output_file.write(to_line(kk, vv))

def doc_id():
  with open('taxonomy.json') as taxo_file:
    taxo = json.load(taxo_file)
    leaves = find_leaves(taxo)

    with open('amazon-coreclass-1000.jsonl') as document_file:
      docs = [json.loads(l)['categories'] for l in document_file.readlines()]

      with open('doc_id.txt', 'w') as output_file:
        for l in leaves:
          ids = [str(i) for i, categories in enumerate(docs) if l in categories][:10]
          output_file.write(f'{l}\t{" ".join(ids)}\n')

def keywords():
  with open('taxonomy.json') as taxo_file:
    taxo = json.load(taxo_file)
    leaves = find_leaves(taxo)

    with open('keywords.txt', 'w') as output_file:
      for l in leaves:
        words = [w.lower() for w in l.split() if '&' not in w]
        output_file.write(f'{l}\t{" ".join(words)}\n')


def labels():
  with open('amazon-coreclass-1000.jsonl') as input_file:
    with open('labels.txt', 'w') as output_file:
      for line in input_file:
        j = json.loads(line)
        categories = j['categories']
        output_file.write(categories[-1] + '\n')

def sentence_lengths():
  with open('dataset.txt') as f:
    for line in f:
      for s in re.split(r"\.|\?|\!", line):
        yield len(s)

def max_len():
  with open('dataset.txt') as f:
    lens = [len(line) for line in f.readlines()]
    print(max(lens))

def max_sentence_len():
  print(max(sentence_lengths()))

def find_big_line():
  with open('dataset.txt') as f:
    for line in f:
      if len(line) >= 25000:
        print(line)


if __name__ == '__main__':
  dataset()
  hier()
  doc_id()
  labels()
  keywords()
  max_len()
  max_sentence_len()
