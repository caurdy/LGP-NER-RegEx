# LGP-NER-RegEx
A linear genetic programming system for generating regular expressions for named entity recognition

## Designed for Term Project for CSE 891 : Genetic Programming

## Usage

Shown in the noteboooks

## Paper

Explains theory behind this idea and the takeaways from the project


# **Evolution of Regular Expressions**

# **for Named Entity Recognition**

Jacob Caurdy

**Abstract –** Named Entity Recognition (NER) is a subtask of [information extraction](https://en.wikipedia.org/wiki/Information_extraction) that seeks to locate and classify [named entities](https://en.wikipedia.org/wiki/Named_entity) mentioned in [unstructured text](https://en.wikipedia.org/wiki/Unstructured_data) into pre-defined categories. Currently, common approaches for NER are statistical models such as machine learning and hand-crafted grammar-based systems [1]. Here I present a linear genetic programming system that takes in named entity labeled sentences and produces a regular expression which can identify them in unstructured text. The system is an adaptation of the Tree-GP system discussed in Automatic Synthesis of Regular Expressions from Examples by A. Bartoli et. al. [2][3]. The system is available at [https://github.com/caurdy/LGP-NER-RegEx](https://github.com/caurdy/LGP-NER-RegEx).

## 1 Introduction

Regular expressions (RE) are a common tool used for searching and matching patterns in text. A regular expression (RegEx) is a sequence of characters which represent a pattern. For example the RegEx &#39;[A-Z]&#39; matches any singular uppercase character in text whereas &#39;\d{5}-\d{4}|\d{5}&#39; matches a standard ZIP Code. Without knowledge of the regular expression syntax, it can be quite hard for someone to design their own for any task, especially for NER. Additionally, many NER models are either behind paywalls or a technical expertise-wall which require knowledge of machine learning or other intensive technical domains. Thus, this system can be used in place of the other options so long as the user provides the properly formatted data. Ideally, this system can be used as a surrogate for RegEx expertise.

For experiments on this system the dataset used is the wikigold dataset [4], composed of Wikipedia articles where each string is labeled into four named entity categories persons (I-PER), locations (I-LOC), organization (I-ORG) and miscellaneous (I-MISC). This data is preprocessed into two different types, word and sentence datasets which is discussed further in 3 Experiments.

Initial Experiments did not show meaningful success as the system proved to be learning the syntax of the data instead of the semantics. Improved data processing and tuning of population-level and individual-level parameters improved fitness levels by overcoming the syntax overfitting yet recall and precision still lay substantially below a state-of-the-art level. Important takeaways from this paper lie in the adaptation of the system and not in the systems utility. It is unclear, but more so doubtful, that LGP can be used to create regular expressions for NER. If this system would be used in production, the word-dataset based result would be the best suitor for a such a task.

## 2 Approach

Formally, this system takes in a set of targets and a set of labels. The targets and labels are both strings. The labels are the expected string which should be matched or found in the target. The system attempts to learn a regular expression which match the optimal number of labels over all targets.

### 2.1 Representation

The system is composed of two levels of hierarchy. The individual level and the population level.

### 2.1.1 Individual

The genome of an individual is a list of strings which at runtime are concatenated together to represent a RegEx. The key parameters are thus the number of genes and gene length. Genes are made of operators and operands. All individuals share the same set of operators and operands. Operators can be viewed as non-terminals and operand as terminals.

- Operand Set: {a...z, A...Z, 0...9, !...?, a-z, A-Z, 0-9, \w, \d, &#39;.&#39;, &#39; &#39; }

Where &#39;…&#39; denotes one character to match from a range of ascii characters between the two symbols and &#39;-&#39; denotes the character range between the two symbols where any character can be matched from the range. &#39;\w&#39; and &#39;\d&#39; denote predefined character classes, any alphabetical string and any numeric string respectively. &#39;.&#39; denotes the wildcard character which matches any character and &#39; &#39; denotes the space character.

- Operator Set: {c\*+, c++, c?+, [c], [^c], &#39;|&#39;}

The letter c represents any string composed of terminals and non-terminals. The operators are mostly different character classes except for the or operator (&#39;|&#39;) which is a key addition in my system compared to previous which will be discussed more later.

Individuals are created at runtime by randomly generating the genes unto the gene length parameter. Genes are filled out with either operands or operators up to the gene length where the last addition must be a operand by definition. The last important parameter, operator Rate, dictates what probability a gene has of adding an operator or operand anytime a gene is modified (inception or mutation). Operator Rate was set to 0.5 or 50% for all experiments for optimal diversity and to avoid a large population of illegal individuals (individuals which at compile time produced an illegal RegEx).

### 2.1.2 Population

A population consists of a set of individuals. At first a population simply was a wrapper to improve code readability and make evolution easier. However, I added hyperparameters to introduce more diversity in the population and to modify the evolution process to be more fitting to the NER problem. The hyperparameters include mean and variance values for the distribution of gene numbers (GN) and lengths (GL) in the population. The normal distribution as used for

both traits, chosen for its observations in populations in biology. Gene length variance is always set to 1 and gene number variance is always set to 2/3.

The evolutionary hyperparameters include random proportion and mutation proportion which represent the proportion of individuals in the intermediate or kid generation which come from random initialization or mutation of existing individuals. More of these proportions later.

An additional hyperparameter is available for tourney selection size, however this was set at 7 for all experiments akin to [2].

## 2.3 Fitness

At first fitness was defined strictly in terms of accuracy but soon was moved to be defined in terms of Levenshtein distance as Albert Bartoli did in [2]. In his paper, Bartoli additionally adds a regularize term which rewards individuals for having shorter genomes. I remove this for my system as it restricted the populations diversity too much as NER is a much more complicated pattern or task which requires longer genomes. Fitness is thus defined as the sum of the Levenshtein distances between all labels and the corresponding predicted string. RE search was used in python for finding the prediction string which gets only the first match from the target string.

## 2.4 Evolutionary Operators

This system uses the classical mutator and crossover operators.

Mutation occurs at the gene level as a whole gene is either removed or completely reinitialized at a fixed probability. The probability to completely remove a gene was set at 20% for these experiments. Early on it was set at 50% however, this reduced diversity way too much in the population and needed to be reduced.

Crossover occurs between two individuals at the gene level. Two entire genes are swapped between individuals. The only shared property between swap genes is that they will always be at the same place in their respective genome. Thus, only first genes can be swapped with first genes, second genes with second genes and so on.

## 2.5 Evolution

Evolution consisted of randomly initializing a population of n individuals, producing an intermediate or kid generation of n individuals and then selecting the top n individuals from the combined population of 2n individuals of both parent and kid generation for the next population. The intermediate population is generated in three portions. A randomly initialized portion, a mutated portion, and a crossover portion. This idea is taken from [2]. In that paper they used .10, .10 and .80 proportions respectively but this proved ineffective at introducing enough diversity shown in the experiments, thus proportions were changed to .25, .25 and .50 respectively. For mutation and crossover, the parents were selected using tourney selection from a sample of 7 individuals. A generational limit of 50 was enforced which caused some great individuals to end their evolution early. Lastly, if the average fitness of the top five individuals did not change, evolution would terminate early.

## 3 Experiments

Experiments can be divided into three groups. First there were the early trials to test the workings of the system and see how it did on basic examples with sentence datasets. Then the system was fine-tuned to avoid early problems of syntax overfitting and quick diversity loss. After which I re-implemented sentence datasets and created word datasets as well. The objective for the experiments was to first find the optimal gene number and length means for both word datasets and sentence datasets and then run many evolutions to find the best individual possible.

### 3.1 Datasets

This system can be used on any dataset so long as the targets and labels follow the correct format. For my experiments I used wikigold dataset [4] and preprocessed it into two types of datasets, word, and sentence. The sentence dataset is the original type early experiments were ran on where each target consisted of a before word, the named entity (one or more strings) and then some text afterwards in the following pseudo-pattern: &quot;the NAMED ENTITY HERE target had the same formula every time&quot;. The system quickly learned to predict the first few tokens of the sentence and I was forced to reimplement the data preprocessing to vary where the Named Entity took place. The motivation behind using two different datasets was to give the system the opportunity to learn the context surrounding a named entity versus giving it only single strings.

### 3.2 Sentence Datasets

Sentence datasets consisted of one or more tokens (defined as strings with a space with a leading and ending space character) with one named entity within the sentence. A named entity can consist of one or more tokens, but they must be sequential.

#### 3.2.1 Early Trials

Here I provide one example of the syntax overfitting shown by early runs of the system on sentence datasets. Below in Figure 1, the system learned to predict the first few alphabetic tokens from the sentence which where the named entity always was in the sentence.

Generation 16, Fitness: 3889.00, Best Genome: \w\w\w\w+.

**Figure 1:** Best individual from an early hyperparameter search on sentence datasets consisting of 10 Wikigold articles (GN=2, GL=6)

#### 3.2.2 Full and Random Context

In the improved datasets I created two types of sentence datasets. Random and full context datasets. Context is defined as the number of tokens preceding the current named entity before you reach the prior named entity in the text, or as viewed from the target, the number of tokens before the named entity in a sentence or target. Random context included a random number of tokens before the named entity, up to but not including the previous. Full context included all token before the named entity, up to but not including the previous. The average sentence length for full context dataset is about 100 characters whereas average sentence length for random context dataset is about 78 characters.

Figure 2 shows the best individuals for both random and max context during a hyperparameter search. From experience the best genomes have more genes and gene length does not matter as much. Figure 3 shows average fitness for both random and max content. Random context edged out max context which is surprising.

Best Idv. Max Context &quot;[A-Z][^.]\w+.&quot; Fitness=4366.00 (GN=4, GL=2)

Best Idv. Rand Context &quot;[A-Z][^5.][^]\w\w[^G]|.a-z[0-9]&quot; Fitness=4257.00 (GN=4, GL=6)

**Figure 2:** Best individuals out of random and maximum context hyperparameter search. Gene length search space was [2, 4, 6] and gene number was [1-5].

Average Fitness Max Context: 5200.00

Average Fitness Random Context: 5034.00

**Figure 3:** Average Fitness for random and maximum context datasets each with 110-examples over a hyperparameter search of 15 combinations.

### 3.3 Word Datasets

Word datasets consisted of a single token. Thus, the label was binary. Either it consisted of the entire target or the null string &#39;&#39;. Figure 4 shows results for a comparison between two sets of intermediate generation proportions. I hypothesized that 80% standard crossover eliminated too much diversity too quickly and thus decreased it to 50% in the altered proportion. This proved effective in decreasing average fitness and producing a better individual.

Avg. Fitness altered proportions 2776.50, [A-Z]\w\w[^(?+]|[^A-Z]\d\d[a-z] (Fitness=1912.00)

Avg. Fitness, standard proportions 3034.00, [^\] a-z].\w.. (Fitness=2063.00)

**Figure 4:** Average fitness of 10 runs on a ~3300-word dataset on two different proportions of evolutionary hyperparameters. Altered proportions have .25, .25 and .50 for random, mutants and crossover. Standard proportions have .10, .10 and .80 respectively.

##


## 4 Discussion

The system did not prove to be highly successful but there was a lot to observe and learn along the way. I see no reason that this system would replace current NER models anytime soon but it&#39;s still a cool space to see just what evolutionary computation is capable of. The primary motivation behind this system was to teach myself evolutionary computation and to see if I could create a system that could be used in my capstone course. Only the former objective was met, but my education and use of evolutionary computation is only beginning, and I hope to further my knowledge of the field to utilize its ability to find unique solutions to its utmost potential. To be honest, it still did better than I expected.

As an educational project, this was great. As an actual utility, not so much. There&#39;s plenty of things with more time and computational power I could have done but maybe next time.

## 6 Future Work

The full power of this system has not yet been explored. This system could be used on other tasks and could be further pushed on NER. All experiments were run on a simple machine with an i5 processor thus there is potential for more exploration on stronger machines to fully explore the evolutionary space.

As for modifying the system there are a few ideas that should be done before writing off LGP for this task. I believe the system was close to creating a few very powerful individuals and needs more time and more incentive to cultivate these individuals further. Thus, it would be interesting to see a sort of elitism crossover where the top individuals after a certain threshold are mutated more than others. On top of that the crossover operator should be between multiple indices not just the same one.

Lastly, there was no test set used in my experiments which is a common practice and should have been included. Another technical mishap was using summation of Levenshtein and not an average to have more readable fitness values.

#

## References

[1][https://en.wikipedia.org/wiki/Named-entity\_recognition](https://en.wikipedia.org/wiki/Named-entity_recognition)

[2] A. Bartoli, G. Davanzo, A. De Lorenzo, E. Medvet and E. Sorio, &quot;Automatic Synthesis of Regular Expressions from Examples,&quot; in _Computer_, vol. 47, no. 12, pp. 72-80, Dec. 2014, doi: 10.1109/MC.2014.344.

[3] A. Bartoli, A. De Lorenzo, E. Medvet and F. Tarlao, &quot;Inference of Regular Expressions for Text Extraction from Examples,&quot; in _IEEE Transactions on Knowledge and Data Engineering_, vol. 28, no. 5, pp. 1217-1230, 1 May 2016, doi: 10.1109/TKDE.2016.2515587.

[4] [https://github.com/juand-r/entity-recognition-datasets/tree/master/data/wikigold](https://github.com/juand-r/entity-recognition-datasets/tree/master/data/wikigold)
