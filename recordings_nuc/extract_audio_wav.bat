@echo off

REM	date format subject to your system setting. Below string slicing is based on DD/MM/YYYY format 
set CUR_YYYY=%date:~-4%
set CUR_MM=%date:~7,2%
set CUR_DD=%date:~4,2%
set CUR_HH=%time:~0,2%
if %CUR_HH% lss 10 (set CUR_HH=0%time:~1,1%)

set CUR_NN=%time:~3,2%
::set CUR_SS=%time:~6,2%
::set CUR_MS=%time:~9,2%

set SUBFILENAME=frames_%CUR_YYYY%%CUR_MM%%CUR_DD%_%CUR_HH%%CUR_NN%
set outputpath=%2_audio
mkdir %outputpath%

::set VID_SOURCE=rtsp://192.168.0.80:9000/live
set VIDEO_OPTS=-vn
set AUDIO_OPTS_WAV=-acodec pcm_s16le -ac 1 -ar 44100
set OUTPUT_FILE=%3.wav

ffmpeg -i %1 -y %AUDIO_OPTS_WAV% %VIDEO_OPTS% %outputpath%\%OUTPUT_FILE%