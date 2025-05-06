define \n


endef

WAV = $(wildcard *.wav)
WAVX = $(WAV:%=%|)

start :
	python run.py

startx : start1
	make conv

conv :
	ffmpeg -i "concat:$(WAVX)" -c copy output.wav
	echo ffmpeg -i output.wav -o output.mp3


nothing :
	echo $(WAVX)


