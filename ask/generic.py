"""generic questions that can hopefully be asked about any of the articles, as long as we classify them correctly.
   add your own! https://www.ark.cs.cmu.edu/NLP/S14/project.php"""

soccer_player = [
    "When was {} born?",
    "Which club does {} play for?",
    "When was {}'s first international appearance?"
]
constellation = [
    "Name one star that {} contains."
]
natconlang = [
    "How many native speakers does {} have?",
    "What type of language is {}?", #this question is not very good, even among these mediocre ones, imo
]
programming_language = [
    "Is {} usually interpreted or compiled?"
]
movie = [
    "When was {} released?",
    "Did {} win any accolades?",
    "Who directed {}?"]

lookup = {'football': soccer_player, 'constellations': constellation, 'natconlang': natconlang, 'proglang': programming_language, 'movies': movie}