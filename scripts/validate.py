"""
Script de validacao para o repositorio babel-tcc-translations.

Executa 4 tipos de validacao:
  1. Sintaxe JSON
  2. Schema (validacao manual, sem dependencias externas)
  3. Completude (todos os IDs do keywords-base cobertos)
  4. Unicidade (sem traducoes duplicadas)
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_FILES = {"template.json"}

KEYWORD_PATTERN = re.compile(r"^[a-z]+$")
ID_PATTERN = re.compile(r"^[0-9]+$")


def find_keywords_base_files():
    """Encontra todos os keywords-base.json."""
    return list((ROOT / "programming-languages").rglob("keywords-base.json"))


def find_translation_files():
    """Encontra todos os ficheiros de traducao."""
    files = []
    for path in (ROOT / "natural-languages").rglob("*.json"):
        if path.name in SKIP_FILES:
            continue
        files.append(path)
    return files


# ---------------------------------------------------------------------------
# 1. Validacao de sintaxe JSON
# ---------------------------------------------------------------------------

def validate_json_syntax(files):
    """Tenta carregar todos os .json e reporta erros de sintaxe."""
    errors = []
    for path in files:
        try:
            with open(path, encoding="utf-8") as f:
                json.load(f)
        except json.JSONDecodeError as e:
            rel = path.relative_to(ROOT)
            errors.append(f"  {rel}: {e}")
    return errors


# ---------------------------------------------------------------------------
# 2. Validacao de schema (manual)
# ---------------------------------------------------------------------------

def validate_keyword_table_schema(path, data):
    """Valida um keywords-base.json contra o schema keyword-table."""
    errors = []
    rel = path.relative_to(ROOT)

    if not isinstance(data, dict):
        errors.append(f"  {rel}: raiz deve ser um objeto")
        return errors

    allowed_root_keys = {"keywords"}
    extra_root = set(data.keys()) - allowed_root_keys
    if extra_root:
        errors.append(f"  {rel}: propriedades extra na raiz: {extra_root}")

    if "keywords" not in data:
        errors.append(f"  {rel}: campo obrigatorio 'keywords' em falta")
        return errors

    keywords = data["keywords"]
    if not isinstance(keywords, dict):
        errors.append(f"  {rel}: 'keywords' deve ser um objeto")
        return errors

    for key, value in keywords.items():
        if not KEYWORD_PATTERN.match(key):
            errors.append(f"  {rel}: chave '{key}' nao corresponde ao pattern ^[a-z]+$")
        if not isinstance(value, int) or value < 0:
            errors.append(f"  {rel}: valor de '{key}' deve ser um inteiro >= 0, encontrado: {value}")

    return errors


def validate_translation_schema(path, data):
    """Valida um ficheiro de traducao contra o schema translation."""
    errors = []
    rel = path.relative_to(ROOT)

    if not isinstance(data, dict):
        errors.append(f"  {rel}: raiz deve ser um objeto")
        return errors

    required_fields = ["version", "languageCode", "languageName", "programmingLanguage", "translations"]
    for field in required_fields:
        if field not in data:
            errors.append(f"  {rel}: campo obrigatorio '{field}' em falta")

    allowed_root_keys = set(required_fields)
    extra_root = set(data.keys()) - allowed_root_keys
    if extra_root:
        errors.append(f"  {rel}: propriedades extra na raiz: {extra_root}")

    string_fields = ["version", "languageCode", "languageName", "programmingLanguage"]
    for field in string_fields:
        if field in data and not isinstance(data[field], str):
            errors.append(f"  {rel}: '{field}' deve ser uma string")

    if "translations" not in data:
        return errors

    translations = data["translations"]
    if not isinstance(translations, dict):
        errors.append(f"  {rel}: 'translations' deve ser um objeto")
        return errors

    for key, value in translations.items():
        if not ID_PATTERN.match(key):
            errors.append(f"  {rel}: chave de traducao '{key}' nao corresponde ao pattern ^[0-9]+$")
        if not isinstance(value, str):
            errors.append(f"  {rel}: traducao para ID '{key}' deve ser uma string")
        elif len(value) < 1:
            errors.append(f"  {rel}: traducao para ID '{key}' esta vazia")

    return errors


def validate_schemas():
    """Executa validacao de schema em todos os ficheiros relevantes."""
    errors = []

    for path in find_keywords_base_files():
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        errors.extend(validate_keyword_table_schema(path, data))

    for path in find_translation_files():
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        errors.extend(validate_translation_schema(path, data))

    return errors


# ---------------------------------------------------------------------------
# 3. Validacao de completude
# ---------------------------------------------------------------------------

def validate_completeness():
    """Verifica que cada traducao cobre todos os IDs do keywords-base."""
    errors = []

    prog_langs = {}
    for kb_path in find_keywords_base_files():
        lang_name = kb_path.parent.name
        with open(kb_path, encoding="utf-8") as f:
            data = json.load(f)
        ids = set(str(v) for v in data.get("keywords", {}).values())
        prog_langs[lang_name] = ids

    for tr_path in find_translation_files():
        with open(tr_path, encoding="utf-8") as f:
            data = json.load(f)

        prog_lang = data.get("programmingLanguage", "").lower()
        rel = tr_path.relative_to(ROOT)

        if prog_lang not in prog_langs:
            errors.append(f"  {rel}: linguagem de programacao '{prog_lang}' sem keywords-base correspondente")
            continue

        base_ids = prog_langs[prog_lang]
        translation_ids = set(data.get("translations", {}).keys())

        missing = base_ids - translation_ids
        extra = translation_ids - base_ids

        if missing:
            sorted_missing = sorted(missing, key=int)
            errors.append(f"  {rel}: IDs em falta: {', '.join(sorted_missing)}")

        if extra:
            sorted_extra = sorted(extra, key=int)
            errors.append(f"  {rel}: IDs extras (nao existem no keywords-base): {', '.join(sorted_extra)}")

    return errors


# ---------------------------------------------------------------------------
# 4. Validacao de unicidade
# ---------------------------------------------------------------------------

def validate_uniqueness():
    """Verifica que nao ha duas keywords traduzidas para a mesma palavra."""
    errors = []

    for tr_path in find_translation_files():
        with open(tr_path, encoding="utf-8") as f:
            data = json.load(f)

        rel = tr_path.relative_to(ROOT)
        translations = data.get("translations", {})

        seen = {}
        for id_key, translated_word in translations.items():
            if not isinstance(translated_word, str) or not translated_word:
                continue
            lower_word = translated_word.lower()
            if lower_word in seen:
                errors.append(
                    f"  {rel}: traducao duplicada '{translated_word}' "
                    f"usada nos IDs {seen[lower_word]} e {id_key}"
                )
            else:
                seen[lower_word] = id_key

    return errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  Validacao de traducoes — babel-tcc-translations")
    print("=" * 60)
    print()

    all_json_files = list(ROOT.rglob("*.json"))
    has_errors = False

    # 1. Sintaxe JSON
    print("[1/4] Validacao de sintaxe JSON...")
    syntax_errors = validate_json_syntax(all_json_files)
    if syntax_errors:
        has_errors = True
        print("  FALHOU:")
        for e in syntax_errors:
            print(e)
    else:
        print(f"  OK — {len(all_json_files)} ficheiros JSON validos")
    print()

    # Se houver erros de sintaxe, as outras validacoes podem falhar
    if syntax_errors:
        print("Abortando validacoes restantes devido a erros de sintaxe.")
        sys.exit(1)

    # 2. Schema
    print("[2/4] Validacao de schema...")
    schema_errors = validate_schemas()
    if schema_errors:
        has_errors = True
        print("  FALHOU:")
        for e in schema_errors:
            print(e)
    else:
        print("  OK — todos os ficheiros cumprem os schemas")
    print()

    # 3. Completude
    print("[3/4] Validacao de completude...")
    completeness_errors = validate_completeness()
    if completeness_errors:
        has_errors = True
        print("  FALHOU:")
        for e in completeness_errors:
            print(e)
    else:
        print("  OK — todas as traducoes cobrem todos os IDs")
    print()

    # 4. Unicidade
    print("[4/4] Validacao de unicidade...")
    uniqueness_errors = validate_uniqueness()
    if uniqueness_errors:
        has_errors = True
        print("  FALHOU:")
        for e in uniqueness_errors:
            print(e)
    else:
        print("  OK — sem traducoes duplicadas")
    print()

    # Resultado final
    print("=" * 60)
    if has_errors:
        total = len(syntax_errors) + len(schema_errors) + len(completeness_errors) + len(uniqueness_errors)
        print(f"  RESULTADO: {total} erro(s) encontrado(s)")
        print("=" * 60)
        sys.exit(1)
    else:
        print("  RESULTADO: Todas as validacoes passaram!")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()
