Usage: juliustographviz < [julius grammar]

Draw graph from Julius grammar.

Options:
  --version      show program's version number and exit
  -h, --help     show this help message and exit
  -v, --verbose  output verbose information

Examples:

- Draw graph of the SRGS grammar.

  ::
  
  $ srgstojulius sample.grxml | juliustographviz | dot -Txlib
