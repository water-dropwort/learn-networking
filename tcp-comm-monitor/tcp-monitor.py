import socket, threading, time, sys
from ipheader import IP
from tcpheader import TCP
import parameter

# TCPクライアント通信スレッド処理
def client_work(client, host, port, is_close_from_client):
    time.sleep(2)
    print("[*] connect")
    client.connect((host,port))

    time.sleep(2)
    print("[*] sendall")
    request = "GET / HTTP/1.1\r\nHost: "+host
    if False == is_close_from_client:
        request = request + "\r\nConnection: close"
    request = request + "\r\n\r\n"
    client.sendall(request.encode("utf-8"))

    time.sleep(2)
    if is_close_from_client:
        print("[*] shutdown from client")
        client.shutdown(socket.SHUT_WR)
    else:
        # 空文字が返されるまでrecvした後にshutdownする。
        while True:
            rcv = client.recv(1024)
            if rcv == b'':
                break
        print("[*] shutdown")
        client.shutdown(socket.SHUT_RDWR)

    time.sleep(2)
    print("[*] close")
    client.close()

# TCP通信監視スレッド処理
def monitor_work(sock, server_addr = None, is_debug = False):
    try:
        while True:
            rcv = sock.recv(65535)
            ip_h = IP(rcv[0:20])
            # IPアドレスでフィルタ
            if server_addr == None or (server_addr == ip_h.src_address or server_addr == ip_h.dst_address):
                if ip_h.protocol == "TCP":
                    ip_h_len = ip_h.ihl * 4 # 4-byte
                    raw = rcv[ip_h_len:(ip_h_len+20)]
                    tcp_h = TCP(raw)
                    print("[%s] %s:%d -> %s:%d ACK=%d,URG=%d,PSH=%d,RST=%d,SYN=%d,FIN=%d"
                          % (ip_h.protocol, ip_h.src_address, tcp_h.src_port, ip_h.dst_address, tcp_h.dst_port
                             ,tcp_h.ack, tcp_h.urg, tcp_h.psh, tcp_h.rst, tcp_h.syn, tcp_h.fin), "\r\n"
                          ,"      AckNo.=%d, SeqNo.=%d, WndSize=%d" % (tcp_h.ack_seq_no, tcp_h.seq_no, tcp_h.window_size), "\r\n"
                          ,"      Body:", rcv[(ip_h_len+20):(ip_h_len+20+100)], "...")
                else:
                    print("[%s] %s -> %s" % (ip_h.protocol, ip_h.src_address, ip_h.dst_address))
    except Exception as ex:
        print("[*] End of monitor work thread")
        if (is_debug):
            print("[*] Excp. Detail:", ex)

def main():
    # パラメータ読込
    filepath = sys.argv[1] if len(sys.argv) > 1 else None
    _parameter = parameter.Parameter(filepath)

    # TCP通信監視用RAWソケット
    sock = socket.socket(socket.AF_INET,socket.SOCK_RAW, socket.IPPROTO_IP)
    host = socket.gethostname()
    sock.bind((host,0))
    sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON) # プロミスキャスモードON

    # TCPクライアント
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_thread = threading.Thread(
        target=client_work,
        args=(client, _parameter.host, _parameter.port, _parameter.close_from_client,) )

    server_addr = socket.gethostbyname(_parameter.host)
    monitor_thread = threading.Thread(
        target=monitor_work,
        args=(sock, server_addr, _parameter.debugmode,))

    # スレッド始動
    monitor_thread.start()
    client_thread.start()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("[*] Close this application")
    except Exception as ex:
        print("[*] Error occured. Detail:", ex)
    finally:
        if sock != None:
            sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF) # プロミスキャスモードOFF
            sock.close()

main()
