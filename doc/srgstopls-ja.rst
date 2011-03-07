Usage: srgstopls [grammarfile]

W3C-SRGS形式の文法からW3C-PLS形式の発音辞書を生成する

Options:
  --version             プログラムのバージョンを表示して終了する
  -h, --help            このヘルプ画面を表示して終了する
  -v, --verbose         デバッグ情報を出力する
  -r TARGETRULE, --target-rule=TARGETRULE
                        対象とするルールのIDを指定する
  -g, --gui             ファイルを開くダイアログをGUIで表示する

Examples:

- W3C-SRGS形式の文法からW3C-PLS形式の発音辞書を生成する

  ::
  
  $ srgstopls sample.grxml > sample-lex.xml

