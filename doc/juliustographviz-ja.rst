Usage: juliustographviz < [julius grammar]

Julius形式の文法をグラフにする

Options:
  --version      show program's version number and exit
  -h, --help     show this help message and exit
  -v, --verbose  デバッグ情報を出力する

Examples:

- SRGS形式の文法をグラフにする

  ::
  
  $ srgstojulius sample.grxml | juliustographviz | dot -Txlib

