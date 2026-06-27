run: build_algocl
		cat 0 | ./a.exe

build_algocl: 
		gcc -oa.exe -std=c99 ./algo.c

build_algogo:
		cat 0 | go run ./algo.go

build_algocpp_seam:
	g++ -o a.exe ./sema.cpp -Wall -std=c++20

build_algocc:
	 g++ -o a.exe ./algo.cc -Wall -std=c++20
	
build_algojava:
	javac Algo.java && java Algo.class
	
build_fibanocci_heap:
	gcc ./fibanocci_heap.c -std=c99


build_build_keyrecorder: keyrecorder
	cat 0 | ./app.exe
	
build_keyrecorder:
	g++ -oapp -m64 keyrecorder.cpp


build_pixel:
	g++ -opixel -I C:///Users/zqshe/olcPixelGameEngine/  pixel.cpp


build_geometry:
	g++ -ogeometry -I C:///Users/zqshe/olcUTIL_Geometry2D/ geometry.cpp


build_binary_indexed_tree:
	gcc ./binary_indexed_tree.c


clean:
	rm a.exe


