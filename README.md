# VRR EFA API Abfragen

Mit diesem Commandline Tool kann man die Abfahrten jeder VRR Haltestelle in der Komandozeile auslesen.


## Version 1.1

Nun ist es auch möglich via argv zu arbeiten

```bash
departures [Stadt] [Haltestelle]
```

## Version 1.0

Hierzu einfach in Zeile 53 der [evavrr.py](python/efavrr.py) die Haltestelle eintragen.

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