Usage: plstosinglewordgrammar [lexiconfile]

Generate W3C-SRGS grammar from the W3C-PLS pronounciation dictionary.

Options:
  --version      show program's version number and exit
  -h, --help     show this help message and exit
  -v, --verbose  output verbose information

Examples:

- Generate single words SRGS grammar from the PLS lexicon.

  ::
  
  $ plstosinglewordgrammar sample-lex.xml > sample.grxml
