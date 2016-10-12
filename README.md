# Search-Engine
Implementation of a search engine where a query is taken as input & then processed in the following order:-

1)Tokenized using nltk word tokenize
2)Removed the articles, pronouns & prepositions using stopwords
3)Removed the affixes using stemmer

Now, we have the filtered string which'll be searched in the sample database.
Sample database consists of a .txt file which has certain links to be parsed & searched for.

The links are opened & searched via KMP Algorithm for pattern matching.

Normalizing the search results -> done using normalization score
Normalization score -> (occurences of words in input string)/(total number of words)

By this normalization score, we calculate the relevance of the links. Now, we display them in decreasing order of their relevance.
