import re
import math
import random
import string
import time


def refresh(sel, gardon):
    for j in range(0, len(gardon.patterns)):
        if re.match(gardon.patterns[j], sel.genome):
            sel.population *= gardon.pressures[j]  # pop(t) = pop(t-1)*pressures
    sel.population = math.floor(sel.population)
    badluck = random.randint(0, sel.population)
    sel.population -= badluck


def mutate(self, gardn):
    gen1 = ""
    a = random.random()

    if len(self.genome) <= 2:
        return False
        # if genome is close to empty, mutation cannot work

    if a < 0.6:  # point mutation, 60% chance by default
        x = random.randint(0, len(self.genome)-1)
        genlist = list(self.genome)
        genlist[x] = random.choice(string.ascii_letters)
        gen1 += ''.join(genlist)

    elif 0.6 < a <= 0.8:  # insertion, 20% chance by default
        start = random.randint(0, len(self.genome) - 2)
        end = random.randint(start, len(self.genome) - 1)
        add = ""
        for i in range(0, end - start):
            add += random.choice(string.ascii_letters)
        gen1 += (self.genome[:start] + add + self.genome[end:-1])

    else:  # deletion, 20% chance by default
        pos = random.randint(1, len(self.genome) - 1)
        length = random.randint(1, len(self.genome) - pos)
        gen1 += (self.genome[:pos] + self.genome[pos + length:])
    # popl: the maximum amount of individuals that could possibly carry a mutation of
    # a certain type (population * mutation rate * possibility of a mutation of the type that happened)
    popl = math.floor(self.population * self.mutationrate * a)
    if math.floor(popl) < 1:
        return False
    else:
        print("Original genotype: " + self.genome)
        print("Mutated genotype: " + gen1)
        # newpop: every mutation has its own prominence (e.g. 1 in 50 people have red hair)
        newpop = random.randint(1, popl)
        mutant = Species(gen1, species, newpop, self.mutationrate)
        gardn.roster.append(mutant)
        self.population -= newpop
        print("Mutation occurrence rate(before any cells died, some will die in next tick): " +
              str(round(newpop*100/self.population)) + "%")
        return True


class Species:
    def __init__(self, genome, number, population, mutationrate):
        self.genome = genome
        self.number = number
        self.population = population
        self.mutationrate = mutationrate
        self.active = True

# patterns(array): Regular expressions exerting pressures on survival (simulates genome wide patterns)
# pressures(array): Pressures exerted by the patterns (e.g. a genetic pattern for multiplying every tick
# would have a pressure of 2.0, or a pattern compelling people to code would have a pressure of 0.2).
# A genome is the convoluted product of these wide patterns, and (along with bad luck) predicts the
# trends of populations of different species.
#
# A Garden is the circumstances under which genes express themselves. For example, in a polar environment, genes
# encoding white fur are advantageous - not so much in a forest. In another words, the white fur pattern could
# have a pressure of 1.3 in one Garden, while it could have a pressure of 0.7 in another.


class Garden:
    def __init__(self, patterns, pressures):
        self.patterns = patterns
        self.pressures = pressures
        self.roster = []


if __name__ == "__main__":

    garden = Garden(["a..d", "a.c", "a..b", "b..d", "ef"], [3, 0.9, 0.8, 1.2, 1.8])

    ancestralSpecies = Species("ajhdushiuhfsadidhef", 0, 20, 0.01)
    garden.roster.append(ancestralSpecies)

    t = 1
    species = 0
    while True:
        if len(garden.roster) == 0:
            print("Every cell died!")
            break
        print("t = " + str(t))
        for i in range(0, len(garden.roster)):
            m = random.random()
            if garden.roster[i].active and garden.roster[i].mutationrate >= m:
                if mutate(garden.roster[i], garden):
                    species += 1
                    print("A new species has emerged, with the number #" + str(
                        species) + "," + "descended from species #" +
                          str(garden.roster[i].number+1) + "\n")
            refresh(garden.roster[i], garden)
            if garden.roster[i].population <= 0 and garden.roster[i].active:
                print("Species #" + str(garden.roster[i].number+1) + " went extinct!")
                garden.roster[i].active = False
        allcellsdied = True
        for i in range(0, len(garden.roster)):
            if garden.roster[i].active:
                print("Population of species #" + str(i) + ": " + str(garden.roster[i].population))
                allcellsdied = False
        if allcellsdied:
            print("All cells died!")
            break
        t += 1
        # "press enter to continue"
        while True:
            if input() == "":
                break
