"""
Implementação de Steps para Testes BDD - Gilded Rose
Using pytest-bdd framework

Este módulo implementa os steps (Given/When/Then) para executar
os cenários BDD definidos em GILDED_ROSE_BDD.feature

Uso:
    pytest --gherkin-terminal-reporter GILDED_ROSE_BDD.feature
"""

from typing import Dict, List, Tuple
import pytest
from pytest_bdd import given, when, then, scenario, scenarios, parsers

# Importar as classes do Gilded Rose
import sys
sys.path.insert(0, '/Users/fernandoibraim/Desktop/trabalho-final-testes/python')
from gilded_rose import Item, GildedRose


# ============================================================================
# PYTEST_BDD CONFIGURATION
# ============================================================================

# Carrega todos os cenários do arquivo .feature
scenarios('../GILDED_ROSE_BDD.feature')


# ============================================================================
# FIXTURES - Inicialização compartilhada
# ============================================================================

@pytest.fixture
def context():
    """Context para armazenar estado entre steps."""
    class Context:
        def __init__(self):
            self.items = []
            self.gilded_rose = None
            self.expected_qualities = []
            self.expected_sell_ins = []
    
    return Context()


# ============================================================================
# GIVEN STEPS - Setup/Contexto
# ============================================================================

@given(parsers.parse('que tenho um item "{item_name}" com qualidade {quality:d} e dias para vender {sell_in:d}'))
def step_create_single_item(context, item_name, quality, sell_in):
    """Cria um único item com nome, qualidade e dias para vender."""
    context.items = [Item(item_name, sell_in, quality)]
    context.gilded_rose = GildedRose(context.items)


@given('que o sistema Gilded Rose está inicializado')
def step_initialize_system(context):
    """Inicializa o sistema Gilded Rose vazio."""
    context.items = []
    context.gilded_rose = GildedRose([])


@given('possuo um inventário vazio')
def step_initialize_empty_inventory(context):
    """Garante que o inventário começa vazio."""
    context.items = []
    context.gilded_rose = GildedRose([])


@given(parsers.parse('que tenho um inventário vazio'))
def step_ensure_empty_inventory(context):
    """Cria um inventário vazio."""
    context.items = []
    context.gilded_rose = GildedRose([])


@given('que tenho os itens no inventário:')
def step_create_multiple_items(context):
    """Cria múltiplos itens a partir de uma tabela."""
    # Tabela esperada:
    # | Nome | Qualidade | Dias |
    context.items = []
    for row in context.table:
        item = Item(row['Nome'], int(row['Dias']), int(row['Qualidade']))
        context.items.append(item)
    context.gilded_rose = GildedRose(context.items)


@given(parsers.parse('que tenho itens com qualidades "{qualities}" para item normal'))
def step_create_items_with_qualities(context, qualities):
    """Cria múltiplos itens normais com qualidades especificadas."""
    context.items = []
    quality_list = [int(q.strip()) for q in qualities.split(',')]
    for quality in quality_list:
        item = Item("Normal Item", 10, quality)
        context.items.append(item)
    context.gilded_rose = GildedRose(context.items)


@given(parsers.parse('que tenho itens com qualidades "{qualities}" para Aged Brie'))
def step_create_aged_brie_with_qualities(context, qualities):
    """Cria múltiplos Aged Brie com qualidades especificadas."""
    context.items = []
    quality_list = [int(q.strip()) for q in qualities.split(',')]
    for quality in quality_list:
        item = Item("Aged Brie", 10, quality)
        context.items.append(item)
    context.gilded_rose = GildedRose(context.items)


# ============================================================================
# WHEN STEPS - Ações
# ============================================================================

@when('o sistema atualiza a qualidade')
def step_update_quality_once(context):
    """Atualiza a qualidade dos itens uma vez."""
    context.gilded_rose.update_quality()


@when(parsers.parse('o sistema atualiza a qualidade {times:d} vezes'))
def step_update_quality_multiple_times(context, times):
    """Atualiza a qualidade dos itens múltiplas vezes."""
    for _ in range(times):
        context.gilded_rose.update_quality()


