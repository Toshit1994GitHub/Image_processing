
#%%
# Import useful library
import base64
import os
import pyodbc
from pdf2image import convert_from_path
from PIL import Image
from pyzbar.pyzbar import decode
from pdf2image.exceptions import (PDFInfoNotInstalledError,
                                  PDFPageCountError,
                                  PDFSyntaxError)
from flask import Flask
from flask import  request
from flask_restful import Api, Resource
import json
from functools import reduce
from base64 import b64decode
from flask_cors import CORS
import pandas as pd

#%%

app = Flask(__name__)
CORS(app)
# creating an API object
api = Api(app)

#%%
conn = pyodbc.connect(DRIVER='{SQL Server Native Client 11.0}',
                       SERVER='xyz',
                       UID ='xyz',
                       PWD ='xyz',
                       DATABASE='xyz',
                       Trusted_Connection='no')
cursor = conn.cursor() 
#%%
class E_Invoicing_pdf(Resource):
    def post(self):
        encoded = request.get_json()  # Get base64 data from API
        
        #Convert receive data in string 

        consume_by=encoded["ID"]
        session_id=encoded["Passward"]
        encoded_data=str(encoded["pdf_data"])
        data= pd.read_sql_query("select * from API_consume_log_ID_Password where UserID='"+consume_by+"' and User_Password='"+session_id+"'",conn)
        if (data.index) >=0:
            ID=data.iat[0,0]
            Passward=data.iat[0,1]
            #if consume_by == "Admin" and session_id == "pass@1234":
            if consume_by == ID and session_id ==Passward:
                cut=encoded_data[0:]
                #print(cut)
                b=cut[2:]
                c=b[:-2]
                b64=c  
                #print(b64)
                # Decode base64 data for save in pdf file
                bytes = b64decode(b64, validate=True)
                # Moreover, if you get Base64 from an untrusted source, you must sanitize the PDF contents
                if bytes[0:4] != b'%PDF':
                  raise ValueError('Missing the PDF file signature')
                # Write the PDF contents to a local file
                f = open('file.pdf', 'wb')
                f.write(bytes)
                f.close()
                #Read all pdf file and save as a Image
                #images=convert_from_path("D:\\Toshit SVN VScan Backup\\file.pdf") # Development Location
                images=convert_from_path("D:\\Webservices\\python_E_Invoicing_UAT\\file.pdf") # Server Location
        #%%        
                out_put=[]
                counts=-1
                for i, image in enumerate(images):
                    counts=counts+1
                    st=str(counts)
                    fname = "image" + str(i) + ".png"
                    image.save(fname, "PNG")   # image will be saved in virtual enviroment
                    # Reagd and decode image from virtual enviroment
                    #aa=("D:/Toshit SVN VScan Backup/image"+st+".png") # Far api input # Development Location
                    #aa=("C:/Users/toshit.maurya/image"+st+".png")  # Local input # Development Location
                    aa=("D:\\Webservices\\python_E_Invoicing_UAT\\image"+st+".png")  #server Location
                    
                    a=decode(Image.open(aa))  # Decode QR Code 
                    #print("a value",a)
                    if a !=[]:
                        #print(a)
                        if a!=[]:
                            out_put.append(a)
                        file = ("image"+st+".png")
                        # File location 
                        #location = "D:/Toshit SVN VScan Backup" # For API use Virtual environment  Development Location
                        location = "D:\\Webservices\\python_E_Invoicing_UAT" # Server Location
                        # Path 
                        path = os.path.join(location, file) 
                        os.remove(path)
                    else:
                        return (json.dumps('Uploaded file have no QR code. Please upload correct file !'),"Failure")
        #%%
                final_list = []
                #for sub_list in a[0]:
                for sub_list in a[0]:
                    #print(sub_list)
                    final_list.append(sub_list)
                s=final_list[0]
                sentence=str(s)
                #print(sentence)
                result_1 = sentence.index('.')+1
                #print("Substring '.':", result_1)
                # Delete all record before first dot(.) and save new value in result_2 variablesl
                result_2=sentence[result_1:]
                #print(result_2)
                # Find second dot(.) index number and store in resule_3 variable 
                result_3=result_2.index('.')
                #print(result_3)
                # Now delete all record of result_2 after second dot(.) index number and save all remaining records in result 
                result=result_2[:result_3]
                #print(result)
                results=result + "======"
                # Finally print useful data
                final_result=base64.b64decode(results)
                #print("Vivek\n",final_result)
                my_bytes_value=final_result
                out=str(my_bytes_value)
    #%%            
                if final_result !=0:
                    sql = "insert into API_consume_log(consume_by, session_id, output_data,input_data,is_mob_app) values (?, ?, ?, ?, ?)" # Save all record in data base
                    cursor.execute(sql, (consume_by, session_id, out,b64,0))
                    cursor.commit()
                
                #t=json.loads(my_bytes_value)
                #print("Toshit\n",t)
                return(json.loads(my_bytes_value),"Success")
        else:
            return("Please Enter Valid User ID And Password")
    
