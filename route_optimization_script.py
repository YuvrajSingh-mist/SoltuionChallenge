from geopy.distance import geodesic as GD
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

from copy import copy
import numpy as np
import matplotlib.pyplot as plt 

np.random.seed(42)
    

dict_places = {
    # 0: (20.294766554410437, 85.74336649575216),
    1: (20.289392134840174, 85.74188592015321),
    2: (20.28595147758, 85.75135547779522),
    3: (20.293225116208706, 85.73277612608766),
    # "PP4": "7PVR+GQ3, Gothapatna, Odisha 751003",
    # "PP5": "7PQP+8VR, Nuagan, Odisha 752054",
    # "PP6": "IIIT Campus, near STPI, Gothapatna, Odisha 751003",
    # "PP7": "7PVR+6XM, Bhubaneswar, Gothapatna, Odisha 751003",
    # "PP8": "7PRR+WG5, Gothapatna, Odisha 751003",
    # "PP9": "The SG's Kitchen, near Bandita Imperials, IIIT Square, Gothapatna, Bhubaneswar, Odisha 751003",
    # "PP10": "IDCO Plot No. 2, Institutional Area, Gothapatna, Bhubaneswar, Odisha 751029",
}

city_names = [1, 2, 3]
start = 0 


def cal_dist(place1, place2):
    return GD(place1,place2).km

while(True):
    location_name = input("Enter your current location : ")
    break
location = geolocator.geocode(location_name)


dict_places[0] = (location.latitude, location.longitude)

def create_guess(cities, start):

    guess = copy(cities)

    np.random.shuffle(guess)
    guess.append(start)
    guess.insert(0,start)
    return list(guess)

create_guess(city_names, start)



def create_generation(cities, population=100):

    generation = [create_guess(cities, start) for _ in range(population)]
    return generation

test_generation = create_generation(city_names, population=10)
# print(test_generation)

def fitness_score(guess):

    score = 0
    for ix, city_id in enumerate(guess[:-1]):
        # print(ix)
        score += cal_dist(dict_places[city_id], dict_places[guess[ix+1]])
    return score

def check_fitness(guesses):
 
    fitness_indicator = []
    for guess in guesses:
        fitness_indicator.append((guess, fitness_score(guess)))
    return fitness_indicator

# print(check_fitness(test_generation))



def get_breeders_from_generation(guesses, take_best_N=10, take_random_N=5, verbose=False, mutation_rate=0.1):

    fit_scores = check_fitness(guesses)
    sorted_guesses = sorted(fit_scores, key=lambda x: x[1])
    new_generation = [x[0] for x in sorted_guesses[:take_best_N]]
    best_guess = new_generation[0]
    
    if verbose:
    
        print(best_guess)
    
   
    for _ in range(take_random_N):
        ix = np.random.randint(len(guesses))
        new_generation.append(guesses[int(ix)])
        

    
    np.random.shuffle(new_generation)
    return new_generation, best_guess

def make_child(parent1, parent2):

    list_of_ids_for_parent1 = list(np.random.choice(parent1, replace=False, size=len(parent1)//2))
    child = [-99 for _ in parent1]
    
    for ix in list_of_ids_for_parent1:
        # print("List is: ", list_of_ids_for_parent1)
        # ix = int(ix)
        child[ix] = parent1[ix]
    for ix, gene in enumerate(child):
        # ix = int(ix)
        if gene == -99:
            for gene2 in parent2:
                if gene2 not in child:
                    child[ix] = gene2
                    break
    child[-1] = child[0]
    return child

def make_children(old_generation, children_per_couple=1):

    mid_point = len(old_generation)//2
    next_generation = [] 
    
    for ix, parent in enumerate(old_generation[:mid_point]):
        for _ in range(children_per_couple):
            next_generation.append(make_child(parent, old_generation[-ix-1]))
    return next_generation


current_generation = create_generation(city_names,population=500)
print_every_n_generations = 5

for i in range(100):
    if not i % print_every_n_generations:
        # print("Generation %i: "%i, end='')
        # print(len(current_generation))
        is_verbose = True
    else:
        is_verbose = False
    is_verbose=False
    breeders, best_guess = get_breeders_from_generation(current_generation, 
                                                        take_best_N=250, take_random_N=100, 
                                                        verbose=is_verbose)
    current_generation = make_children(breeders, children_per_couple=3)


def evolve_to_solve(current_generation, max_generations, take_best_N, take_random_N,
                    mutation_rate, children_per_couple, print_every_n_generations, verbose=False):

    fitness_tracking = []
    for i in range(max_generations):
        if verbose and not i % print_every_n_generations and i > 0:
            print("Generation %i: "%i, end='')
            print(len(current_generation))
            print("Current Best Score: ", fitness_tracking[-1])
            is_verbose = True
        else:
            is_verbose = False
        is_verbose=False
        breeders, best_guess = get_breeders_from_generation(current_generation, 
                                                            take_best_N=take_best_N, take_random_N=take_random_N, 
                                                            verbose=is_verbose, mutation_rate=mutation_rate)
        fitness_tracking.append(fitness_score(best_guess))
        current_generation = make_children(breeders, children_per_couple=children_per_couple)
    
    return fitness_tracking, best_guess

current_generation = create_generation(city_names,population=100)
fitness_tracking, best_guess = evolve_to_solve(current_generation, 100, 150, 70, 0.5, 3, 5, verbose=False)

print("Route is: ", best_guess)


# def make_fitness_tracking_plot(fitness_tracking):
#     plt.figure(dpi=150)
#     plt.plot(range(len(fitness_tracking)), fitness_tracking)
#     plt.ylabel("Fitness Score")
#     plt.xlabel("Generation")
#     plt.title("Fitness Evolution");

# make_fitness_tracking_plot(fitness_tracking)











