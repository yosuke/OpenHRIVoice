Usage: srgstojulius [grammarfile]

Generate Julius grammar from the W3C-SRGS grammar.

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -v, --verbose         output verbose information
  -r TARGETRULE, --target-rule=TARGETRULE
                        specify target rule id

Examples:

- Generate Julius grammar from the W3C-SRGS grammar.

  ::
  
  $ srgstojulius sample.grxml > sample.julius

