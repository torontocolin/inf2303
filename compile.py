
import markdown
import codecs
import yaml

sections = ["intro", "evaluation", "readings", "schedule", "procedures"]

buffer = codecs.open("header.html", "r", encoding="utf8").read()

table_row_template = """
 <tr>
  <td width="35%%"><b>%s:</b></td> 
  <td width="65%%">%s</td>
 </tr>
"""

type2marker = {
  "inforum" : "Inforum",
  "electronic" : "Online",
  "reserve" : "Reserve"
}

def format_availability(resource) :

  if resource.has_key("bitly") :
    link = "<a href='%s'>%s</a>" % (resource["url"], resource["bitly"])
  elif resource.has_key("url") :
    link = "<a href='%s'>%s</a>" % (resource["url"], resource["url"])
  else :
    link = None

  marker = "<span class='%s'>%s</span>" % (resource["type"], type2marker[resource["type"]])

  if link :
    return marker + ": " + link
  else : 
    return marker

for section in sections :

  buffer += "<div class='box' id='%s'>" % section
  
  if section=="schedule" :
    buffer += "<h1>Schedule</h1>"
    yamlsource = codecs.open("schedule.yaml", "r", encoding="utf8").read()
    schedule = yaml.load(yamlsource)
    md_buffer = ""
    for week in schedule :
      md_buffer += "\n\n## Week %s\n\n" % (week["week"])

      for klass in week["classes"] :      
        #print klass["date"]
      
        if klass.has_key("no_class") :
          md_buffer += "\n\n### <span class='no_class'>%s, 2013<br/>No Class: %s</span>\n\n" % (klass["date"], klass["no_class"].strip())
      
        else :
          md_buffer += "\n\n### %s, 2013<br/>%s\n\n" % (klass["date"], klass["title"].strip())
          if klass.has_key("summary") :
            md_buffer += "\n\n" + klass["summary"] + "\n\n"
        
        if klass.has_key("due") :
          md_buffer += "\n\n" + klass["due"] + "\n\n"
          
        if klass.has_key("readings") :
          md_buffer += "\n\n"
          for reading in klass["readings"] :
            md_buffer += "* " + reading["bib"].strip()
            if reading.has_key("availability") :
              md_buffer += " " + (", ".join([format_availability(x) for x in reading["availability"]]))
            md_buffer += "\n"

          md_buffer += "\n\n"

    buffer += markdown.markdown(md_buffer)
  else :
    source = codecs.open(section +".markdown", "r", encoding="utf8").read()
    if section=="intro" :
      yamlsource = codecs.open("intro.yaml", "r", encoding="utf8").read()
      yamldoc = yaml.load(yamlsource)
      table = ""
      for item in yamldoc["intro_table"] :
        table += table_row_template % (item["field"], item["value"])
      source = source % table
  
    html = markdown.markdown(source)
    buffer += html
  buffer += "</div>"
    
buffer += """
<div class="box" id="footer" markdown="1">
<br/>
<a href="http://validator.w3.org/check?uri=referer"><img style="border:none" src="http://www.w3.org/Icons/valid-xhtml10-blue" alt="Valid XHTML 1.0 Transitional" height="31" width="88" /></a>
</div>
"""
    
print codecs.encode(buffer, "utf8")

