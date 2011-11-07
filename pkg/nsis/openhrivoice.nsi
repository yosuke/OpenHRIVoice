;  This file is part of OpenHRI.
;  Copyright (C) 2010  AIST-OpenHRI Project
;

!addplugindir "."

;--------------------------------
;Include Modern UI

!include "MUI.nsh"

;--------------------------------
;General

!define PACKAGE_NAME "OpenHRIVoice"
!define PACKAGE_VERSION "2.00"
!define OUTFILE "${PACKAGE_NAME}-${PACKAGE_VERSION}-installer.exe"
!define TOP_SRCDIR "..\.."
!define TOP_BUILDDIR "..\.."
!define INSTDIR_REG_ROOT "HKLM"
!define INSTDIR_REG_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PACKAGE_NAME}"
!define SCDIR "$SMPROGRAMS\OpenHRI\voice"

;Name and file
Name "${PACKAGE_NAME} ${PACKAGE_VERSION}"
OutFile "${OUTFILE}"
ShowInstDetails show
ShowUninstDetails show
InstallDir "$PROGRAMFILES\${PACKAGE_NAME}"
InstallDirRegKey ${INSTDIR_REG_ROOT} ${INSTDIR_REG_KEY} "InstallDir"

!include "AdvUninstLog.nsh"
!insertmacro UNATTENDED_UNINSTALL
;!insertmacro INTERACTIVE_UNINSTALL

;--------------------------------
;Interface Settings

;  !define MUI_ICON "${TOP_SRCDIR}\icons\openhrivoice.ico"
;  !define MUI_UNICON "${TOP_SRCDIR}\icons\openhrivoice.uninstall.ico"

;--------------------------------
;Pages

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE $(MUILicense)
!insertmacro MUI_PAGE_LICENSE $(MUILicense_Julius)
!insertmacro MUI_PAGE_LICENSE $(MUILicense_OpenJTalk)
!insertmacro MUI_PAGE_LICENSE $(MUILicense_Male)
!insertmacro MUI_PAGE_LICENSE $(MUILicense_Mei)
!insertmacro MUI_PAGE_LICENSE $(MUILicense_Festival)
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

;--------------------------------
;Languages

!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Japanese"

;--------------------------------
;License Language String

LicenseLangString MUILicense ${LANG_ENGLISH} "${TOP_SRCDIR}\COPYING"
LicenseLangString MUILicense ${LANG_JAPANESE} "${TOP_SRCDIR}\COPYING"
LicenseLangString MUILicense_Julius ${LANG_ENGLISH} "C:\Program Files (x86)\OpenHRIVoice\3rdparty\dictation-kit-v4.0-win\doc\LICENSE.txt"
LicenseLangString MUILicense_Julius ${LANG_JAPANESE} "C:\Program Files (x86)\OpenHRIVoice\3rdparty\dictation-kit-v4.0-win\doc\LICENSE.txt"
LicenseLangString MUILicense_OpenJTalk ${LANG_ENGLISH} "${TOP_SRCDIR}\pkg\nsis\License-Open_JTalk.txt"
LicenseLangString MUILicense_OpenJTalk ${LANG_JAPANESE} "${TOP_SRCDIR}\pkg\nsis\License-Open_JTalk.txt"
LicenseLangString MUILicense_Male ${LANG_ENGLISH} "C:\Program Files (x86)\OpenHRIVoice\3rdparty\hts_voice_nitech_jp_atr503_m001-1.04\COPYING"
LicenseLangString MUILicense_Male ${LANG_JAPANESE} "C:\Program Files (x86)\OpenHRIVoice\3rdparty\hts_voice_nitech_jp_atr503_m001-1.04\COPYING"
LicenseLangString MUILicense_Mei ${LANG_ENGLISH} "C:\Program Files (x86)\OpenHRIVoice\3rdparty\MMDAgent_Example-1.0\Voice\mei_normal\COPYRIGHT.txt"
LicenseLangString MUILicense_Mei ${LANG_JAPANESE} "C:\Program Files (x86)\OpenHRIVoice\3rdparty\MMDAgent_Example-1.0\Voice\mei_normal\COPYRIGHT.txt"
LicenseLangString MUILicense_Festival ${LANG_ENGLISH} "C:\Program Files (x86)\OpenHRIVoice\3rdparty\festival-1.96.03-win\festival\COPYING"
LicenseLangString MUILicense_Festival ${LANG_JAPANESE} "C:\Program Files (x86)\OpenHRIVoice\3rdparty\festival-1.96.03-win\festival\COPYING"