#%%

class Mobile_data_E_Invoicing_QR(Resource):
    @app.route("/")
    def post(self):
        Mobile_data = request.get_json()  # Get base64 data from API
        consume_by=Mobile_data["ID"]
        session_id=Mobile_data["Passward"]
        data= pd.read_sql_query("select * from API_consume_log_ID_Password where UserID='"+consume_by+"' and User_Password='"+session_id+"'",conn)
        if (data.index) >=0:
            ID=data.iat[0,0]
            Passward=data.iat[0,1]
            if consume_by == ID and session_id == Passward:
                #print("Mobile_data\n",Mobile_data)
                res = reduce(lambda key, val : key + str(val[0]) + str(val[1]), Mobile_data.items(), '') 
                # Remove some unwanted value
                cut=res[8:]
                #print(cut)
                b=cut[2:]
                c=b[:-2]
                Mobile_data_b64=c
                #Convert receive data in string 
                Mobile_data_result_1 = Mobile_data_b64.index('.')+1
                #print("Substring '.':", Mobile_data_result_1)
                # Delete all record before first dot(.) and save new value in result_2 variablesl
                Mobile_data_result_2=Mobile_data_b64[Mobile_data_result_1:]
                #print(Mobile_data_result_2)
                # Find second dot(.) index number and store in resule_3 variable 
                Mobile_data_result_3=Mobile_data_result_2.index('.')
                #print(Mobile_data_result_3)
                # Now delete all record of result_2 after second dot(.) index number and save all remaining records in result 
                Mobile_data_result=Mobile_data_result_2[:Mobile_data_result_3]
                #print("Mobile_data_result\n",Mobile_data_result)
                Mobile_data_results=Mobile_data_result + "======"
                # Finally print useful data
                Mobile_data_final_result=base64.b64decode(Mobile_data_results)
                #print(Mobile_data_final_result)
                out_mobile=str(Mobile_data_final_result)
                Mobile_data_my_bytes_value=Mobile_data_final_result
                if Mobile_data_final_result !=0:
                    sql = "insert into API_consume_log(consume_by, session_id, output_data,input_data,is_mob_app) values (?, ?, ?, ?, ?)"
                    cursor.execute(sql, (consume_by, session_id, out_mobile,Mobile_data_b64,1))
                    cursor.commit()
                t=json.loads(Mobile_data_my_bytes_value)
                #print(t)
                return(t)
        else:
            return("Please Enter Valid User ID And Password")
api.add_resource(E_Invoicing_pdf,'/E_Invoicing_pdf')
api.add_resource(Mobile_data_E_Invoicing_QR,'/Mobile_data_E_Invoicing_QR')

if __name__ == "__main__":
    app.run(port=5000, debug=True)

    
