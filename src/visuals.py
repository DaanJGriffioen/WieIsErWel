from parse import arrayParsing

# Make nice graph who is present and who is not
def makeHTML(aanwezig, afwezig, datums):
    presentie = arrayParsing(aanwezig, afwezig)
    
    presentie["counts"] = presentie["afwezig"].value_counts()
    f = open("table.html", "w")
    f.write("<!DOCTYPE html>\n<html>\n<head>\n<link rel=\"stylesheet\" href=\"style.css\">\n<script type=\"text/javascript\" src=\"site.js\"></script>\n</head>\n<body>")
    f.write("<h1>Kamerleden Afwezigheid</h1>\n")
    f.write(f"<h2>Afwezigheid van {datums[0]} tot {datums[1]}</h2>")
    f.write("<table id=\"data-table\">")
    f.write("</body>\n<thead>\n<th>Naam</th>\n<th>Aanwezig aantal</th>\n<th>Afwezig aantal</th>\n</thead>\n<tbody>\n</tbody>\n</table>\n")
    f.write(f"<script>table(['{datums[0]}','{datums[1]}']);</script>")
    f.write("</body>")

