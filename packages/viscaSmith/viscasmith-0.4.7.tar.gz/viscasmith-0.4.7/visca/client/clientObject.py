import time
from collections import deque
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtNetwork import QUdpSocket, QHostAddress
from PyQt6.QtWidgets import QApplication

from visca.cameraObject import CameraObject
from visca.dataStucture.messagePacker import MessagePacker
from visca.dataStucture.messageUnpacker import MessageUnpacker
from visca.dictionary.enumerations import ExposureModeEnum

VISCA_TERMINATOR = b'\xFF'
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 52381
CAMERA_ID = b'\x81'
# Messaggi standard (minimi) - qui semplificati
VISCA_ACK = b'\x01\x00\x00\x04\x00\x00\x00\x00\x02\xFF'
VISCA_COMPLETION = b'\x01\x00\x00\x04\x00\x00\x00\x00\x03\xFF'
VISCA_ERROR = b'\x01\x00\x00\x04\x00\x00\x00\x00\x04\xFF'

class ViscaCommand:
    """
    Rappresenta un comando in coda:
    - data: bytes da inviare (comando "puro" con header VISCA IP)
    - sequence_number: per correlare i pacchetti di ack/error/completion
    - state: WAITING_ACK -> WAITING_COMPLETION -> DONE/FAILED
    - retries: quante volte abbiamo ritrasmesso
    - last_send_time: quando l'abbiamo inviato l'ultima volta
    """
    def __init__(self, data: bytes, sequence_number: int):
        self.data = data
        self.sequence_number = sequence_number

        self.state = "WAITING_ACK"
        self.retries = 0
        self.last_send_time = 0.0


