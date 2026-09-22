from src.database.connection import registrar_infracao
import cv2
from ultralytics import YOLO
import time
import os

def run_inference(source_path=0):
    """
    Roda a inferência em tempo real para detecção de EPIs.
    source_path: 0 para WebCam, ou string com o caminho do vídeo de teste.
    """
    # 1. Carrega o modelo YOLOv8 padrão (Treinado em 80 classes do COCO)
    # Em produção, este modelo seria substituído pelo modelo treinado em classes (Helmet, Vest, etc.)
    print("[INFO] Carregando modelo YOLOv8...")
    model = YOLO("models/yolov8n.pt") 
    
    # 2. Inicializa a captura de vídeo (Webcam ou Arquivo)
    cap = cv2.VideoCapture(source_path)
    if not cap.isOpened():
        print(f"[ERRO] Não foi possível abrir a fonte de vídeo: {source_path}")
        return

    print("[INFO] Iniciando monitoramento do Chão de Fábrica. Pressione 'q' para sair.")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 3. Executa a detecção da IA no frame atual
        results = model(frame, verbose=False)[0]
        
        # Variáveis de controle para simulação da regra de negócio do EPI
        detectou_pessoa = False
        detectou_epi = False

        # 4. Varre os objetos detectados
        for box in results.boxes:
            class_id = int(box.cls[0])
            label = model.names[class_id]
            conf = float(box.conf[0])
            
            # Coordenadas do retângulo (Bounding Box)
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Mapeamento lógico de classes (Simulação baseada no dataset COCO padrão)
            # No COCO: class 0 = person, class 1 = bicycle, class 2 = car...
            # Para o seu projeto treinado, as classes seriam: 'Person', 'Helmet', 'Vest', 'Goggles'
            if label == "person" and conf > 0.5:
                detectou_pessoa = True
                # Desenha retângulo azul para pessoas
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, f"Operador {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            # Simulando detecção de EPI (usaremos objetos alternativos do COCO para teste visual se necessário)
            if label in ["backpack", "tie", "handbag"] and conf > 0.4:
                detectou_epi = True
                # Desenha retângulo verde para EPIs detectados
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "EPI OK", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 5. Validação da Regra de Negócio Crítica (Lógica IoU / Presença)
        # Se há uma pessoa na zona de risco mas nenhum EPI foi associado a ela:
        if detectou_pessoa and not detectou_epi:
            cv2.putText(frame, "ALERTA: INFRACAO DE EPI DETECTADA!", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        
        # Salva o log no banco de dados SQLite local
        registrar_infracao(
            id_setor="SETOR_MONTAGEM_01",
            id_camera="CAM_CFTV_04",
            epi_ausente="Capacete/Colete",
            confianca=conf
        )
            
            # Aqui entraria a chamada de banco de dados: LOG_INFRAÇÃO_EPI
            # print(f"[ALERTA BANCO DE DADOS] Registro gerado às {time.strftime('%X')} - EPI Ausente.")

        # 6. Exibe o painel de monitoramento na tela
        cv2.imshow("Painel HSE - Monitoramento de Visao Computacional por IA", frame)

        # Tecla de escape: pressionar 'q' encerra o sistema
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera recursos
    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Sistema de monitoramento encerrado.")

if __name__ == "__main__":
    # Executa usando a WebCam local. Para testar com arquivo, mude para: run_inference("data/mock_video.mp4")
    run_inference(source_path=0)