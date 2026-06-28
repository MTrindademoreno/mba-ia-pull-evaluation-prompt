"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """

    prompt_key = next(iter(prompt_data))
    prompt = prompt_data[prompt_key]

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", prompt["system_prompt"]),
        ("human", prompt["user_prompt"]),
    ])

    client = Client()
    client.push_prompt(prompt_name, object=chat_prompt)
    print(f"✅ Prompt enviado: {prompt_name}")
    return True


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    prompt_name = next(iter(prompt_data))
    return validate_prompt_structure(prompt_data[prompt_name])


def main():
    """Função principal"""
    prompt_data = load_yaml(Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml")
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print(f"❌ Prompt inválido: {errors}")
        return 1
    
    username = os.getenv("USERNAME_LANGSMITH_HUB")
    push_prompt_to_langsmith(prompt_name=f"{username}/bug_to_user_story_v2", prompt_data=prompt_data)


if __name__ == "__main__":
    sys.exit(main())
