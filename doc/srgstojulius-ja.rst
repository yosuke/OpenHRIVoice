Usage: srgstojulius [grammarfile]

W3C-SRGS形式の文法からJulius形式の文法を生成する

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -v, --verbose         デバッグ情報を出力する
  -r TARGETRULE, --target-rule=TARGETRULE
                        対象とするルールのIDを指定する

Examples:

- W3C-SRGS形式の文法からJulius形式の文法を生成する

  ::
  
  $ srgstojulius sample.grxml > sample.julius