;--------------------------------
;Reserve Files

;These files should be inserted before other files in the data block
;Keep these lines before any File command
;Only for solid compression (by default, solid compression is enabled for BZIP2 and LZMA)

!insertmacro MUI_RESERVEFILE_LANGDLL

!macro Download URL NAME
  IfFileExists "$INSTDIR\downloads\${NAME}" ${NAME}_found ${NAME}_notfound
    ${NAME}_found:
      Goto ${NAME}_end
    ${NAME}_notfound:
      IfFileExists "$EXEDIR\3rdparty\${NAME}" ${NAME}_local ${NAME}_remote
      ${NAME}_local:
        CopyFiles "$EXEDIR\3rdparty\${NAME}" "$INSTDIR\downloads"
        Goto ${NAME}_end
      ${NAME}_remote:
        NSISdl::download "${URL}" "$INSTDIR\downloads\${NAME}"
        Goto ${NAME}_end
  ${NAME}_end:
!macroend

;--------------------------------
;Installer Sections

Section $(TEXT_SecBase) SecBase

  SetOutPath "$INSTDIR"

  !insertmacro UNINSTALL.LOG_OPEN_INSTALL

  ; Main executables
  File "/oname=juliusrtc.exe" "${TOP_BUILDDIR}\dist\JuliusRTC.exe"
  File "/oname=openjtalkrtc.exe" "${TOP_BUILDDIR}\dist\OpenJTalkRTC.exe"
  File "/oname=festivalrtc.exe" "${TOP_BUILDDIR}\dist\FestivalRTC.exe"
  File "/oname=combineresultsrtc.exe" "${TOP_BUILDDIR}\dist\CombineResultsRTC.exe"
  File "/oname=xsltrtc.exe" "${TOP_BUILDDIR}\dist\XSLTRTC.exe"
  File "${TOP_BUILDDIR}\dist\srgstopls.exe"
  File "${TOP_BUILDDIR}\dist\validatesrgs.exe"
  File "${TOP_BUILDDIR}\dist\srgseditor.exe"
  File "${TOP_BUILDDIR}\dist\w9xpopen.exe"
  File "${TOP_BUILDDIR}\dist\dot.exe"
  File "${TOP_BUILDDIR}\dist\config6"
  File "rtc.conf"
  File "${TOP_SRCDIR}\openhrivoice\dummy.dfa"
  File "${TOP_SRCDIR}\openhrivoice\dummy.dict"
  File "${TOP_SRCDIR}\openhrivoice\dummy-en.dfa"
  File "${TOP_SRCDIR}\openhrivoice\dummy-en.dict"
  File "${TOP_SRCDIR}\openhrivoice\xml.xsd"
  File "${TOP_SRCDIR}\openhrivoice\grammar.xsd"
  File "${TOP_SRCDIR}\openhrivoice\grammar-core.xsd"
  File "${TOP_SRCDIR}\openhrivoice\pls.xsd"
  File "${TOP_SRCDIR}\pkg\nsis\open_jtalk.exe"
  File "${TOP_SRCDIR}\pkg\nsis\License-Open_JTalk.txt"
  File "vcredist_x86.exe"

  ; Required Libralies
  File /r "${TOP_BUILDDIR}\dist\*.pyd"
  File /r "${TOP_BUILDDIR}\dist\*.dll"
  File "${TOP_BUILDDIR}\dist\library.zip"
  File /r "${TOP_BUILDDIR}\dist\share"
  File /r "${TOP_BUILDDIR}\dist\etc"

  ; Information/documentation files
