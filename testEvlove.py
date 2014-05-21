from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Util


def eval_func(chromosome):
    score = 0.0
    # iterate over the chromosome
    sum = 0
    for value in chromosome:
        sum += value
        #print sum
        score = 10000/(abs(sum-800)+1)
    return score

genome = G1DList.G1DList(40)
genome.evaluator.set(eval_func)
ga = GSimpleGA.GSimpleGA(genome)
ga.evolve(freq_stats=10)
print ga.bestIndividual()
