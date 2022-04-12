
:: mocap_clipper is determined by the current folder name
for %%I in (.) do set mocap_clipper=%%~nxI
SET CLEAN_mocap_clipper=%mocap_clipper:-=_%

:: Check if modules folder exists
if not exist %UserProfile%\Documents\maya\modules mkdir %UserProfile%\Documents\maya\modules

:: Delete .mod file if it already exists
if exist %UserProfile%\Documents\maya\modules\%mocap_clipper%.mod del %UserProfile%\Documents\maya\modules\%mocap_clipper%.mod

:: Create file with contents in users maya/modules folder
(echo|set /p=+ %mocap_clipper% 1.0 %CD%\_setup_\maya & echo; & echo icons: ..\%CLEAN_mocap_clipper%\icons)>%UserProfile%\Documents\maya\modules\%mocap_clipper%.mod

:: end print
echo .mod file created at %UserProfile%\Documents\maya\modules\%mocap_clipper%.mod



