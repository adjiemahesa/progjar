import sys
import socket
import logging
import json
import os
import ssl

alldata = dict()
alldata['1']=dict(nomor=1, nama="lionel messi", posisi="penyerang")
alldata['2']=dict(nomor=2, nama="cristiano ronaldo", posisi="penyerang")
alldata['3']=dict(nomor=3, nama="david de gea", posisi="kiper")
alldata['4']=dict(nomor=4, nama="jordi alba", posisi="bek kiri")
alldata['5']=dict(nomor=5, nama="aaron wan-bissaka", posisi="bek kanan")
alldata['6']=dict(nomor=6, nama="kevin de bruyne", posisi="gelandang tengah")
alldata['7']=dict(nomor=7, nama="casemiro", posisi="gelandang tengah")
alldata['8']=dict(nomor=8, nama="andreas christensen", posisi="bek tengah kanan")
alldata['9']=dict(nomor=8, nama="neymar", posisi="penyerang sayap kiri")
alldata['10']=dict(nomor=9, nama="ousmane dembele", posisi="penyerang sayap kanan")

def versi():
    return "versi 0.0.1"


def proses_request(request_string):
    #format request
    # NAMACOMMAND spasi PARAMETER
    cstring = request_string.split(" ")
    hasil = None
    try:
        command = cstring[0].strip()
        if (command == 'getplayerdata'):
            # getdata spasi parameter1
            # parameter1 harus berupa nomor pemain
            playernumber = cstring[1].strip()
            logging.warning("Request: getplayerdata {}".format(playernumber))
            try:
                hasil = alldata[playernumber]
            except:
                hasil = None
        elif (command == 'versi'):
            hasil = versi()
    except:
        hasil = None
    return hasil


def serialisasi(a):
    #print(a)
    #serialized = str(dicttoxml.dicttoxml(a))
    serialized =  json.dumps(a)
    return serialized

def run_server(server_address,is_secure=False):
    # ------------------------------ SECURE SOCKET INITIALIZATION ----
    if is_secure == True:
        print(os.getcwd())
        cert_location = os.getcwd() + '/certs/'
        socket_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        socket_context.load_cert_chain(
            certfile=cert_location + 'domain.crt',
            keyfile=cert_location + 'domain.key'
        )
    # ---------------------------------

    #--- INISIALISATION ---
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    logging.warning(f"starting up on {server_address}")
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1000)


    while True:
        # Wait for a connection
        koneksi, client_address = sock.accept()
        print("")
        logging.warning(f"Incoming connection from {client_address}")
        # Receive the data in small chunks and retransmit it

        try:
            if is_secure == True:
                connection = socket_context.wrap_socket(koneksi, server_side=True)
            else:
                connection = koneksi

            selesai=False
            data_received="" #string
            while True:
                data = connection.recv(32)
                if data:
                    data_received += data.decode()
                    if "\r\n\r\n" in data_received:
                        selesai=True

                    if (selesai==True):
                        hasil = proses_request(data_received)
                        logging.warning(f"sending response: {hasil}")

                        #hasil bisa berupa tipe dictionary
                        #harus diserialisasi dulu sebelum dikirim via network
                        # Send data
                        # some data structure may have complex structure
                        # how to send such data structure through the network ?
                        # use serialization
                        #  example : json, xml

                        # complex structure, nested dict
                        # all data that will be sent through network has to be encoded into bytes type"
                        # in this case, the message (type: string) will be encoded to bytes by calling encode

                        hasil = serialisasi(hasil)
                        hasil += "\r\n\r\n"
                        connection.sendall(hasil.encode())
                        selesai = False
                        data_received = ""  # string
                        break

                else:
                   logging.warning(f"no more data from {client_address}")
                   break
            # Clean up the connection
        except ssl.SSLError as error_ssl:
            logging.warning(f"SSL error: {str(error_ssl)}")

if __name__=='__main__':
    try:
        run_server(('0.0.0.0', 12000),is_secure=False)
    except KeyboardInterrupt:
        logging.warning("Control-C: Program Stop")
        exit(0)
    finally:
        logging.warning("Finished")