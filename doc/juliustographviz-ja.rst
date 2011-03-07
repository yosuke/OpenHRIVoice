Usage: juliustographviz < [julius grammar]

Julius形式の文法をグラフにする

Options:
  --version      プログラムのバージョンを表示して終了する
  -h, --help     このヘルプ画面を表示して終了する
  -v, --verbose  デバッグ情報を出力する

Examples:

- SRGS形式の文法をグラフにする

  ::
  
  $ srgstojulius sample.grxml | juliustographviz | dot -Txlib

