# CronoTermoPi
Comandare e programmare caldaia e splitter con RaspberryPi
Programma per la gestione di un impianto di riscaldamento e di condizionamento 
con monitoraggio e gestione via Blynk su Android.
Il programma è sviluppato principalmente per esigenze personali per una villa al
mare. D'inverno deve accendere la caldaia e riscaldare la casa, e, all'occorrenza, 
accendere il deumidificatore, per un paio di ore a settimana, e devo poter 
comandarne l'accensione quando decido di andare nel w.e.. Inizialmente questi 
parametri verranno inseriti nel codice, prevedendo poi di spostarli su file o 
database. Cercherò di tenere presente una programmazione quanto piu flessibile
possibile

  Downloads, docs, tutorials: https://github.com/Mas7ro/CronoTermoPi

Considero due macrovariabili, Stagione e Stato. La stagione è intendo o estiva
o invernale, lo Stato sarà On oppure Off. D'inverno se lo Stato è On accende il
riscaldamento e porta la casa a Tmax, se invece Stato è Off accenderà la caldaia
solo se la temperatura scende sotto Tmin.
Questa è la parte che piu mi interessa e parto con lo sviluppo di questa.