class ClientObject(QObject):
    info_SIGNAL = pyqtSignal(str)
    error_SIGNAL = pyqtSignal(str)
    serverMessage = pyqtSignal(str)

    def __init__(self, _camera, parent=None):
        super().__init__(parent)
        self.cameraObject = _camera
        self.socket = QUdpSocket(self)
        self.server_address = QHostAddress("127.0.0.1")
        self.server_port = 52381
        # Ci sono situazioni come durante i movimenti della camera in cui
        # si possono inviare comandi in rapida successione.
        # Per evitare di sovraccaricare il server, mettiamo i comandi in coda.
        # e verranno invianti uno alla volta.
        self.queue = deque()
        self.current_command = None
        # Contatore sequence number
        self.sequence_counter = 1
        # Timer periodico per controllare timeout e inviare/rinviare comandi
        self.check_timer = QTimer()
        self.check_timer.setInterval(50)  # 50ms o 100ms
        self.check_timer.timeout.connect(self.processQueue)
        self.check_timer.start()
        self.socket.readyRead.connect(self.handleReadyRead)
        self.messagePacker = MessagePacker()
        self.messageUnpacker = MessageUnpacker()

    def connectToServer(self, host, port):
        self.server_address = QHostAddress(host)
        self.server_port = port
        self.sendHandshake()

    def sendHandshake(self):
        handshake = b'\x02\x00\x00\x01\x00\x00\x00\x01\x01'
        self.socket.writeDatagram(handshake, self.server_address, self.server_port)
        self.info_SIGNAL.emit("Sent handshake")

    def enqueueViscaString(self, command_str: str):
        """ Converte la stringa in un ViscaCommand e lo mette in coda. """
        packed_data = self.messagePacker.build_command(command_str)
        seq = self.sequence_counter
        self.sequence_counter += 1
        cmd = ViscaCommand(packed_data, seq)
        self.queue.append(cmd)

    def processQueue(self):
        """
        Se non c'è un cmd in corso, prendo il prossimo in coda e lo invio con sendCommand.
        Se c'è un cmd in corso, verifico timeout/ritrasmissione.
        Cosa fa questo snippet

        Timeout: ogni chiamata a processQueue(), se c’è un comando
        in WAITING_ACK o WAITING_COMPLETION e il tempo dall’ultimo invio supera
        1 secondo, lo ritrasmette incrementando il contatore retries.
        Limite di ritrasmissioni: se retries supera 5, consideriamo il comando “FAILED”
        e lo scartiamo.
        Rilascio del comando (current_command = None) per passare a quello successivo in coda.

        Quando ricevi l’ACK, imposti state = "WAITING_COMPLETION".
        Quando ricevi la Completion (o l’equivalente per un Inquire),
        imposti state = "DONE" e fai current_command = None (nel tuo parseIncomingPacket).

        Una volta che current_command diventa None, il prossimo ciclo di processQueue()
        pescherà un nuovo comando dalla coda, se c’è.
        """
        # 1) Se NON abbiamo un comando attivo e la coda non è vuota,
        #    estraiamo il prossimo e lo inviamo.
        if not self.current_command and self.queue:
            self.current_command = self.queue.popleft()
            self.sendCommand(self.current_command)

        # 2) Se ABBIAMO un comando in corso, controlliamo se è andato in timeout
        if self.current_command:
            now = time.time()
            # Esempio: timeout di 1 secondo
            if (now - self.current_command.last_send_time) > 1.0:
                # SE il comando è ancora in attesa di ACK o di COMPLETION
                if self.current_command.state in ("WAITING_ACK", "WAITING_COMPLETION"):
                    self.current_command.retries += 1
                    if self.current_command.retries > 5:
                        # Abbiamo superato il numero massimo di ritrasmissioni
                        self.error_SIGNAL.emit(
                            f"Command seq={self.current_command.sequence_number} failed after 5 retries."
                        )
                        self.current_command.state = "FAILED"
                        # Libera lo slot
                        self.current_command = None
                    else:
                        # Ritrasmetti
                        self.info_SIGNAL.emit(
                            f"Timeout -> retrying command seq={self.current_command.sequence_number}. "
                            f"Attempt #{self.current_command.retries}."
                        )
                        self.sendCommand(self.current_command)
                elif self.current_command.state in ("DONE", "FAILED"):
                    # Se per qualche motivo siamo già in stato DONE o FAILED,
                    # liberiamo lo slot (potrebbe essere un caso limite).
                    self.current_command = None

    def sendCommand(self, cmd: ViscaCommand):
        """ Invia 'cmd' via socket, setta last_send_time """
        cmd.last_send_time = time.time()
        self.socket.writeDatagram(cmd.data, self.server_address, self.server_port)
        self.info_SIGNAL.emit(f"Sending seq={cmd.sequence_number}: {cmd.data.hex()}")

    def handleReadyRead(self):
        while self.socket.hasPendingDatagrams():
            datagram, host, port = self.socket.readDatagram(self.socket.pendingDatagramSize())
            self.parseIncomingPacket(datagram)

    def parseIncomingPacket(self, packet: bytes):
        print(f"Received packet: {packet.hex().upper()}")
        parsed = self.messageUnpacker.unpack_message(packet)
        msg_type = parsed["message_type"]
        seq_num = parsed["sequence_number"]
        self.info_SIGNAL.emit(f"Ricevuto pacchetto -> type={msg_type}, seq={seq_num}, raw={packet.hex().upper()}")

        # Se vuoi associare il seq_num al comando in corso:
        if msg_type in ("ack", "completion", "error"):
            # Confronta seq_num col current_command
            if self.current_command and self.current_command.sequence_number == seq_num:
                if msg_type == "ack":
                    # se il comando è in attesa di ACK, passa a "WAITING_COMPLETION"
                    if self.current_command.state == "WAITING_ACK":
                        self.current_command.state = "WAITING_COMPLETION"
                elif msg_type == "completion":
                    # se il comando è in attesa di COMPLETION, passa a "DONE"
                    self.current_command.state = "DONE"
                    self.current_command = None
                elif msg_type == "error":
                    self.current_command.state = "FAILED"
                    self.current_command = None
            # Se i sequence number non corrispondono, potresti ignorare o loggare

        elif msg_type == "inquire_reply":
            # Se fosse un messaggio di "comando" dal server al client,
            # oppure semplicemente lo ignori se sei lato client.
            print("Comando ricevuto dal server command_set")
            self.cameraObject.handleSet(parsed["command_payload"])
            self.serverMessage.emit(f"Comando ricevuto dal server: {parsed['command_payload'].hex()}")
            self.current_command.state = "DONE"
            self.current_command = None

    def isHandShake(self, data):
        return data == b'\x02\x00\x00\x01\x00\x00\x00\x01\x01'

    def isIFClear(self, data):
        return data == b'\x01\x00\x00\x05\x00\x00\x00\x02\x81\x01\x00\x01\xff'

if __name__ == "__main__":
    app = QApplication([])
    camera = CameraObject()
    client = ClientObject(camera)
    client.connectToServer(SERVER_HOST, SERVER_PORT)

    # Collegamento ai segnali per debug
    client.error_SIGNAL.connect(print)
    client.info_SIGNAL.connect(print)
    client.serverMessage.connect(print)

    # Messaggi da inviare
    exposure_message = camera.exposure.setExposureMode(ExposureModeEnum.MANUAL)
    QTimer.singleShot(1000, lambda: client.enqueueViscaString(exposure_message))

    message = camera.exposure.getExposureMode()
    QTimer.singleShot(2000, lambda: client.enqueueViscaString(message))

    app.exec()