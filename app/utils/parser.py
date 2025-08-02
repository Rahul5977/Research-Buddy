# To parse the document ->grobid 
from grobid_client.grobid_client import GrobidClient
import xml.etree.ElementTree as ET

def parse_pdf_with_grobid(pdf_path):
   # parse pdf with local grobid server
   print("Connecting to local grobid server->pdf_path :{pdf_path}")
   client = GrobidClient(config_path="./config.json")
   # process the document to get the TEI XML response 
   status,text=client.process(
      "processFulltextDocument",
      pdf_path,
      generateIDs=True,
      consolidate_header=True
   )
   if status!=200:
      error_message=f"Failed to process document, Status {status}, Text {text}"
      print(error_message)
      raise RuntimeError(error_message)
   
   # Parse the XML string to an XML element tree
   root=ET.fromstring(text)
   # Define the XML namespace used by TEI (this is standard)
   ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
   # Find the paper title
   title_element = root.find('.//tei:titleStmt/tei:title', ns)
   title = title_element.text if title_element is not None else "Title Not Found"

    # Find the abstract paragraph
   abstract_element = root.find('.//tei:abstract//tei:p', ns)
   abstract = abstract_element.text if abstract_element is not None else "Abstract Not Found"

   # Find all paragraphs from the main body of the text
   body_paragraphs = root.findall('.//tei:body//tei:p', ns)
   full_text_body = "\n\n".join([para.text for para in body_paragraphs if para.text])

   # Combine abstract and body for a complete text representation
   full_text = abstract + "\n\n" + full_text_body
   print("GROBID parsing success")
   return {
      "title":title,
      "abstract":abstract,
      "full_text":full_text
   }
    
   
