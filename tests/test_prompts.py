"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure


def load_prompts(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
V2_PATH = PROMPTS_DIR / "bug_to_user_story_v2.yml"


def get_v2_prompt_data():
    data = load_prompts(str(V2_PATH))
    key = list(data.keys())[0]
    return data[key]


class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompt = get_v2_prompt_data()
        assert "system_prompt" in prompt, "Campo 'system_prompt' ausente"
        assert prompt["system_prompt"].strip(), "system_prompt está vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona."""
        prompt = get_v2_prompt_data()
        system = prompt["system_prompt"]
        assert "Você é" in system, "Prompt não define uma persona com 'Você é'"

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato de User Story padrão."""
        prompt = get_v2_prompt_data()
        system = prompt["system_prompt"]
        assert "Como" in system and "eu quero" in system and "para que" in system, \
            "Prompt não menciona o formato padrão de User Story (Como / eu quero / para que)"

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (Few-shot)."""
        prompt = get_v2_prompt_data()
        system = prompt["system_prompt"]
        assert "Relato de Bug:" in system, "Prompt não contém exemplos few-shot"
        assert system.count("Relato de Bug:") >= 2, \
            "Prompt deve ter pelo menos 2 exemplos few-shot"

    def test_prompt_no_todos(self):
        """Garante que não há TODOs pendentes no prompt."""
        prompt = get_v2_prompt_data()
        system = prompt["system_prompt"]
        assert "TODO" not in system, "system_prompt ainda contém TODOs"

    def test_minimum_techniques(self):
        """Verifica se pelo menos 2 técnicas foram declaradas nos metadados."""
        prompt = get_v2_prompt_data()
        techniques = prompt.get("techniques_applied", [])
        assert len(techniques) >= 2, \
            f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques)}"

    def test_prompt_has_acceptance_criteria(self):
        """Verifica se o prompt instrui a gerar critérios de aceitação."""
        prompt = get_v2_prompt_data()
        system = prompt["system_prompt"]
        assert "Critérios de Aceitação" in system, \
            "Prompt não instrui sobre critérios de aceitação"

    def test_prompt_has_given_when_then(self):
        """Verifica se o prompt usa o formato Given-When-Then."""
        prompt = get_v2_prompt_data()
        system = prompt["system_prompt"]
        assert "Dado que" in system and "Quando" in system and "Então" in system, \
            "Prompt não menciona o formato Given-When-Then"

    def test_prompt_has_complexity_levels(self):
        """Verifica se o prompt diferencia bugs por complexidade."""
        prompt = get_v2_prompt_data()
        system = prompt["system_prompt"]
        assert "simples" in system.lower() and "médio" in system.lower() and "complexo" in system.lower(), \
            "Prompt não diferencia os níveis de complexidade do bug"

    def test_prompt_has_chain_of_thought(self):
        """Verifica se o prompt instrui um processo de análise interno."""
        prompt = get_v2_prompt_data()
        system = prompt["system_prompt"]
        assert "Processo de Análise" in system, \
            "Prompt não define um Processo de Análise (Chain of Thought)"
        assert "Não exponha essa análise na resposta final" in system, \
            "Prompt não instrui o modelo a ocultar o raciocínio interno"

    def test_prompt_has_bug_report_placeholder(self):
        """Verifica se o placeholder {bug_report} está presente."""
        prompt = get_v2_prompt_data()
        assert "{bug_report}" in prompt["system_prompt"], \
            "Placeholder {bug_report} ausente no system_prompt"
        assert "{bug_report}" in prompt.get("user_prompt", ""), \
            "Placeholder {bug_report} ausente no user_prompt"

    def test_validate_prompt_structure(self):
        """Executa a validação completa via validate_prompt_structure."""
        prompt = get_v2_prompt_data()
        is_valid, errors = validate_prompt_structure(prompt)
        assert is_valid, f"Prompt inválido: {errors}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
