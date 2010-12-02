;  This file is part of OpenHRI.
;  Copyright (C) 2010  AIST-OpenHRI Project
;

!include "MUI2.nsh"
!include "LogicLib.nsh"
!include "WordFunc.nsh"
!insertmacro WordFind

!define VERSION "1.01"

Outfile "update-checker-${VERSION}.exe"
ShowInstDetails show

!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Japanese"
!insertmacro MUI_RESERVEFILE_LANGDLL

!insertmacro MUI_PAGE_INSTFILES

;Language strings
LangString ASK_NEW_INSTALL ${LANG_ENGLISH} "$PKG_NAME is not installed. Would you like to install the package?"
LangString ASK_UPDATE ${LANG_ENGLISH} "$PKG_NAME is updated to version $PKG_VERSION_ONLINE. Would you like to install the update?"
LangString UPDATE_COMPLETE ${LANG_ENGLISH} "Update complete."
LangString ASK_NEW_INSTALL ${LANG_JAPANESE} "インストールされていないパッケージ$PKG_NAMEが見つかりましたインストールしますか？"
LangString ASK_UPDATE ${LANG_JAPANESE} "パッケージ$PKG_NAMEの新しいバージョン$PKG_VERSION_ONLINEが見つかりました。このバージョンにアップデートしますか？"
LangString UPDATE_COMPLETE ${LANG_JAPANESE} "アップデートが完了しました。"
 
Var SW_RET
Var SW_TMPFILE

!macro downloadAndInstall SW_NAME SW_URL
  StrCpy $SW_TMPFILE "$TEMP\${SW_NAME}-update.exe"
  NSISdl::download ${SW_URL} $SW_TMPFILE
  Pop $SW_RET
  ${If} $SW_RET == "success"
    DetailPrint "Installing ${SW_NAME}"
    ExecWait $SW_TMPFILE $0
    DetailPrint "Return code: $0"
    ${If} $0 != "0"
      MessageBox MB_OK "${SW_NAME} installer returned $0"
    ${EndIf}
    Delete $SW_TMPFILE
    Push $0
  ${Else}
    MessageBox MB_OK "Download failed: ${SW_NAME}"
    Push 1
  ${EndIf}
!macroend

!define URL "http://openhri.net/sw-update-util.php"
!define INSTDIR_REG_ROOT "HKLM"
!define INSTDIR_REG_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\"

Var VERS
Var PKG_ENTRY
Var PKG_INDEX
Var PKG_NAME
Var PKG_VERSION
Var PKG_VERSION_ONLINE
Var PKG_URL
Var COMPARE_RESULT

Section "main"

GetTempFileName $VERS
NSISdl::download ${URL} $VERS
Pop $0
${If} $0 != "success"
  DetailPrint "$0"
  MessageBox MB_OK "Failed to download update information."
  Goto end
${EndIf}

ReadINIStr $PKG_ENTRY $VERS "main" "entry"
DetailPrint "Entry: $PKG_ENTRY"

StrCpy $PKG_INDEX "0"

${While} 1 == 1
  IntOp $PKG_INDEX $PKG_INDEX + 1
  ${WordFind} $PKG_ENTRY "," "+$PKG_INDEX" $PKG_NAME
  ${If} $PKG_INDEX > 1
    ${IfThen} $PKG_NAME == $PKG_ENTRY ${|} ${Break} ${|}
  ${EndIf}

  ReadINIStr $PKG_VERSION_ONLINE $VERS $PKG_NAME "version"
  ReadINIStr $PKG_URL $VERS $PKG_NAME "url"
  ReadRegStr $PKG_VERSION ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}$PKG_NAME" "DisplayVersion"

  DetailPrint "Found package: $PKG_NAME"
  DetailPrint "Package version: $PKG_VERSION_ONLINE"
  DetailPrint "Package URL: $PKG_URL"
  DetailPrint "Current package version: $PKG_VERSION"

  ${If} $PKG_VERSION == ""
     MessageBox MB_YESNO $(ASK_NEW_INSTALL) IDYES newinstall IDNO next
newinstall:
     !insertmacro downloadAndInstall $PKG_NAME $PKG_URL
next:
  ${Else}
    ${VersionCompare} $PKG_VERSION $PKG_VERSION_ONLINE $COMPARE_RESULT
    ${If} $COMPARE_RESULT == "2"
      MessageBox MB_YESNO $(ASK_UPDATE) IDYES newupdate IDNO next2
newupdate:
      !insertmacro downloadAndInstall $PKG_NAME $PKG_URL
next2:
    ${EndIf}
  ${EndIf}

${EndWhile}

Delete $VERS

MessageBox MB_OK $(UPDATE_COMPLETE)

end:

SectionEnd

Function .onInit
  !insertmacro MUI_LANGDLL_DISPLAY
FunctionEnd