;  File "/oname=ChangeLog.txt" "${TOP_SRCDIR}\ChangeLog"
  File "/oname=Authors.txt" "${TOP_SRCDIR}\AUTHORS"
  File "/oname=License.txt" "${TOP_SRCDIR}\COPYING"

  !insertmacro UNINSTALL.LOG_CLOSE_INSTALL

  ; tcl files
  ;File /r "${TOP_BUILDDIR}\dist\tcl"

  ;Store installation folder
  WriteRegStr HKLM "Software\${PACKAGE_NAME}" "" $INSTDIR

  ; Write the Windows-uninstall keys
  WriteRegStr ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "DisplayName" "${PACKAGE_NAME}"
  WriteRegStr ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "DisplayVersion" "${PACKAGE_VERSION}"
  WriteRegStr ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "Publisher" "AIST-OpenHRI Project"
  WriteRegStr ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "InstallDir" "$INSTDIR"
  WriteRegStr ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PACKAGE_NAME}" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PACKAGE_NAME}" "NoRepair" 1

  ;Create uninstaller
  WriteUninstaller "$INSTDIR\uninstall.exe"

  ;Create shortcuts
  CreateDirectory "${SCDIR}"
  CreateShortCut "${SCDIR}\Uninstall Voice Components.lnk" "$INSTDIR\uninstall.exe"
  CreateShortCut "${SCDIR}\juliusrtc.lnk" "$INSTDIR\juliusrtc.exe" "--gui"
  CreateShortCut "${SCDIR}\srgstopls.lnk" "$INSTDIR\srgstopls.exe" "--gui"
  CreateShortCut "${SCDIR}\validatesrgs.lnk" "$INSTDIR\validatesrgs.exe" "--gui"
  CreateShortCut "${SCDIR}\openjtalkrtc.lnk" "$INSTDIR\openjtalkrtc.exe"
  CreateShortCut "${SCDIR}\festivalrtc.lnk" "$INSTDIR\festivalrtc.exe"
  CreateShortCut "${SCDIR}\combineresultsrtc.lnk" "$INSTDIR\combineresultsrtc.exe"
  CreateShortCut "${SCDIR}\xsltrtc.lnk" "$INSTDIR\xsltrtc.exe" "--gui"
  CreateShortCut "${SCDIR}\srgseditor.lnk" "$INSTDIR\srgseditor.exe"

  ; download external data
  IfFileExists "$INSTDIR\downloads" +2
    CreateDirectory "$INSTDIR\downloads"

  ; sox sound exchange
  !insertmacro Download "http://prdownloads.sourceforge.net/sox/sox-14.3.2-win32.zip" "sox-14.3.2-win32.zip"
  ZipDLL::extractall "$INSTDIR\downloads\sox-14.3.2-win32.zip" "$INSTDIR\3rdparty"

  ; julius for windows and acoustic model for japansese
  ;!insertmacro Download "http://prdownloads.sourceforge.jp/julius/44943/dictation-kit-v4.0-win.zip" "julius-dictation-kit-v4.0-win.zip"
  !insertmacro Download "http://sourceforge.jp/frs/redir.php?m=iij&f=%2Fjulius%2F44943%2Fdictation-kit-v4.0-win.zip" "julius-dictation-kit-v4.0-win.zip"
  ZipDLL::extractall "$INSTDIR\downloads\julius-dictation-kit-v4.0-win.zip" "$INSTDIR\3rdparty"

  ; julius acoustic model for english
  !insertmacro Download "http://www.repository.voxforge1.org/downloads/Main/Tags/Releases/0_1_1-build726/Julius_AcousticModels_16kHz-16bit_MFCC_O_D_(0_1_1-build726).zip" "julius-voxforge-build726.zip"
  ZipDLL::extractall "$INSTDIR\downloads\julius-voxforge-build726.zip" "$INSTDIR\3rdparty\julius-voxforge-build726"

  ; Open JTalk dictionary
  !insertmacro Download "http://prdownloads.sourceforge.net/open-jtalk/open_jtalk_dic_utf_8-1.04.tar.gz"  "open_jtalk_dic_utf_8-1.04.tar.gz"
  untgz::extract -d "$INSTDIR\3rdparty" "$INSTDIR\downloads\open_jtalk_dic_utf_8-1.04.tar.gz"

  ; Open JTalk acoustic model
  !insertmacro Download "http://prdownloads.sourceforge.net/open-jtalk/hts_voice_nitech_jp_atr503_m001-1.04.tar.gz"  "hts_voice_nitech_jp_atr503_m001-1.04.tar.gz"
  untgz::extract -d "$INSTDIR\3rdparty" "$INSTDIR\downloads\hts_voice_nitech_jp_atr503_m001-1.04.tar.gz"

  ; MMDAgent model file
  !insertmacro Download "http://prdownloads.sourceforge.net/mmdagent/MMDAgent_Example-1.0.zip"  "MMDAgent_Example-1.0.zip"
  ZipDLL::extractall "$INSTDIR\downloads\MMDAgent_Example-1.0.zip" "$INSTDIR\3rdparty"

  ; Festival
  !insertmacro Download "http://prdownloads.sourceforge.net/e-guidedog/festival-1.96.03-win.zip"  "festival-1.96.03-win.zip"
  ZipDLL::extractall "$INSTDIR\downloads\festival-1.96.03-win.zip" "$INSTDIR\3rdparty\festival-1.96.03-win"

  ClearErrors
  ReadRegDword $R0 HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{FF66E9F6-83E7-3A3E-AF14-8DE9A809A6A4}" "Version"
  IfErrors 0 VSRedistInstalled
    ExecWait '"$INSTDIR\vcredist_x86.exe" /q:a /c:"VCREDI~1.EXE /q:a /c:""msiexec /i vcredist.msi /qb!"" "'
  VSRedistInstalled:

