package main

import (
	"bufio"
	"flag"
	"fmt"
	"net"
	"os"
	"strings"
)

func main() {
    host := flag.String("host", "0.0.0.0", "Host to connect to")
    port := flag.String("port", "4444", "Port to connect on")

    client(*host, *port)
}

func client(host, port string) {
    // create a socket connection
    connection, err := net.Dial("tcp", host + ":" + port)
    if err != nil {
        panic(err)
    }
    defer connection.Close()

    fmt.Println("Connected to remote host " + host + " on port " + port)
    fmt.Println("Enter 'quit', 'exit', or 'q' to disconnect")

    // create reader for input
    reader := bufio.NewReader(os.Stdin)

    for {
        fmt.Print(">>> ")
        message, _ := reader.ReadString('\n')
        message = strings.Replace(message, "\n", "", -1)

        if message == "quit" || message == "exit" || message == "q" {
            break
        } 

        if len(message) > 0 {
            connection.Write([]byte(message))

            response := make([]byte, 4096)
            responseLen, err := connection.Read(response)
            if err != nil {
                fmt.Println("Error reading response:", err.Error())
            }

            fmt.Print(string(response[:responseLen]))
        }
    }
}
