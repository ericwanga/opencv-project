@echo off

cls

::set VID_SOURCE=rtsp://192.168.0.80:9000/live
set VID_SOURCE=%1

REM	date format subject to your system setting. Below string slicing is based on DD/MM/YYYY format 
set CUR_YYYY=%date:~-4%
set CUR_MM=%date:~7,2%
set CUR_DD=%date:~4,2%
set CUR_HH=%time:~0,2%
if %CUR_HH% lss 10 (set CUR_HH=0%time:~1,1%)
echo Current date %date%
::echo %CUR_YYYY%
::echo %CUR_MM%
::echo %CUR_DD%

set CUR_NN=%time:~3,2%
::set CUR_SS=%time:~6,2%
::set CUR_MS=%time:~9,2%

set SUBFILENAME=videoall_%CUR_YYYY%%CUR_MM%%CUR_DD%_%CUR_HH%%CUR_NN%
set outputpath=%2_video
mkdir %OUTPUTPATH%

::set VIDEO_OPTS=-f mpegts -b 400k -r 25 -vcodec libx264 -s 640x480 -aspect 4:3 -b:v 2000k -bufsize 6000k
set VIDEO_OPTS=-f mpegts -b:v 400k -r 25 -vcodec libx264 -s 1280x960 -aspect 4:3 -bufsize 6000k
::set AUDIO_OPTS=-acodec aac -ab 128k -ac 2 -ar 22050 -bf 0 -level 30
set AUDIO_OPTS=-af asetrate=48000 -acodec aac -b:a 96k -ac 1


set OUTPUT_FILE=%3.ts
::set OUTPUT_FILE=%3.mp4

:: -use_wallclock_as_timestamps 1
ffmpeg -use_wallclock_as_timestamps 1 -rtsp_transport tcp -i %VID_SOURCE% %VIDEO_OPTS% %AUDIO_OPTS% -y %outputpath%\%OUTPUT_FILE%
