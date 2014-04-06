Ideas
-----
* Take a bunch of sentences that could be potential questions from wikipedia articles. Manually classify them into the type of question they should become<br/>
  (Just do who, when, why, how, what, where)
* Now train a BAG OF WORDS NAIVE BAYES CLASSIFIER (WOOHOO) on these classified questions
* Now we can classify all sentences in any article given to us! woohoo! so we know what kinds of questions to generate!

Whoops
=======
* So while messing with the Stanford NER system, I realised that it tags entities with the following:<br/>
  - Time, Location, Organization, Person, Money, Percent, Date
  which might actually (in some sense, given the limited amount of training data we have) be a more reliable indicator of what kind of questions we can generate from that sentence.<br/>
  On the other hand, something like "Organization" is really quite vague. If we had anything resembling a decent ontology, we could, for instance, look up something like "Manchester United" and be able to generate a 