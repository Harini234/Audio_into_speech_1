import inflect
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import yake

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# p=inflect.engine()
kw_extractor = yake.KeywordExtractor(lan="en",n=1,dedupLim=0.9,top=10)
backend_sentence="I want to buy five shares of google at price ten dollar."

class InputData(BaseModel):
      order_type:str
      quantity:str
      symbol:str
      Transcribed_text:str

@app.post("/validate_input/")
def validate_input(data:InputData):
      backend_sentence = data.Transcribed_text
      extracted_keywords=kw_extractor.extract_keywords(backend_sentence)
      print(data.Transcribed_text)
      extracted_keywords=[word for word,_ in extracted_keywords]
      print("Extracted words:",extracted_keywords)

      # quantity_in_words = p.number_to_words(data.quantity).lower()
      json_values={"Order_Type":data.order_type.lower(),
                   "Quantity":data.quantity,
                   "Symbol":data.symbol.lower()
                  }
      
      mismatched_data=[]
      for key,value in json_values.items():
            if value not in backend_sentence.lower():
                 mismatched_data.append({"status":f"{key}Mismatch","Mismatch_data":value})
      if mismatched_data:
          return {"status":"Mismatch found","mismatch_data":mismatched_data}   
      return{
            "status": "Match",
            "extracted_keywords":extracted_keywords
      }

    #   mismatched_words = [word for word in json_values if word not in backend_sentence.lower()]
    #   mismatched_data = []

    #   if data.order_type.lower() in mismatched_words:
    #         mismatched_data.append({"status":"Order_Type Mismatch","Mismatch data:":data.order_type})
    #   if data.quantity.lower() in mismatched_words:
    #         mismatched_data.append({"status":"Quantity Mismatch","Mismatch data:":data.quantity})
    #   if mismatched_data:
    #         return{"status":"Mismatch found","mismatched_data":mismatched_data}
    #   return{"status":"Match",
    #          "extracted_keywords":extracted_keywords}






