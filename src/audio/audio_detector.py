import time
import random
from datetime import datetime

# Simula as classes do classificador de áudio industrial (padrão YAMNet / CNN 1D)
CLASSES_AUDIO = ["Sirene_Incendio", "Sirene_Evacuacao", "Ruido_Furadeira", "Motor_Industrial", "Silencio"]

def simular_classificador_audio():
    """
    Simula o comportamento de um pipeline YAMNet/CNN escutando o chão de fábrica.
    Retorna a classe detectada e o nível de confiança da IA.
    """
    # Em um ambiente real, aqui seriam capturados buffers do microfone via PyAudio/SoundDevice
    # e passados como tensores para o modelo de IA (.pt).
    
    # Simulação probabilística: 85% ruído normal ou silêncio, 15% evento de emergência
    gatilho = random.random()
    if gatilho < 0.08:
        return "Sirene_Incendio", random.uniform(0.85, 0.99)
    elif gatilho < 0.15:
        return "Sirene_Evacuacao", random.uniform(0.82, 0.98)
    elif gatilho < 0.60:
        return "Ruido_Furadeira", random.uniform(0.70, 0.95)
    elif gatilho < 0.90:
        return "Motor_Industrial", random.uniform(0.65, 0.92)
    else:
        return "Silencio", random.uniform(0.90, 1.00)

def traduzir_alerta_acessibilidade(tipo_alerta: str, confianca: float):
    """
    Simula o envio digital instantâneo do evento para o smartwatch tátil do Mateus.
    Atende à tabela LOG_TRADUÇÃO_ACESSIBILIDADE do DER.
    """
    inicio_processamento = time.perf_counter()
    
    # Mapeamento do tipo de alerta exigido no Dicionário de Dados
    mapeamento_alertas = {
        "Sirene_Incendio": "incêndio",
        "Sirene_Evacuacao": "evacuação"
    }
    
    tipo_formatado = mapeamento_alertas.get(tipo_alerta, "falha")
    
    print("\n" + "🚨" * 20)
    print(f"[ALERTA DE EVENTO SONORO] DETECTADO: {tipo_alerta} ({confianca*100:.2f}% de certeza)")
    print(f"[ACESSIBILIDADE] Traduzindo frequência sonora para pulsação digital...")
    
    # Simulação do disparo de pacotes de rede UDP/MQTTS de baixa latência para os LEDs e Smartwatches
    time.sleep(random.uniform(0.015, 0.045)) # Simula latência de rede em milissegundos
    
    fim_processamento = time.perf_counter()
    latencia_ms = int((fim_processamento - inicio_processamento) * 1000)
    
    # Estruturação exata dos dados para a tabela LOG_TRADUÇÃO_ACESSIBILIDADE
    log_acessibilidade = {
        "data_hora": datetime.now().isoformat(),
        "tipo_alerta": tipo_formatado,
        "tempo_latencia_ms": latencia_ms,
        "status_envio_dispositivos": "SUCESSO_ENVIADO_SMARTWATCH"
    }
    
    print(f"[DISPOSITIVO MATEUS] Vibração Contínua de Emergência Ativada! Código: TÁTIL_PULSE_MAX")
    print(f"[LOG GERADO] Tipo: {log_acessibilidade['tipo_alerta']} | Latência: {log_acessibilidade['tempo_latencia_ms']}ms | Status: {log_acessibilidade['status_envio_dispositivos']}")
    print("🚨" * 20 + "\n")

def executar_monitoramento_audio():
    print("[INFO] Carregando Classificador de Sinais de Áudio Industrial...")
    print("[INFO] Escutando o ambiente fabril continuamente... Pressione Ctrl+C para parar.")
    
    try:
        while True:
            # Analisa o ambiente a cada 2 segundos
            time.sleep(2)
            classe, confianca = simular_classificador_audio()
            
            # Se a IA classificar o som como uma sirene de emergência:
            if "Sirene" in classe:
                traduzir_alerta_acessibilidade(classe, confianca)
            else:
                print(f"[ÁUDIO] Monitorando ambiente... Som predominante: {classe} ({confianca*100:.1f}%)", end="\r")
                
    except KeyboardInterrupt:
        print("\n[INFO] Sistema de monitoramento de áudio encerrado.")

if __name__ == "__main__":
    executar_monitoramento_audio()
