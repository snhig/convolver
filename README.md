# convolver
This is a mini Python applicaiton that takes an Impulse response .wav and a input .wav to demonstrate audio convolution. A tool used in audio and signal processing. 

Created by Sean Higley snhigley@gmail.com
Inspired by Dan Price's video on [Spring Reverb Analysis and Synthesization](https://www.youtube.com/watch?v=q63ypxds0cY) 


## What is Reverb Convolution

_"A convolution reverb takes an input signal (the sound to be reverberated) and processes it with the sound of an actual or virtual acoustic space to create the illusion that the input was recorded in that space. The sound of the acoustic space is captured in what is called an impulse response (IR), which often starts as a recording of a short, sharp sound, such as the firing of a starter pistol or the bursting of an inflated balloon (the impulse), in the acoustic space in question."_
from [Ask.Audio "What is Convolution Reverb?"](https://ask.audio/articles/what-is-convolution-reverb)

IMPORTANT LIBRARIES:
	-	numpy
	-	matplotlib
	-	scipy
	-   PySide6
	-   pyqtgraph

Running from the command line:

	unix>>	python3 convolver.py <impulse repsonse .wav> <input file .wav> <output file .wav> 
	
	*Optional		-p		flag at the end to plot spectrograms
	
Using the sample files:
	unix>>	python3 convolver.py ir.wav test_in.wav test_out.wav -p
	
NOTABLE ISSUES:
	If the program throws errors about Chunk Issues regarding no data, it is likely that the audio files you used have extra metadata or tags within them. I suggest removing all metadata/tags so that the output files are not silent. 
