from brain.utils import clean_output
from core.inicializador import gerar_resposta

contexto_memoria = []
MAX_CONTEXTO = 5
DEFAULT_MODEL = "llama3.2"
DEFAULT_MODEL_HIGH = "llama3.3"

def generate_response(prompt, model_name=DEFAULT_MODEL):
    try:
        system_prompt = (
            "Você é Jarvis, um assistente de inteligência artificial altamente preciso, confiável e direto. "
            "Seu papel é fornecer respostas claras, informativas e bem estruturadas para qualquer pergunta feita. "
            "Evite respostas vagas, piadas ou firulas. Priorize a profundidade, concisão e utilidade da informação. "
            "Se a pergunta exigir, organize a resposta em seções com títulos e marcadores. "
            "Sempre responda em português, com linguagem formal e objetiva. "
            "Nunca diga que é um assistente de IA ou mencione sua programação, apenas entregue a resposta com autoridade e clareza."
        )
        # (Nota: você tinha dois prompts — você pode alternar entre eles aqui se quiser no futuro)

        # Monta histórico recente
        historico = "\n".join([f"Usuário: {p}\nJarvis: {r}" for p, r in contexto_memoria[-MAX_CONTEXTO:]])

        # Prepara o prompt final
        full_prompt = f"{system_prompt}\n{historico}\nUsuário: {prompt}\nJarvis:"

        # 🔥 Agora usa a chamada API moderna
        resposta = gerar_resposta(full_prompt, model_name)

        # Limpa a resposta (caso queira, mas na API já vem limpinha muitas vezes)
        resposta = clean_output(resposta.strip())

        # Atualiza o histórico de memória
        contexto_memoria.append((prompt, resposta))
        if len(contexto_memoria) > MAX_CONTEXTO:
            contexto_memoria.pop(0)

        return resposta
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"
