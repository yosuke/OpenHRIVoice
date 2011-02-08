Usage: plstosinglewordgrammar [lexiconfile]

W3C-PLS形式の発音辞書からW3C-SRGS形式の文法を生成する

Options:
  --version      show program's version number and exit
  -h, --help     show this help message and exit
  -v, --verbose  デバッグ情報を出力する

Examples:

- PLS形式の発話辞書からSRGS形式の文法を生成する

  ::
  
  $ plstosinglewordgrammar sample-lex.xml > sample.grxml

