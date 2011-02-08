Usage: srgstopls [grammarfile]

Generate W3C-PLS lexcon from the W3C-SRGS grammar.

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -v, --verbose         output verbose information
  -r TARGETRULE, --target-rule=TARGETRULE
                        specify target rule id
  -g, --gui             show file open dialog in GUI

Examples:

- Generate W3C-PLS lexcon from the W3C-SRGS grammar.

  ::
  
  $ srgstopls sample.grxml > sample-lex.xml

