import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Definição da URL do Banco de Dados
# Cria um banco de dados local SQLite (em arquivo) para testes sem precisar instalar servidores pesados.
# Em produção, bastaria trocar para: "postgresql://usuario:senha@localhost:5432/nomedobanco"
DATABASE_URL = "sqlite:///./industria_segura.db"

# 2. Inicialização do Engine e da Sessão
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Modelagem da Tabela com base no seu DER (Dicionário de Dados)
class LogInfracaoEPI(Base):
    __tablename__ = "log_infracao_epi"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    data_hora = Column(DateTime, default=datetime.utcnow, nullable=False)
    id_setor = Column(String, nullable=False)
    id_camera = Column(String, nullable=False)
    tipo_epi_ausente = Column(String, nullable=False)
    confianca_ia = Column(Float, nullable=False)
    url_frame_evidencia = Column(String, nullable=True)

# 4. Função para Criar as Tabelas no Banco de Dados automaticamente
def init_db():
    Base.metadata.create_all(bind=engine)
    print("[DATABASE] Tabelas iniciadas com sucesso.")

# 5. Função Utilitária para Salvar uma Infração (Será chamada pelo YOLO)
def registrar_infracao(id_setor: str, id_camera: str, epi_ausente: str, confianca: float, url_evidencia: str = None):
    session = SessionLocal()
    try:
        novo_log = LogInfracaoEPI(
            data_hora=datetime.now(),
            id_setor=id_setor,
            id_camera=id_camera,
            tipo_epi_ausente=epi_ausente,
            confianca_ia=confianca,
            url_frame_evidencia=url_evidencia
        )
        session.add(novo_log)
        session.commit()
        print(f"[DATABASE] Infração gravada! Setor: {id_setor} | Falta: {epi_ausente} | Confiança: {confianca:.2f}")
    except Exception as e:
        session.rollback()
        print(f"[DATABASE ERRO] Falha ao salvar log: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    # Se executar este arquivo diretamente, ele cria o banco de dados de teste
    init_db()