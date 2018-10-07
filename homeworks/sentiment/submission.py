#!/usr/bin/python

import random
import collections
import math
import sys
from util import *

############################################################
# Problem 3: binary classification
############################################################

############################################################
# Problem 3a: feature extraction

def extractWordFeatures(x):
    """
    Extract word features for a string x. Words are delimited by
    whitespace characters only.
    @param string x: 
    @return dict: feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    output = {}
    for word in x.split():
        output[word] = output[word] + 1 if word in output else 1
    return output
    # END_YOUR_CODE

############################################################
# Problem 3b: stochastic gradient descent

def learnPredictor(trainExamples, testExamples, featureExtractor, numIters, eta):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, the step size |eta|, return the weight vector (sparse
    feature vector) learned.

    You should implement stochastic gradient descent.

    Note: only use the trainExamples for training!
    You should call evaluatePredictor() on both trainExamples and testExamples
    to see how you're doing as you learn after each iteration.
    '''
    weights = {}  # feature => weight
    # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)

    def scaler_product(d, x): return {k: v * x for k, v in d.items()}

    def gradient_hinge_loss(phi_x, y, w): return scaler_product(phi_x, -y) if dotProduct(w, phi_x)*y < 1 else {}

    for _ in range(numIters):
        for x, y in trainExamples:
            phi_x = featureExtractor(x)
            increment(weights, -eta, gradient_hinge_loss(phi_x, y, weights))

    # END_YOUR_CODE
    return weights

############################################################
# Problem 3c: generate test case

def generateDataset(numExamples, weights):
    '''
    Return a set of examples (phi(x), y) randomly which are classified correctly by
    |weights|.
    '''
    random.seed(42)
    # Return a single example (phi(x), y).
    # phi(x) should be a dict whose keys are a subset of the keys in weights
    # and values can be anything (randomize!) with a nonzero score under the given weight vector.
    # y should be 1 or -1 as classified by the weight vector.
    def generateExample():
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        phi = {k: random.randint(1, 10) for k, v in weights.iteritems() if 1 == random.randint(0, 1)}
        y = 1 if dotProduct(phi, weights) >= 0 else -1
        # END_YOUR_CODE
        return (phi, y)
    return [generateExample() for _ in range(numExamples)]

############################################################
# Problem 3e: character features

def extractCharacterFeatures(n):
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all n-grams of |x| without spaces.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    You may assume that n >= 1.
    '''
    def extract(x):
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        vector = {}
        stripped = x.replace(" ", "")
        for c in range(len(stripped) - n + 1):
            gram = stripped[c: c + n]
            vector[gram] = vector[gram] + 1 if gram in vector else 1
        return vector
        # END_YOUR_CODE
    return extract

############################################################
# Problem 4: k-means
############################################################


def kmeans(examples, K, maxIters):
    '''
    examples: list of examples, each example is a string-to-double dict representing a sparse vector.
    K: number of desired clusters. Assume that 0 < K <= |examples|.
    maxIters: maximum number of iterations to run (you should terminate early if the algorithm converges).
    Return: (length K list of cluster centroids,
            list of assignments (i.e. if examples[i] belongs to centers[j], then assignments[i] = j)
            final reconstruction loss)
    '''
    # BEGIN_YOUR_CODE (our solution is 32 lines of code, but don't worry if you deviate from this)

    def mod_square(vector): return sum([v*v for k, v in vector.iteritems()])

    def cluster_assignment_loss(mod_square_phi, mod_square_mu, dot_product):
        return mod_square_phi + mod_square_mu - 2 * dot_product

    def average_vector(vectors):
        avg_vector = collections.defaultdict(float)
        for vector in vectors:
            for (key, value) in vector.iteritems():
                avg_vector[key] += value
        return dict({key: value/len(vectors) for key, value in avg_vector.iteritems()})

    cluster_locations = random.sample(examples, K)
    examples_mod_square = [mod_square(example) for example in examples]
    last_assigned_examples = []

    for _ in range(maxIters):
        clusters_with_mod_square = [(v, mod_square(v)) for v in cluster_locations]

        assigned_examples = [0] * len(examples)
        for index, example in enumerate(examples):
            losses = [cluster_assignment_loss(examples_mod_square[index], mod_square_mu, dotProduct(examples[index], c)) for (c, mod_square_mu) in clusters_with_mod_square]
            assigned_examples[index] = losses.index(min(losses))

        if assigned_examples == last_assigned_examples:
            break
        else:
            last_assigned_examples = assigned_examples

        clustered_vectors = [[] for _ in range(K)]
        for vector_index, cluster_number in enumerate(assigned_examples):
            clustered_vectors[cluster_number].append(examples[vector_index])

        cluster_locations = [average_vector(v) for v in clustered_vectors]

    return cluster_locations, last_assigned_examples, sum([cluster_assignment_loss(examples_mod_square[example_index], mod_square(cluster_locations[cluster_index]), dotProduct(examples[example_index], cluster_locations[cluster_index])) for example_index, cluster_index in enumerate(last_assigned_examples)])
    # END_YOUR_CODE
