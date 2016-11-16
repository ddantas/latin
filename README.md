# Latin charts

This repository contains a tiny Latin verb conjugator that generates yaml and pdf files containing respectively the conjugation of each verb and a graphical rendering.

Contains also a tool to generate a noun declination chart.

The design is strongly based on the charts by Ben Crowder, found [here](https://github.com/bccharts).

## Verbs

To conjugate verbs, do as follows. The first step is to go to the verbs folder:

* `cd latin/verbs`

To conjugate, for example, amo, run:

* `./conjugate.sh amo`

This command will generate the yaml file inside the folder verbs_yaml and the pdf file inside verbs_pdf. To view the resulting pdf file immediately after generation, add a pdf viewer as second parameter:

* `./conjugate.sh amo evince`

To conjugate all the supported verbs, run:

* `./conjugate_all.sh`

## Nouns

To generate the nouns declination chart, go to the nouns folder:

* `cd latin/nouns`

Then run the command:

* `./runnouns.sh`

## Prerequisites

This project requires python and the package shoebot.

## Supported verbs

[Here](https://github.com/ddantas/latin/blob/master/verbs/verbs_data/latin_verbs_ids.txt) is a list of the supported verbs until now. The list will probably grow in the near future.

## References

* George J. Adler. A Practical Grammar of the Latin Language.

* Napoleão Mendes de Almeida. Gramática Latina.

* Paulo Rónai. Gradus Primus.

* [Latin Word Study Tool](http://www.perseus.tufts.edu/hopper/morph?l=chartis&la=latin)

* [Cactus 2000 Latin Conjugation](http://latin.cactus2000.de/index.en.php)

* [Irregular Verbs in Latin](http://ancienthistory.about.com/od/irregulars/)

* [Descriptive Latin Grammar](http://www.orbilat.com/Languages/Latin/Grammar/)

* [Verbix Online Latin Verb Conjugator](http://www.verbix.com/languages/latin.shtml)

* [The Latin Dictionary](http://latindictionary.wikidot.com/)

