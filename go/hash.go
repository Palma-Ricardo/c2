package main

import (
	// "crypto/sha256"
	"fmt"

	"golang.org/x/crypto/bcrypt"
)

func main() {
	str := "qwerty"

	h, _ := bcrypt.GenerateFromPassword([]byte(str), 6)

	fmt.Println(string(h))
}
