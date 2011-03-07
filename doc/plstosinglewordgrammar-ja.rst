Usage: plstosinglewordgrammar [lexiconfile]

W3C-PLS形式の発音辞書からW3C-SRGS形式の文法を生成する

Options:
  --version      プログラムのバージョンを表示して終了する
  -h, --help     このヘルプ画面を表示して終了する
  -v, --verbose  デバッグ情報を出力する

Examples:

- PLS形式の発話辞書からSRGS形式の文法を生成する

  ::
  
  $ plstosinglewordgrammar sample-lex.xml > sample.grxml

