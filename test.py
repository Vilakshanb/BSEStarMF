import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from zeep import Client

# Define the URL of the WSDL file
wsdl_url = "https://www.bsestarmf.in/MFOrderEntry/MFOrder.svc?Wsdl"

# Create a Zeep client
client = Client(wsdl_url)


# Get the current date in YYYYMMDD format
current_date = datetime.now().strftime("%Y%m%d")

# Your memberid
memberid = "13464"

# Construct the TransNo
trans_no = current_date + memberid + "000001"

print(f"Trans No: {trans_no}")


# Define the SOAP endpoint
url = "https://www.bsestarmf.in/MFOrderEntry/MFOrder.svc/Secure"

# Define the SOAP headers
headers = {
    "Content-Type": "application/soap+xml; charset=utf-8",
    "SOAPAction": "http://bsestarmf.in/MFOrderEntry/getPassword",
}

# Define the SOAP body with placeholders for LoginID, Password, and Passkey
body = """
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
xmlns:bses="http://bsestarmf.in/">
<soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
<wsa:Action>http://bsestarmf.in/MFOrderEntry/getPassword</wsa:Action>
<wsa:To>
https://www.bsestarmf.in/MFOrderEntry/MFOrder.svc/Secure
</wsa:To>
</soap:Header>
<soap:Body>
<bses:getPassword> 
<bses:UserId>{LoginID}</bses:UserId> 
<bses:Password>{Password}</bses:Password> 
<bses:PassKey>{Passkey}</bses:PassKey> 
</bses:getPassword>
</soap:Body>
</soap:Envelope>
"""

body_order = """
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
xmlns:bses="http://bsestarmf.in/">
<soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
<wsa:Action>http://bsestarmf.in/MFOrderEntry/OrderEntry</wsa:Action>
<wsa:To>
https://www.bsestarmf.in/MFOrderEntry/MFOrder.svc/Secure
</wsa:To>
</soap:Header>
<soap:Body>
<bses:getPassword> 
<bses:UserId>{LoginID}</bses:UserId> 
<bses:Password>{Password}</bses:Password> 
<bses:PassKey>{Passkey}</bses:PassKey> 
</bses:getPassword>
</soap:Body>
</soap:Envelope>
"""

# Replace placeholders with actual values
login_id = "1346403"
password = "Mpcpl@113g"
passkey = "0123456789"
body = body.format(LoginID=login_id, Password=password, Passkey=passkey)

# Send the SOAP request
response = requests.post(url, headers=headers, data=body)

# Parse the XML response
root = ET.fromstring(response.text)

# Define the namespace
namespaces = {
    "s": "http://www.w3.org/2003/05/soap-envelope",
    "a": "http://www.w3.org/2005/08/addressing",
    "bse": "http://bsestarmf.in/",
}


# Extract the getPasswordResult value
if response.status_code == 200:
    # Parse the XML and proceed
    pass
    # print(f"Error: Received status code {response.status_code}")
    # print(response.text)


# Split the result to get the session ID
result_element = root.find(".//bse:getPasswordResult", namespaces=namespaces)
if result_element is not None:
    result = result_element.text
    session_id = result.split("|")[1]
    print(f"Session ID: {session_id}")
else:
    print("Error: getPasswordResult not found in the response.")
    exit()  # Exit the script if the result is not found


# print(f"Session ID: {session_id}")


# Extracted session ID from previous step
encrypted_password = session_id
print(f"Encrypted Password: {encrypted_password}")

# Define the SOAP endpoint for order entry
order_entry_url = "https://bsestarmf.in/MFOrderEntry/MFOrder.svc/Secure"

# Define the SOAP headers for order entry
order_entry_headers = {
    "Content-Type": "application/soap+xml; charset=utf-8",
    "SOAPAction": "http://bsestarmf.in/MFOrderEntry/orderEntryParam",
}

# Define the SOAP body for order entry with placeholders
order_entry_body = """
<soap:Envelope xmlns:soap="https://www.w3.org/2003/05/soap-envelope" xmlns:bses="http://bsestarmf.in/">
   <soap:Header xmlns:wsa="https://www.w3.org/2005/08/addressing">
      <wsa:Action>http://bsestarmf.in/MFOrderEntry/OrderEntry</wsa:Action>
      <wsa:To>https://bsestarmf.in/MFOrderEntry/MFOrder.svc/Secure</wsa:To>
   </soap:Header>
   <soap:Body>
      <bses:orderEntryParam>
         <bses:TransCode>NEW</bses:TransCode>
         <bses:TransNo>{trans_no}</bses:TransNo>
         <bses:UserID>{loginid}</bses:UserID>
         <bses:MemberId>{membercode}</bses:MemberId>
         <bses:ClientCode>{clientcode}</bses:ClientCode>
         <bses:SchemeCd>02G</bses:SchemeCd>
         <bses:BuySell>P</bses:BuySell>
         <bses:BuySellType>FRESH</bses:BuySellType>
         <bses:DPTxn>P</bses:DPTxn>
         <bses:OrderVal>50000</bses:OrderVal>
         <bses:AllRedeem>N</bses:AllRedeem>
         <bses:KYCStatus>Y</bses:KYCStatus>
         <bses:EUINVal>N</bses:EUINVal>
         <bses:MinRedeem>N</bses:MinRedeem>
         <bses:DPC>Y</bses:DPC>
         <bses:Password>{encrypted_password}</bses:Password>
         <bses:PassKey>{passkey}</bses:PassKey>
      </bses:orderEntryParam>
   </soap:Body>
</soap:Envelope>
"""

# ... (rest of the code remains unchanged)

# Replace placeholders with actual values
loginid = "1346403"
membercode = "13464"
clientcode = "BZPPB4781G"
encrypted_password = (
    session_id  # This could be the session ID or another encrypted password
)
print(f"encrypted_password: {encrypted_password}")
print(f"PASSKEY: {passkey}")  # Add this line

# ... (rest of the code remains unchanged)

order_entry_body = order_entry_body.format(
    loginid=loginid,
    membercode=membercode,
    clientcode=clientcode,
    encrypted_password=encrypted_password,
    passkey=passkey,
    trans_no=trans_no,  # Add this line
)

# Send the SOAP request for order entry
order_entry_response = requests.post(
    order_entry_url, headers=order_entry_headers, data=order_entry_body
)

# Print the order entry response
print(f"Order Entry Response Status Code: {order_entry_response.status_code}")
print("Error details:", order_entry_response.text)
print("Order Entry SOAP Body:", order_entry_body)

if order_entry_response.status_code != 200:
    print("Error in order entry request.")
    print(order_entry_response.text)
    exit()