SectionEnd

;--------------------------------
;Installer Functions

Function .onInit
  !insertmacro MUI_LANGDLL_DISPLAY
  !insertmacro UNINSTALL.LOG_PREPARE_INSTALL
FunctionEnd

Function .onInstSuccess
  !insertmacro UNINSTALL.LOG_UPDATE_INSTALL
FunctionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString TEXT_SecBase ${LANG_ENGLISH} "Standard installation."
  LangString DESC_SecBase ${LANG_ENGLISH} "Standard installation."
 
  LangString TEXT_SecBase ${LANG_JAPANESE} "Standard installation"
  LangString DESC_SecBase ${LANG_JAPANESE} "Standard installation"
 
  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecBase} $(DESC_SecBase)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END


;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;!insertmacro UNINSTALL.LOG_BEGIN_UNINSTALL
  !insertmacro UNINSTALL.LOG_UNINSTALL "$INSTDIR"
  !insertmacro UNINSTALL.LOG_END_UNINSTALL

  RMDir /r "$INSTDIR\tcl"
  RMDir /r "$INSTDIR\3rdparty"

  Delete "$INSTDIR\uninstall.exe"

  Delete "${SCDIR}\Uninstall Voice Components.lnk"
  Delete "${SCDIR}\juliusrtc.lnk"
  Delete "${SCDIR}\srgstopls.lnk"
  Delete "${SCDIR}\validatesrgs.lnk"
  Delete "${SCDIR}\openjtalkrtc.lnk"
  Delete "${SCDIR}\festivalrtc.lnk"
  Delete "${SCDIR}\combineresultsrtc.lnk"
  Delete "${SCDIR}\xsltrtc.lnk"
  Delete "${SCDIR}\srgseditor.lnk"
  RMDir "${SCDIR}"

  DeleteRegKey /ifempty ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}"

  ; Unregister with Windows' uninstall system
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PACKAGE_NAME}"

SectionEnd

;--------------------------------
;Uninstaller Functions

Function un.onInit
  !insertmacro MUI_UNGETLANGUAGE
  !insertmacro UNINSTALL.LOG_BEGIN_UNINSTALL
FunctionEnd
