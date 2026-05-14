package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

type Data struct {
	DriverID string  `json:"driver_id"`
	Lat      float64 `json:"lat"`
	Lon      float64 `json:"lon"`
}

func update(w http.ResponseWriter, r *http.Request) {
	var d Data
	json.NewDecoder(r.Body).Decode(&d)

	fmt.Println("Driver:", d.DriverID, "Lat:", d.Lat, "Lon:", d.Lon)

	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(`{"status":"location received"}`))
}

func health(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Location service running"))
}

func main() {
	http.HandleFunc("/update", update)
	http.HandleFunc("/health", health)

	fmt.Println("Running on 3003")
	http.ListenAndServe(":3003", nil)
}