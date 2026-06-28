"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()



def pull_prompt_from_langsmith(prompt_name: str):
    """Baixa um prompt do LangSmith."""

    client = Client()
   
    prompt = client.pull_prompt(prompt_name)

    return prompt


def main() -> int:
    prompt_name = "leonanluppi/bug_to_user_story_v1"
    prompt = pull_prompt_from_langsmith(prompt_name)

    repo_name = prompt.metadata['lc_hub_repo']
    data = {
        repo_name: {
            'system_prompt': prompt.messages[0].prompt.template,
            'user_prompt': prompt.messages[1].prompt.template,
        }
    }

    output_path = Path(__file__).parent.parent / "prompts" / f"{repo_name}.yml"
    save_yaml(data, str(output_path))

    return 0


if __name__ == "__main__":
    sys.exit(main())
