#import library
import socket
import sys

#fungsi untuk koneksi ke server
def http_client(server_host, server_port, filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #membuat socket
    
    client_socket.connect((server_host, int(server_port))) #koneksi ke server
    
    #membuat dan mengirim request http
    request = f"GET {filename} HTTP/1.1\r\nHost: {server_host}\r\nConnection: close\r\n\r\n"
    client_socket.sendall(request.encode())
    
    #menerima dan membaca response
    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data
    
    client_socket.close() #menutup koneksi
    
    print(response.decode()) #menampilkan response

if __name__ == "__main__": #kondisi yang memeriksa apakah skrip dijalankan sebagai skrip utama atau tidak.
    if len(sys.argv) != 4: #memeriksa apakah jumlah argumen yang diberikan melalui baris perintah benar.
        print("Please use this command line format on your terminal: python client.py <server_host> <server_port> <filename>")
        sys.exit(1)

    # Jika jumlah argumen benar (yaitu 4), skrip akan melanjutkan untuk mendapatkan nilai dari argumen baris perintah. 
    #Argumen disini maksudnya server host, server port dan filename 
    server_host = sys.argv[1]
    server_port = sys.argv[2]
    filename = sys.argv[3]
    
    #memulai proses koneksi ke server HTTP dan mengirim request
    http_client(server_host, server_port, filename)