@when('o sistema atualiza todos os itens')
def step_update_all_items(context):
    """Atualiza todos os itens no inventário."""
    context.gilded_rose.update_quality()


# ============================================================================
# THEN STEPS - Verificações
# ============================================================================

@then(parsers.parse('a qualidade deve ser {expected:d}'))
def step_check_quality(context, expected):
    """Verifica a qualidade do primeiro item."""
    assert context.items[0].quality == expected, \
        f"Esperado qualidade {expected}, mas obteve {context.items[0].quality}"


@then(parsers.parse('os dias para vender devem ser {expected:d}'))
def step_check_sell_in(context, expected):
    """Verifica os dias para vender do primeiro item."""
    assert context.items[0].sell_in == expected, \
        f"Esperado sell_in {expected}, mas obteve {context.items[0].sell_in}"


@then(parsers.parse('o item "{item_name}" deve ter qualidade {expected:d}'))
def step_check_item_quality_by_name(context, item_name, expected):
    """Verifica a qualidade de um item específico por nome."""
    item = next((i for i in context.items if i.name == item_name), None)
    assert item is not None, f"Item '{item_name}' não encontrado"
    assert item.quality == expected, \
        f"Item '{item_name}': esperado qualidade {expected}, mas obteve {item.quality}"


@then(parsers.parse('o item "{item_name}" deve ter dias para vender {expected:d}'))
def step_check_item_sell_in_by_name(context, item_name, expected):
    """Verifica os dias para vender de um item específico por nome."""
    item = next((i for i in context.items if i.name == item_name), None)
    assert item is not None, f"Item '{item_name}' não encontrado"
    assert item.sell_in == expected, \
        f"Item '{item_name}': esperado sell_in {expected}, mas obteve {item.sell_in}"


@then(parsers.parse('as qualidades devem ser "{expected_qualities}"'))
def step_check_multiple_qualities(context, expected_qualities):
    """Verifica as qualidades de múltiplos itens."""
    expected_list = [int(q.strip().strip('"')) for q in expected_qualities.split(',')]
    for i, expected in enumerate(expected_list):
        assert context.items[i].quality == expected, \
            f"Item {i}: esperado qualidade {expected}, mas obteve {context.items[i].quality}"


@then('nenhum erro deve ocorrer')
def step_no_error_occurred(context):
    """Verifica que nenhum erro foi lançado (fixture passa se chegou até aqui)."""
    assert True, "Nenhum erro deve ter ocorrido"


# ============================================================================
# COMPLEX ASSERTION CHAINS - Para cenários com múltiplos steps
# ============================================================================

@then(parsers.parse('a qualidade deve ser {q:d}\nE os dias para vender devem ser {s:d}'))
def step_check_quality_and_sell_in(context, q, s):
    """Verifica qualidade e sell_in em um só step."""
    step_check_quality(context, q)
    step_check_sell_in(context, s)


# ============================================================================
# PARAMETRIZATION HELPERS
# ============================================================================

@pytest.fixture(params=[
    ("Normal Item", 25, 10),
    ("Normal Item", 50, 10),
    ("Normal Item", 0, 10),
])
def normal_items_fixture(request):
    """Fixture parametrizada para testes de item normal."""
    item_name, quality, sell_in = request.param
    return Item(item_name, sell_in, quality)


@pytest.fixture(params=[
    ("Aged Brie", 25, 10),
    ("Aged Brie", 0, 10),
    ("Aged Brie", 50, 10),
])
def aged_brie_fixture(request):
    """Fixture parametrizada para testes de Aged Brie."""
    item_name, quality, sell_in = request.param
    return Item(item_name, sell_in, quality)


