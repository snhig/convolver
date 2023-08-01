# convolver
Python script that takes an Impulse response .wav and a input .wav to demonstrate audio convolution. 

Created by Sean Higley snhigley@gmail.com
Inspired by Dan Price's video on Spring Reverb Analysis and Synthesization 

IMPORTANT LIBRARIES:
	-	numpy
	-	matplotlib
	-	scipy

Running from the command line:

	unix>>	python3 convolver.py <impulse repsonse .wav> <input file .wav> <output file .wav> 
	
	*Optional		-p		flag at the end to plot spectrograms
	
Using the sample files:
	unix>>	python3 convolver.py ir.wav test_in.wav test_out.wav -p
	
NOTABLE ISSUES:
	If the program throws errors about Chunk Issues regarding no data, it is likely that the audio files you used have extra metadata or tags within them. I suggest removing all metadata/tags so that the output files are not silent. 
