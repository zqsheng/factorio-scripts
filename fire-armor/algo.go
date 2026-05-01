package main

import (
	"fmt"
)

func solve() {
	var n = 0
	for { 
		_, err := fmt.Scanf("%d", &n)
		if err == nil { break }
	}
	fmt.Println(n-1)
}


func main() {
	tt := 0
	fmt.Scanf("%d", &tt)
	for tt > 0 {
		tt--
		solve()
	}
	
}


