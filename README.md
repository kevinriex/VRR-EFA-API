# VRR EFA API Abfragen

Mit diesem Commandline Tool kann man die Abfahrten jeder VRR Haltestelle in der Komandozeile auslesen.

Hierzu einfach in Zeile 53 der evavrr.py die Haltestelle eintragen.

## Syntax:
```python
departures = await EFA("https://efa.vrr.de/standard/").get_departures(
    "{STADTNAME}", "{HALTESTELLEN NAME}", now
    )
```   

## Beispiel:
```python
departures = await EFA("https://efa.vrr.de/standard/").get_departures(
    "Ratingen", "Mitte", now
    )
```  

## Output:
![Output Beispiel](https://kevinriex.de/ZAVAs)