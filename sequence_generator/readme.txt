This directory contains the details of rewriting the sequence generator
(Utility_VIs\sequence_writer)



ORGANIZATION
	global variables: 
	classes:  pulses

TODO
	V	generate single pulse
	V	Pulse class
	V	sweeps: amplitude, sin_quad, width, start_time, phase angle
	(double sweep?)
	V	SSM'
	V	Multiple channels (input 'ch3mark', etc)
	useful errors 
	add functionality to steps: two of (step_size, start, stop), number of steps (or list of steps)
		or delays
	GUI: show all waveforms in heat map, or emulate old sequence viewer
	check for readout ++ alazar
	better Pulse.copy()
	clarify ALL_channels matrix with class. Currently is all_channels[which_channel][ch or m1 or m2][step in sequence][which sample]  = 4x3x101x16000 matrix
		or a get_element function.
	Double check writing
	

	
TESTS:
	frequencies of SSM are correct (test that seq of 100MHz == ARB standard mode)
	sin should not change with sweep.

ERRORS TO HANDLE:
	writing past end of file (esp duration mistakes)
		(add feature: start,end,duration or any two; maybe include this as pre-function)


FUN FEATURES
	GUI
	dynamically calcute optimal length (easy to pass around?)
	Quasi measurements
	auto-generate readme's with copy of generating code pasted in