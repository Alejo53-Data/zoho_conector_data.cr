from flask import Flask, request
from src.zoho_connector.zcrmsdk_initializer import ZCRM_Initializer
from src.modules.General import *
import json
import pymssql
from src.modules.Invoice import *
from src.modules.CustomerPayments import *
from src.modules.Items import *
from src.modules.Expense import *
from  src.utils.BooksRecurringInvoices import BooksRecurringInvoices
from  src.utils.BooksInvoices import BooksInvoices
from  src.utils.BooksContacts import BooksContacts
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path as path
import requests

import csv
import time

#"approved,processed,create,pending"

app = Flask(__name__)

#Credenciasles DB
conn = pymssql.connect(server='192.168.81.191',
                       database='ADNPayV2',
                       user='sa',
                       password='7ssvwAvKVUYB6')



#Cronjob route, lista los un nuevo cliente tanto de ADNPay , como de vendors. que sean validos 
# y cumpla con los requisitos necesarios
@app.route('/w', methods=['GET'])
def sync_users():
    #Credenciales Outlook
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_username = 'pay@data.cr'
    smtp_password = 'zpmwjdjzcprhkyng'
    arr={}
    arr_lead={}
    arrpro={}
    cursor = conn.cursor()
    
    
    #Prueba Jose Hernandez
    
    #cursor.execute("SELECT TOP (1) [index],[coordinate],[name],[email],[phone],[id],[id_type],[type],[condominium],[ftth],[mobile],[province],[canton],[district],[address],[plan],[dates],[user_agent],[ip_address],[status],[reference],[create_time],[extra_iptv],[promcode],[crm_status],[telephony] as telephony_cus,[public_ip] as public_ip_cus,[promotion],[promotion_type],[promotion_date],[pay_type] FROM [ADNPayV2].[dbo].[Customer] where [index]=6848")
    cursor.execute("SELECT TOP (1) [index],[coordinate],[name],[email],[phone],[id],[id_type],[type],[condominium],[ftth],[mobile],[province],[canton],[district],[address],[plan],[dates],[user_agent],[ip_address],[status],[reference],[create_time],[extra_iptv],[promcode],[crm_status],[telephony] as telephony_cus,[public_ip] as public_ip_cus,[promotion],[promotion_type],[promotion_date],[pay_type] FROM [ADNPayV2].[dbo].[Customer] where status ='approved' and type = 'customer' and crm_status = '0'")
    result =cursor.fetchall()
    print("ARREGLO DATA: ", result)
    #Mete todo en un array
    for row in result:
        for i,k in zip(cursor.description,row):
            arr[i[0]]=k
    
    
    if len(result) > 0:
        print("Arreglo:",arr)
        plan=str(arr['plan'])
        index=str(arr['index'])
        
        #Consulta al servicio relacionado con el cliente
        cursor.execute("SELECT * FROM Service s where s.[index] ='"+plan+"' ")
        result =cursor.fetchall()
        for row in result:
            for i,k in zip(cursor.description,row):
                if(i[0]=='index' or i[0]=='name'):
                    None
                else:
                    arr[i[0]]=k
        zcrm=ZCRM_Initializer()
       
       #API tipo de cambio
        changeusd=requests.get("http://apis.gometa.org/tdc/tdc.json")
        if changeusd.status_code == 200:
            changeusd=changeusd.json()
            sell =changeusd["venta"]
            arr['exchange_rate']=sell
        else :
            print("Error API tipo de cambio")

        #MMain function
        res=zcrm.create_record_account(arr)
        #Test pruebas directas
        
        #namem="FTTHs"
        #nameaccm="ftth"
        #arr['idacc']=3413022000117265671
        #arr['namem']=namem
        #arr['nameaccm']=nameaccm
        #arr['idcont']=3413022000117265677
        #arr['circuito']='DAT-5450'
        #arr['coorda']=' 9.978952, -84.187725'
        #arr['idcon']=3413022000234045424
        
        #res=zcrm.create_feasibility_ftth(arr)
        #res= zcrm.create_record_contract(arr)
        print(res)
        #Update customer done
        cursor.execute("UPDATE [ADNPayV2].[dbo].[Customer] SET [crm_status] = '1' WHERE [index] = '"+index+"' ")
        conn.commit()
        idtask= res.get('idtask')
        nombret =res.get("name")
        
        #Mail notification when customer is vendors
        if res.get('ftth') is not None:
        
            # Crear objeto mensaje
            mensaje = MIMEMultipart()
            mensaje['From'] = smtp_username
            mensaje['To'] = 'dev@data.cr,fmarcias@data.cr'
            tituloh=f"Nuevo Cliente Vendor , Task Generated  {nombret}"
            mensaje['Subject'] = tituloh
            # Agregar cuerpo del mensaje
            cuerpo = MIMEText(f"""
            <!DOCTYPE html>
            <html>
            <table class="x_contentOuter" id="x_contentOuter" cellpadding="0" cellspacing="0" width="100%" style="width: 100%; border: 0px; font-family: Arial, Helvetica, sans-serif; color: rgb(245, 245, 245) !important; font-size: 13px; border-collapse: collapse; letter-spacing: normal; " data-ogsc="rgb(17, 17, 17)" data-ogsb="rgb(240, 240, 240)">
                <tbody    tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                    <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                        <td align="center" class="x_contentmaintd" style="border: 0px; padding-top: 10px; padding-bottom: 20px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                            <table class="x_contentInner" id="x_contentInner" cellpadding="0" cellspacing="0" width="600px" style="width: 600px; border: 0px; border-collapse: collapse; table-layout: fixed;  color: rgb(245, 245, 245) !important;" data-ogsc="" data-ogsb="rgb(255, 255, 255)">
                                <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                    <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                        <td valign="top" style="border: 0px; overflow-wrap: break-word; word-break: break-word; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                            <div class="x_zpcontent-wrapper" id="x_page-container" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                <table cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_spacebar" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="height: 20px; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <p style="height: 20px; margin: 0px; padding: 0px; color: rgb(245, 245, 245) !important;" data-ogsc=""></p>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_image" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="overflow-wrap: break-word; word-break: break-word; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; padding: 6px 16px; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <p style="float: none; text-align: center; padding: 0px; margin: 0px; color: rgb(245, 245, 245) !important;" data-ogsc=""><img data-imagetype="AttachmentByCid" originalsrc="cid:gg4lga0f9a1c1433a4aa1942207bdf4bd2e9a" data-custom="AAMkADNjY2U1MjNhLWYwNGEtNDc1NC1hMDAwLTc2ZGM1ODViOGIzNABGAAAAAACs5oio36XmQLxiKvkcV0xvBwCKIfefbn62SJRbzT3Y61iDAAAAAAEMAACKIfefbn62SJRbzT3Y61iDAAF4A4KpAAABEgAQAKecKpFrrX1Hp2J3QQX%2Bnxs%3D" naturalheight="0" naturalwidth="0" src="https://attachments.office.net/owa/luis.herrera%40data.cr/service.svc/s/GetAttachmentThumbnail?id=AAMkADNjY2U1MjNhLWYwNGEtNDc1NC1hMDAwLTc2ZGM1ODViOGIzNABGAAAAAACs5oio36XmQLxiKvkcV0xvBwCKIfefbn62SJRbzT3Y61iDAAAAAAEMAACKIfefbn62SJRbzT3Y61iDAAF4A4KpAAABEgAQAKecKpFrrX1Hp2J3QQX%2Bnxs%3D&amp;thumbnailType=2&amp;token=eyJhbGciOiJSUzI1NiIsImtpZCI6IjczRkI5QkJFRjYzNjc4RDRGN0U4NEI0NDBCQUJCMTJBMzM5RDlGOTgiLCJ0eXAiOiJKV1QiLCJ4NXQiOiJjX3VidnZZMmVOVDM2RXRFQzZ1eEtqT2RuNWcifQ.eyJvcmlnaW4iOiJodHRwczovL291dGxvb2sub2ZmaWNlLmNvbSIsInVjIjoiZWExZjNkNDYyMWE5NGE2ZjhmZTRjZDJjZjVlZjBmZjUiLCJzaWduaW5fc3RhdGUiOiJbXCJrbXNpXCJdIiwidmVyIjoiRXhjaGFuZ2UuQ2FsbGJhY2suVjEiLCJhcHBjdHhzZW5kZXIiOiJPd2FEb3dubG9hZEA1NzAxOTkzOS1iMDdiLTRkOTUtODIwMC0zMmJkMGNmOTVkYzgiLCJpc3NyaW5nIjoiV1ciLCJhcHBjdHgiOiJ7XCJtc2V4Y2hwcm90XCI6XCJvd2FcIixcInB1aWRcIjpcIjExNTM4MDExMjIxNDk1NDM0MjhcIixcInNjb3BlXCI6XCJPd2FEb3dubG9hZFwiLFwib2lkXCI6XCI4ZTE2ODkzNS1lOTYxLTQzYjEtOWEyNS00NGY4ODhjN2ExNDhcIixcInByaW1hcnlzaWRcIjpcIlMtMS01LTIxLTIxODEwMDUyNzgtMjMxMjA4MDg0Mi0xMzMzMTg0ODA3LTQ3NzY5ODMzXCJ9IiwibmJmIjoxNjk4MjcyNjMwLCJleHAiOjE2OTgyNzMyMzAsImlzcyI6IjAwMDAwMDAyLTAwMDAtMGZmMS1jZTAwLTAwMDAwMDAwMDAwMEA1NzAxOTkzOS1iMDdiLTRkOTUtODIwMC0zMmJkMGNmOTVkYzgiLCJhdWQiOiIwMDAwMDAwMi0wMDAwLTBmZjEtY2UwMC0wMDAwMDAwMDAwMDAvYXR0YWNobWVudHMub2ZmaWNlLm5ldEA1NzAxOTkzOS1iMDdiLTRkOTUtODIwMC0zMmJkMGNmOTVkYzgiLCJoYXBwIjoib3dhIn0.LrTwDlQt9xdxs8etzdofDrWk1EYth-rQTj1f0Nq4o3GYtzzVnPmUl4H8Up3-Pf6Dmvf1Fl0SzieuUIhqkzLavM77U_K09VeAYiLXutl_LKvfRB0CPIVj5AG4y4WBPqLkn0WKF--yXLo_vXqb5irk_vHhonasz8qzcjNHGx2v3lHAM896zqFw-w1ZHYk7Q8g9SantJv9jnrDeA6J49Dm7jlnoSrflPdoNdQHo14h2yPBqvMOsEbPCRFWwNIMW7ww8oSCMTzQOyKnHsP884PR6rXTgMaYCMrrm7k80D69rGX0iaAK03I6ZA3w6NMNkE3nIVRsWAOV8iOJcPiup--5gWQ&amp;X-OWA-CANARY=1ZxTa212yUO8vgbOqLlI8eBugRyp1dsYVda629n30Nf5QmFptyQr4jUi0_X9IHZIR5FCcHMB3YQ.&amp;owa=outlook.office.com&amp;scriptVer=20231013005.20&amp;animation=true" class="x_zpImage x_imgsize_F Do8Zj" alt="Company name" width="540" height="139.479" style="width: 100%; max-width: 100%; vertical-align: top; color: rgb(245, 245, 245) !important; min-height: auto; min-width: auto; cursor: pointer;" crossorigin="use-credentials" fetchpriority="high" data-ogsc=""></p>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_spacebar" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="height: 15px; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <p style="height: 15px; margin: 0px; padding: 0px; color: rgb(245, 245, 245) !important;" data-ogsc=""></p>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_spacebar" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="height: 30px; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <p style="height: 30px; margin: 0px; padding: 0px; color: rgb(245, 245, 245) !important;" data-ogsc=""></p>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_text" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="font-size: 13px; letter-spacing: normal; font-family: Arial, Helvetica, sans-serif; min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="overflow-wrap: break-word; word-break: break-word; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; padding: 6px 16px; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); font-family: Arial, Helvetica, sans-serif; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <div align="center" style="padding: 0px; margin: 0px; color: rgb(255, 255, 255) !important;" data-ogsc="rgb(0, 0, 0)"><font style="color: rgb(255, 255, 255) !important;" data-ogsc=""><font size="4" style="color: rgb(255, 255, 255) !important;" data-ogsc=""><b data-ogsc="" style="color:black !important;">Nuevo Cliente Generado ADNPAY</b></font><br style="" aria-hidden="true"></font></div>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_spacebar" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="height: 5px; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <p style="height: 5px; margin: 0px; padding: 0px; color: rgb(245, 245, 245) !important;" data-ogsc=""></p>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_text" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="font-size: 13px; letter-spacing: normal; font-family: Arial, Helvetica, sans-serif; min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="overflow-wrap: break-word; word-break: break-word; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; padding: 6px 16px; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); font-family: Arial, Helvetica, sans-serif; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <div align="center" style="color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                                <div style="text-align: left; color: rgb(245, 245, 245) !important;" data-ogsc=""><br aria-hidden="true"></div>
                                                                                <font size="2" style="color: rgb(245, 245, 245) !important;" data-ogsc=""></font>
                                                                            </div>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_spacebar" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="height: 30px; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <p style="height: 30px; margin: 0px; padding: 0px; color: rgb(245, 245, 245) !important;" data-ogsc=""></p>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_button" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" align="center" cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td align="center" style="border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; padding: 6px 16px; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <table cellspacing="0" cellpadding="0" align="center" style="table-layout: fixed; border: 0px; border-collapse: collapse; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                                <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                                    <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                                    <td data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                                        <a href="https://sender.zohoinsights-crm.com/ck1/2d6f.327230a/fdc74cb0-7357-11ee-a23c-52540064429e/f31ca0669287c4c601c8d128a3776655379226e0/2?e=cMbKC42Vh%2BmcQqtqj6%2FQossHL4vyLVPQOChggEUh9ZxRnHbqE8mRrG8J6Buetc08namtmzdrikQ7c0AsOxg%2B9m%2Fxgqcj1rhL5vTYEg%2BvJKw%3D" target="_blank" rel="noopener noreferrer" data-auth="NotApplicable" class="x_buttonOuterLink" style="text-decoration: none; color: rgb(219, 151, 255) !important;" data-ogsc="" data-linkindex="0">
                                                                                            <table cellspacing="3" cellpadding="3" align="center" style="font-size: 13px; letter-spacing: normal; font-family: Arial; background-color: rgb(60, 60, 60) !important; color: rgb(201, 201, 201) !important; border-radius: 6px; border-width: 0px; border-style: none; border-color: initial;" data-ogsc="rgb(67, 67, 67)" data-ogsb="rgb(217, 217, 217)">
                                                                                                <tbody data-ogsc="" style="color: rgb(201, 201, 201) !important;">
                                                                                                <tr data-ogsc="" style="color: rgb(201, 201, 201) !important;">
                                                                                                    <td align="center" style="overflow-wrap: break-word; word-break: break-word; border: 0px; padding: 7px 20px; font-size: 32px; font-weight: 400; font-style: normal; text-decoration: none; color: rgb(201, 201, 201) !important;" data-ogsc="">
                                                                                                        <p style="padding: 0px; margin: 0px; color: rgb(201, 201, 201) !important;" data-ogsc="">
                                                                                        <a href="https://crm.zoho.com/crm/org680056826/tab/Tasks/{idtask}" target="_blank" rel="noopener noreferrer" data-auth="NotApplicable" class="x_buttonInnerLink" style="text-decoration: none; color:white !important;" data-ogsc="rgb(67, 67, 67)" data-linkindex="1">Link Task</a> </p></td></tr></tbody></table></a>
                                                                                    </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_spacebar" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="height: 60px; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <p style="height: 60px; margin: 0px; padding: 0px; color: rgb(245, 245, 245) !important;" data-ogsc=""></p>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_text" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="font-size: 13px; letter-spacing: normal; font-family: Arial, Helvetica, sans-serif; min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgb(54, 54, 54) !important; color: rgb(245, 245, 245) !important;" data-ogsc="" data-ogsb="rgb(229, 229, 229)">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="overflow-wrap: break-word; word-break: break-word; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; padding: 6px 16px; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); font-family: Arial, Helvetica, sans-serif; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <div align="center" style="color: rgb(245, 245, 245) !important;" data-ogsc=""><br aria-hidden="true"></div>
                                                                            <font color="rgb(215, 215, 215)" size="2" style="color: rgb(215, 215, 215) !important;" data-ogsc="" data-ogac="#333333">
                                                                                <div style="clear: both; color: rgb(215, 215, 215) !important;" data-ogsc=""></div>
                                                                            </font>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                    </table>
                                </td>
                            </tr>
                        </tbody>
                        </table>
                        </table>
                        </html>
                    """, 'html')
            mensaje.attach(cuerpo)

            # Crear conexión al servidor SMTP y enviar mensaje
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, 'dev@data.cr,fmarcias@data.cr', mensaje.as_string()) 
        
        #Make notification when customer is PayDAta
        else :
             # Crear objeto mensaje
            mensaje = MIMEMultipart()
            mensaje['From'] = smtp_username
            mensaje['To'] = 'dev@data.cr,mgreen@data.cr,rmata@data.cr'
            tituloh=f"Nuevo Cliente ADNPAY , Task Generated  {nombret}"
            mensaje['Subject'] = tituloh
            # Agregar cuerpo del mensaje
            cuerpo = MIMEText(f"""
            <!DOCTYPE html>
            <html>
            <table class="x_contentOuter" id="x_contentOuter" cellpadding="0" cellspacing="0" width="100%" style="width: 100%; border: 0px; font-family: Arial, Helvetica, sans-serif; color: rgb(245, 245, 245) !important; font-size: 13px; border-collapse: collapse; letter-spacing: normal; " data-ogsc="rgb(17, 17, 17)" data-ogsb="rgb(240, 240, 240)">
                <tbody    tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                    <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                        <td align="center" class="x_contentmaintd" style="border: 0px; padding-top: 10px; padding-bottom: 20px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                            <table class="x_contentInner" id="x_contentInner" cellpadding="0" cellspacing="0" width="600px" style="width: 600px; border: 0px; border-collapse: collapse; table-layout: fixed;  color: rgb(245, 245, 245) !important;" data-ogsc="" data-ogsb="rgb(255, 255, 255)">
                                <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                    <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                        <td valign="top" style="border: 0px; overflow-wrap: break-word; word-break: break-word; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                            <div class="x_zpcontent-wrapper" id="x_page-container" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                <table cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_spacebar" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="height: 20px; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <p style="height: 20px; margin: 0px; padding: 0px; color: rgb(245, 245, 245) !important;" data-ogsc=""></p>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_image" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="overflow-wrap: break-word; word-break: break-word; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; padding: 6px 16px; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <p style="float: none; text-align: center; padding: 0px; margin: 0px; color: rgb(245, 245, 245) !important;" data-ogsc=""><img data-imagetype="AttachmentByCid" originalsrc="cid:gg4lga0f9a1c1433a4aa1942207bdf4bd2e9a" data-custom="AAMkADNjY2U1MjNhLWYwNGEtNDc1NC1hMDAwLTc2ZGM1ODViOGIzNABGAAAAAACs5oio36XmQLxiKvkcV0xvBwCKIfefbn62SJRbzT3Y61iDAAAAAAEMAACKIfefbn62SJRbzT3Y61iDAAF4A4KpAAABEgAQAKecKpFrrX1Hp2J3QQX%2Bnxs%3D" naturalheight="0" naturalwidth="0" src="https://attachments.office.net/owa/luis.herrera%40data.cr/service.svc/s/GetAttachmentThumbnail?id=AAMkADNjY2U1MjNhLWYwNGEtNDc1NC1hMDAwLTc2ZGM1ODViOGIzNABGAAAAAACs5oio36XmQLxiKvkcV0xvBwCKIfefbn62SJRbzT3Y61iDAAAAAAEMAACKIfefbn62SJRbzT3Y61iDAAF4A4KpAAABEgAQAKecKpFrrX1Hp2J3QQX%2Bnxs%3D&amp;thumbnailType=2&amp;token=eyJhbGciOiJSUzI1NiIsImtpZCI6IjczRkI5QkJFRjYzNjc4RDRGN0U4NEI0NDBCQUJCMTJBMzM5RDlGOTgiLCJ0eXAiOiJKV1QiLCJ4NXQiOiJjX3VidnZZMmVOVDM2RXRFQzZ1eEtqT2RuNWcifQ.eyJvcmlnaW4iOiJodHRwczovL291dGxvb2sub2ZmaWNlLmNvbSIsInVjIjoiZWExZjNkNDYyMWE5NGE2ZjhmZTRjZDJjZjVlZjBmZjUiLCJzaWduaW5fc3RhdGUiOiJbXCJrbXNpXCJdIiwidmVyIjoiRXhjaGFuZ2UuQ2FsbGJhY2suVjEiLCJhcHBjdHhzZW5kZXIiOiJPd2FEb3dubG9hZEA1NzAxOTkzOS1iMDdiLTRkOTUtODIwMC0zMmJkMGNmOTVkYzgiLCJpc3NyaW5nIjoiV1ciLCJhcHBjdHgiOiJ7XCJtc2V4Y2hwcm90XCI6XCJvd2FcIixcInB1aWRcIjpcIjExNTM4MDExMjIxNDk1NDM0MjhcIixcInNjb3BlXCI6XCJPd2FEb3dubG9hZFwiLFwib2lkXCI6XCI4ZTE2ODkzNS1lOTYxLTQzYjEtOWEyNS00NGY4ODhjN2ExNDhcIixcInByaW1hcnlzaWRcIjpcIlMtMS01LTIxLTIxODEwMDUyNzgtMjMxMjA4MDg0Mi0xMzMzMTg0ODA3LTQ3NzY5ODMzXCJ9IiwibmJmIjoxNjk4MjcyNjMwLCJleHAiOjE2OTgyNzMyMzAsImlzcyI6IjAwMDAwMDAyLTAwMDAtMGZmMS1jZTAwLTAwMDAwMDAwMDAwMEA1NzAxOTkzOS1iMDdiLTRkOTUtODIwMC0zMmJkMGNmOTVkYzgiLCJhdWQiOiIwMDAwMDAwMi0wMDAwLTBmZjEtY2UwMC0wMDAwMDAwMDAwMDAvYXR0YWNobWVudHMub2ZmaWNlLm5ldEA1NzAxOTkzOS1iMDdiLTRkOTUtODIwMC0zMmJkMGNmOTVkYzgiLCJoYXBwIjoib3dhIn0.LrTwDlQt9xdxs8etzdofDrWk1EYth-rQTj1f0Nq4o3GYtzzVnPmUl4H8Up3-Pf6Dmvf1Fl0SzieuUIhqkzLavM77U_K09VeAYiLXutl_LKvfRB0CPIVj5AG4y4WBPqLkn0WKF--yXLo_vXqb5irk_vHhonasz8qzcjNHGx2v3lHAM896zqFw-w1ZHYk7Q8g9SantJv9jnrDeA6J49Dm7jlnoSrflPdoNdQHo14h2yPBqvMOsEbPCRFWwNIMW7ww8oSCMTzQOyKnHsP884PR6rXTgMaYCMrrm7k80D69rGX0iaAK03I6ZA3w6NMNkE3nIVRsWAOV8iOJcPiup--5gWQ&amp;X-OWA-CANARY=1ZxTa212yUO8vgbOqLlI8eBugRyp1dsYVda629n30Nf5QmFptyQr4jUi0_X9IHZIR5FCcHMB3YQ.&amp;owa=outlook.office.com&amp;scriptVer=20231013005.20&amp;animation=true" class="x_zpImage x_imgsize_F Do8Zj" alt="Company name" width="540" height="139.479" style="width: 100%; max-width: 100%; vertical-align: top; color: rgb(245, 245, 245) !important; min-height: auto; min-width: auto; cursor: pointer;" crossorigin="use-credentials" fetchpriority="high" data-ogsc=""></p>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_spacebar" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="height: 15px; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <p style="height: 15px; margin: 0px; padding: 0px; color: rgb(245, 245, 245) !important;" data-ogsc=""></p>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_spacebar" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="height: 30px; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <p style="height: 30px; margin: 0px; padding: 0px; color: rgb(245, 245, 245) !important;" data-ogsc=""></p>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_text" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="font-size: 13px; letter-spacing: normal; font-family: Arial, Helvetica, sans-serif; min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="overflow-wrap: break-word; word-break: break-word; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; padding: 6px 16px; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); font-family: Arial, Helvetica, sans-serif; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <div align="center" style="padding: 0px; margin: 0px; color: rgb(255, 255, 255) !important;" data-ogsc="rgb(0, 0, 0)"><font style="color: rgb(255, 255, 255) !important;" data-ogsc=""><font size="4" style="color: rgb(255, 255, 255) !important;" data-ogsc=""><b data-ogsc="" style="color:black !important;">Nuevo Cliente Generado ADNPAY</b></font><br style="" aria-hidden="true"></font></div>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_spacebar" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="height: 5px; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <p style="height: 5px; margin: 0px; padding: 0px; color: rgb(245, 245, 245) !important;" data-ogsc=""></p>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_text" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="font-size: 13px; letter-spacing: normal; font-family: Arial, Helvetica, sans-serif; min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="overflow-wrap: break-word; word-break: break-word; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; padding: 6px 16px; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); font-family: Arial, Helvetica, sans-serif; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <div align="center" style="color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                                <div style="text-align: left; color: rgb(245, 245, 245) !important;" data-ogsc=""><br aria-hidden="true"></div>
                                                                                <font size="2" style="color: rgb(245, 245, 245) !important;" data-ogsc=""></font>
                                                                            </div>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_spacebar" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="height: 30px; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <p style="height: 30px; margin: 0px; padding: 0px; color: rgb(245, 245, 245) !important;" data-ogsc=""></p>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_button" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" align="center" cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td align="center" style="border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; padding: 6px 16px; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <table cellspacing="0" cellpadding="0" align="center" style="table-layout: fixed; border: 0px; border-collapse: collapse; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                                <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                                    <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                                    <td data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                                        <a href="https://sender.zohoinsights-crm.com/ck1/2d6f.327230a/fdc74cb0-7357-11ee-a23c-52540064429e/f31ca0669287c4c601c8d128a3776655379226e0/2?e=cMbKC42Vh%2BmcQqtqj6%2FQossHL4vyLVPQOChggEUh9ZxRnHbqE8mRrG8J6Buetc08namtmzdrikQ7c0AsOxg%2B9m%2Fxgqcj1rhL5vTYEg%2BvJKw%3D" target="_blank" rel="noopener noreferrer" data-auth="NotApplicable" class="x_buttonOuterLink" style="text-decoration: none; color: rgb(219, 151, 255) !important;" data-ogsc="" data-linkindex="0">
                                                                                            <table cellspacing="3" cellpadding="3" align="center" style="font-size: 13px; letter-spacing: normal; font-family: Arial; background-color: rgb(60, 60, 60) !important; color: rgb(201, 201, 201) !important; border-radius: 6px; border-width: 0px; border-style: none; border-color: initial;" data-ogsc="rgb(67, 67, 67)" data-ogsb="rgb(217, 217, 217)">
                                                                                                <tbody data-ogsc="" style="color: rgb(201, 201, 201) !important;">
                                                                                                <tr data-ogsc="" style="color: rgb(201, 201, 201) !important;">
                                                                                                    <td align="center" style="overflow-wrap: break-word; word-break: break-word; border: 0px; padding: 7px 20px; font-size: 32px; font-weight: 400; font-style: normal; text-decoration: none; color: rgb(201, 201, 201) !important;" data-ogsc="">
                                                                                                        <p style="padding: 0px; margin: 0px; color: rgb(201, 201, 201) !important;" data-ogsc="">
                                                                                        <a href="https://crm.zoho.com/crm/org680056826/tab/Tasks/{idtask}" target="_blank" rel="noopener noreferrer" data-auth="NotApplicable" class="x_buttonInnerLink" style="text-decoration: none; color:white !important;" data-ogsc="rgb(67, 67, 67)" data-linkindex="1">Link Task</a> </p></td></tr></tbody></table></a>
                                                                                    </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_spacebar" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgba(0, 0, 0, 0); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="height: 60px; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <p style="height: 60px; margin: 0px; padding: 0px; color: rgb(245, 245, 245) !important;" data-ogsc=""></p>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                            <td class="x_txtsize" valign="top" style="border: 0px; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                            <div class="x_zpelement-wrapper x_text" data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                <table title="" cellspacing="0" cellpadding="0" width="100%" style="font-size: 13px; letter-spacing: normal; font-family: Arial, Helvetica, sans-serif; min-width: 100%; max-width: 100%; table-layout: fixed; border: 0px; border-collapse: collapse; background-color: rgb(54, 54, 54) !important; color: rgb(245, 245, 245) !important;" data-ogsc="" data-ogsb="rgb(229, 229, 229)">
                                                                    <tbody data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <tr data-ogsc="" style="color: rgb(245, 245, 245) !important;">
                                                                        <td style="overflow-wrap: break-word; word-break: break-word; border-width: 0px; border-right-style: initial; border-left-style: initial; border-right-color: initial; border-left-color: initial; border-image: initial; padding: 6px 16px; border-top-style: none; border-top-color: rgb(17, 17, 17); border-bottom-style: none; border-bottom-color: rgb(17, 17, 17); font-family: Arial, Helvetica, sans-serif; color: rgb(245, 245, 245) !important;" data-ogsc="">
                                                                            <div align="center" style="color: rgb(245, 245, 245) !important;" data-ogsc=""><br aria-hidden="true"></div>
                                                                            <font color="rgb(215, 215, 215)" size="2" style="color: rgb(215, 215, 215) !important;" data-ogsc="" data-ogac="#333333">
                                                                                <div style="clear: both; color: rgb(215, 215, 215) !important;" data-ogsc=""></div>
                                                                            </font>
                                                                        </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                    </table>
                                </td>
                            </tr>
                        </tbody>
                        </table>
                        </table>
                        </html>
                    """, 'html')
            mensaje.attach(cuerpo)

            # Crear conexión al servidor SMTP y enviar mensaje
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, 'dev@data.cr,mgreen@data.cr,rmata@data.cr', mensaje.as_string()) 
        
    cursor.close()
    return "Webhook received!"
    
if __name__ == '__mail__':
    app.run(host='0.0.0.0', port=5002, debug=False)

