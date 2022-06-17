# Script get images google

This script let to download a images group about theme of google.

## Installing

```bash
pip install -r requirements.txt
```

## Using

```bash
python main.py -p "url google images" -d "path willsave images" -s "text list to search" -l "limit images" -c
```

### Parameters

| Parameter                 | Description                                                    |
| ------------------------- | -------------------------------------------------------------- |
| -page, -p                 | url of google images\*                                         |
| -path_saved, -d           | path where save the searched images                            |
| -list_searching_texts, -s | texts list what will be search in google images                |
| -limit, -l                | limit download images, default=0                               |
| -copyright, -c            | with this option the images could have copyright, default=True |

\* To use this url https://www.google.com.co/imghp?hl=es-419&authuser=0&ogbl

### Example

```bash
python main.py -p "https://www.google.com.co/imghp?hl=es-419&authuser=0&ogbl" -d ./images -s "conflicto armado en colombia" -l 5
```
