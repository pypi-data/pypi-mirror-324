import re
import sys

class CommitGenerator:
    def extract_code_block(self, text: str) -> str:
        try:
            if not isinstance(text, str):
                raise TypeError("O argumento 'text' deve ser uma string")

            match = re.search(r"```(.*?)```", text, re.DOTALL)
            if match:
                return match.group(1).strip()
            
            match = re.search(r"`(.*?)`", text)
            if match:
                return match.group(1).strip()

            raise ValueError("Nenhum bloco de código ou trecho inline foi encontrado no texto")

        except TypeError as e:
            sys.stderr.write(f"[ERROR] Tipo inválido: {e}\n")
        except AttributeError as e:
            sys.stderr.write(f"[ERROR] Erro ao acessar o bloco de código: {e}\n")
        except ValueError as e:
            sys.stderr.write(f"[WARNING] {e}\n")
        except Exception as e:
            sys.stderr.write(f"[ERROR] Erro inesperado em extract_code_block: {e}\n")

        return text
