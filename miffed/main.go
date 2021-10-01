package main

import (
	"flag"
	"fmt"
	"log"
	"os"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

func parseColor(v string) string {
	if len(v) == 6 {
		return v
	}
	if len(v) == 3 {
		return fmt.Sprintf("%c%c%c%c%c%c", v[0], v[0], v[1], v[1], v[2], v[2])
	}
	fmt.Println("cannot handle color: ", v)
	os.Exit(1)
	return ""
}

func main() {

	var port = flag.Int("p", 1883, "broker port")
	var host = flag.String("h", "192.168.86.98", "broker host")

	flag.Parse()

	values := flag.Args()
	if len(values) != 1 {
		fmt.Println("Usage: color")
		flag.PrintDefaults()
		os.Exit(1)
	}
	color := parseColor(values[0])
	fmt.Println(color)

	mqtt.ERROR = log.New(os.Stdout, "[ERROR] ", 0)
	mqtt.CRITICAL = log.New(os.Stdout, "[CRIT] ", 0)

	opts := mqtt.NewClientOptions()
	opts.AddBroker(fmt.Sprintf("tcp://%s:%d", *host, *port))

	client := mqtt.NewClient(opts)

	if token := client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}

	token := client.Publish("miffy", 0, false, color)
	token.Wait()

	client.Disconnect(250)
}
