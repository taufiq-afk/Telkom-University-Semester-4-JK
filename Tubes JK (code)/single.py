#import library
import socket
import os

#fungsi ini mengurus semua koneksi client
def handle_client(client_socket):
    try:
        # Menerima data dari client hingga 1024 byte dan mengkonversi / decode dari byte ke string
        request = client_socket.recv(1024).decode()
        print(f"Received request: {request}")
        
        headers = request.split('\n') # Memisahkan request HTTP ke dalam baris-baris individu
        filename = headers[0].split()[1] # Mendapatkan nama file yang diminta dari baris pertama header
        
        # Jika file yang diminta adalah root directory '/', ubah menjadi '/ui.html'
        if filename == '/':
            filename = '/ui.html'
        
        # menentukan lokasi lengkap file tersebut
        filepath = os.getcwd() + filename

        # Memeriksa apakah file yang diminta ada di sistem
        if os.path.exists(filepath):
            with open(filepath, 'rb') as file:
                response_content = file.read()
                response_headers = (
                    "HTTP/1.1 200 OK\n"
                    "Content-Type: text/html\n"
                    f"Content-Length: {len(response_content)}\n"
                    "Connection: close\n\n"
                )
        else:
            # Jika file tidak ditemukan, membuat konten untuk halaman 404 Not Found
            response_content = b"<html><body><h1>404 Not Found</h1></body></html>"
            # Membuat response status 404 Not Found
            response_headers = (
                "HTTP/1.1 404 Not Found\n"
                "Content-Type: text/html\n"
                "Connection: close\n\n"
            )
        
        # Menggabungkan header dan konten untuk membentuk response lengkap
        response = response_headers.encode() + response_content
        
        # Mengirim response lengkap ke client
        client_socket.sendall(response)
        print(f"Response sent")
    finally:
        #menutup koneksi ke client
        client_socket.close()
        print(f"Closed connection")

#fungsi ini mememulai server dan menangkap koneksi masuk (listening)
def main():
    server_ip = '127.0.0.1' #menetapkan server ip
    server_port = 6789 #menetapkan server port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #membuat socket server
    server.bind((server_ip, server_port)) # Menghubungkan socket ke alamat IP dan port yang ditentukan
    server.listen(5) #Memulai mendengarkan koneksi masuk
    print(f"Listening on {server_ip}:{server_port}") #print untuk memberi tau server sedang mendengarkan di IP dan port tertentu

    # Loop tak terbatas untuk terus menerima koneksi baru
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

#Memastikan bahwa fungsi main() dijalankan jika script ini dijalankan sebagai program utama
if __name__ == "__main__":
    main()