@pytest.fixture(params=[
    ("Backstage passes to a TAFKAL80ETC concert", 25, 11),
    ("Backstage passes to a TAFKAL80ETC concert", 25, 10),
    ("Backstage passes to a TAFKAL80ETC concert", 25, 5),
    ("Backstage passes to a TAFKAL80ETC concert", 25, 0),
])
def backstage_pass_fixture(request):
    """Fixture parametrizada para testes de Backstage Passes."""
    item_name, quality, sell_in = request.param
    return Item(item_name, sell_in, quality)


@pytest.fixture(params=[
    ("Sulfuras, Hand of Ragnaros", 80, 10),
    ("Sulfuras, Hand of Ragnaros", 80, -1),
])
def sulfuras_fixture(request):
    """Fixture parametrizada para testes de Sulfuras."""
    item_name, quality, sell_in = request.param
    return Item(item_name, sell_in, quality)


# ============================================================================
# HOOKS - Executado antes/depois de cenários
# ============================================================================

def before_scenario(scenario, context):
    """Executado antes de cada cenário."""
    # Reset context
    if not hasattr(context, 'items'):
        context.items = []
    if not hasattr(context, 'gilded_rose'):
        context.gilded_rose = None


def after_scenario(scenario, context):
    """Executado depois de cada cenário."""
    # Cleanup
    context.items = []
    context.gilded_rose = None


# ============================================================================
# CUSTOM ASSERTIONS
# ============================================================================

def assert_item_unchanged(item: Item, original_quality: int, original_sell_in: int):
    """Verifica que um item não mudou (para Sulfuras)."""
    assert item.quality == original_quality, \
        f"Qualidade mudou! Esperado {original_quality}, obteve {item.quality}"
    assert item.sell_in == original_sell_in, \
        f"Sell_in mudou! Esperado {original_sell_in}, obteve {item.sell_in}"


def assert_quality_in_bounds(item: Item, min_quality: int = 0, max_quality: int = 50):
    """Verifica que a qualidade está dentro dos limites."""
    assert min_quality <= item.quality <= max_quality, \
        f"Qualidade {item.quality} fora dos limites [{min_quality}, {max_quality}]"


def assert_quality_decreased(item: Item, original_quality: int, expected_decrease: int):
    """Verifica que a qualidade diminuiu do valor esperado."""
    expected_quality = max(0, original_quality - expected_decrease)
    assert item.quality == expected_quality, \
        f"Qualidade esperada {expected_quality}, obteve {item.quality}"


def assert_quality_increased(item: Item, original_quality: int, expected_increase: int):
    """Verifica que a qualidade aumentou do valor esperado."""
    expected_quality = min(50, original_quality + expected_increase)
    assert item.quality == expected_quality, \
        f"Qualidade esperada {expected_quality}, obteve {item.quality}"


# ============================================================================
# EXEMPLO DE USO DIRETO (sem pytest-bdd)
# ============================================================================

def example_manual_bdd_test():
    """Exemplo de como testar manualmente sem pytest-bdd."""
    
    print("=" * 70)
    print("EXEMPLO: Item normal com qualidade dentro dos limites")
    print("=" * 70)
    
    # Given
    print("✓ Given: Criando item 'Normal Item' com qualidade 25 e dias 10")
    items = [Item("Normal Item", 10, 25)]
    gilded_rose = GildedRose(items)
    
    # When
    print("✓ When: Atualizando a qualidade")
    gilded_rose.update_quality()
    
    # Then
    print("✓ Then: Verificando resultados")
    assert items[0].quality == 24, f"Esperado 24, obteve {items[0].quality}"
    assert items[0].sell_in == 9, f"Esperado 9, obteve {items[0].sell_in}"
    
    print(f"  → Qualidade: {items[0].quality} ✅")
    print(f"  → Dias: {items[0].sell_in} ✅")
    print("  PASSOU! ✅\n")


if __name__ == "__main__":
    # Executar exemplo manual
    example_manual_bdd_test()
    
    print("Para executar todos os cenários BDD:")
    print("  pytest --gherkin-terminal-reporter GILDED_ROSE_BDD.feature -v")
    print("\nOu com behave:")
    print("  behave features/")
