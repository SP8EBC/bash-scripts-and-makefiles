SRCS := $(wildcard ./*.MP4)
TARGETS := $(notdir $(SRCS:.MP4=.RAW.H264))

show:
	@echo "list of input files"
	@echo $(SRCS)
	@echo "intermediate files"
	@echo $(TARGETS)

25fps: $(TARGETS)

%.RAW.H264: %.MP4
	ffmpeg -i "$<" -map 0:v -c:v copy -bsf:v h264_mp4toannexb "$@"
	ffmpeg -fflags +genpts -r 25 -i "$@" -c:v copy $(addprefix 25FPS_,"$<")
	rm -f *.RAW.H264

clean:
	rm -f *.RAW.H264
	rm -f 25FPS_*