Usage: srgstojulius [grammarfile]

W3C-SRGS形式の文法からJulius形式の文法を生成する

Options:
  --version             プログラムのバージョンを表示して終了する
  -h, --help            このヘルプ画面を表示して終了する
  -v, --verbose         デバッグ情報を出力する
  -r TARGETRULE, --target-rule=TARGETRULE
                        対象とするルールのIDを指定する

Examples:

- W3C-SRGS形式の文法からJulius形式の文法を生成する

  ::
  
  $ srgstojulius sample.grxml > sample.julius

