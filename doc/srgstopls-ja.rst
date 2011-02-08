Usage: srgstopls [grammarfile]

W3C-SRGS形式の文法からW3C-PLS形式の発音辞書を生成する

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -v, --verbose         デバッグ情報を出力する
  -r TARGETRULE, --target-rule=TARGETRULE
                        対象とするルールのIDを指定する
  -g, --gui             ファイルを開くダイアログをGUIで表示する

Examples:

- W3C-SRGS形式の文法からW3C-PLS形式の発音辞書を生成する

  ::
  
  $ srgstopls sample.grxml > sample-lex.xml

