package main

import (
	"fmt"
	"math/rand"
	"time"
)

var NumElfos = 10 // coment
var Num_Renos = 9
var Min_elfos_ayuda = 3
var Min_renos_para_enganchar = 9

func SantaClaus(ElfoProblema chan bool, LiberarElfo chan bool, RenosRegresandeVacaciones chan bool, RenoListoSalir chan bool, santaEmpiezaSalir chan bool) {
	fmt.Println("Santa: Esta durmiendo")

	// No hay while en Go :) El proceso santa es infinito
	elvs := 0
	reinds := 0

	for {
		select {
		// Renos regresan de vacaciones
		case <-RenosRegresandeVacaciones:
			reinds++
			if reinds == Min_renos_para_enganchar {
				fmt.Println("Despierta a Santa el reno ", reinds)
				fmt.Println("Santa: Preparando Trineo")
				for i := 0; i < reinds; i++ {
					RenoListoSalir <- true
					<-santaEmpiezaSalir
				}
				fmt.Println("Santa: Hohoho! Hora de repartir regalos")
				reinds = 0
			}
		//Problema con elfos
		case <-ElfoProblema:
			elvs++
			if elvs == Min_elfos_ayuda {
				fmt.Println("Santa: Ayudando Elfos")
				for i := 0; i < elvs; i++ {
					LiberarElfo <- true
				}
				elvs = 0
			}
		}
	}

}

func Elve(num int, ElfoProblema chan bool, LiberarElfo chan bool) {

	fmt.Println("Esta listo para trabajar el elfo ", num)
	for true {
		NecesitaAyuda := rand.Int()%100 < 10
		if NecesitaAyuda {
			fmt.Println("Elfo ", num, " esta esperando la ayuda de Santa")

			//Escribir problema
			ElfoProblema <- true
			//Esperar que santa reaccione
			<-LiberarElfo
			fmt.Println("Elfo", num, "recibe ayuda de Santa")
		}
		fmt.Println("Elfo ", num, " esta trabajando")
		waitingtime := time.Duration(rand.Int()%5 + 2)
		time.Sleep(waitingtime * time.Second)
	}
}

func Reindeer(num int, RenosRegresandeVacaciones chan bool, RenoListoSalir chan bool, santaEmpiezaSalir chan bool) {

	fmt.Println("LLego de vacaciones el reno ", num)
	for true {
		// Prepara a los renos
		RenosRegresandeVacaciones <- true
		// Espera a que Santa se enganche
		<-RenoListoSalir
		// Dar la señal a santa de estar todos listos
		santaEmpiezaSalir <- true
		fmt.Println("Reno ", num, " esta siendo enganchado")
		// Ir de vacaciones
		time.Sleep(20 * time.Second)
	}
}

func main() {

	ElfoProblema := make(chan bool)
	LiberarElfo := make(chan bool)

	RenosRegresandeVacaciones := make(chan bool)
	RenoListoSalir := make(chan bool)

	santaEmpiezaSalir := make(chan bool)

	go SantaClaus(ElfoProblema, LiberarElfo, RenosRegresandeVacaciones, RenoListoSalir, santaEmpiezaSalir)

	for i := 1; i <= Num_Renos; i++ {
		go Reindeer(i, RenosRegresandeVacaciones, RenoListoSalir, santaEmpiezaSalir)
	}
	for i := 1; i <= NumElfos; i++ {
		go Elve(i, ElfoProblema, LiberarElfo)
	}

	// No termina el programa
	i := 0
	fmt.Scan(&i)
}
