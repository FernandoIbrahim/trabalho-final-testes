# 🧬 Stryker - Mutation Testing Framework

## Visão Geral

**Stryker** é um framework profissional de **mutation testing** que avalia a qualidade dos testes. Para projetos em **Python**, usamos **`cosmic-ray`** que é o equivalente direto do Stryker.

---

## 🎯 O Que é Stryker?

**Stryker** (e seu equivalente Python `cosmic-ray`) é uma ferramenta que:

1. **Cria mutantes**: Altera pequenas partes do código
2. **Executa testes**: Roda a suíte contra cada mutante
3. **Calcula Kill Rate**: Mede quantos mutantes foram "mortos" (detectados)
4. **Gera relatórios**: Mostra onde os testes são fracos

---

## 🔍 Conceito: Mutation Testing

### Exemplo Prático

```python
# Código Original
def update_quality(quality, item_type):
    if quality < 50:                    # ← Linha original
        quality = quality + 1
    return quality

# Mutante 1: Trocar < por <=
def update_quality(quality, item_type):
    if quality <= 50:                   # ← MUTADO: < → <=
        quality = quality + 1
    return quality

# Mutante 2: Trocar + por -
def update_quality(quality, item_type):
    if quality < 50:
        quality = quality - 1            # ← MUTADO: + → -
    return quality

# Mutante 3: Remover incremento
def update_quality(quality, item_type):
    if quality < 50:
        pass                             # ← MUTADO: instrução removida
    return quality
```

### Teste Bom vs Teste Fraco

```python
# ❌ TESTE FRACO - Não detecta mutação
def test_quality_increases():
    result = update_quality(25)
    assert result > 25  # ← Muito genérico!

# ✅ TESTE BOM - Detecta qualquer mutação
def test_quality_increases():
    result = update_quality(25)
    assert result == 26  # ← Exato! Qualquer mudança falha
```

---

## 📊 Métricas de Stryker

### Kill Rate (Taxa de Morte de Mutantes)

```
Mutantes Detectados pelos Testes
────────────────────────────── = Kill Rate
Total de Mutantes Gerados
```

### Exemplo

```
✅ 95 mutantes mortos (detectados pelos testes)
❌  5 mutantes sobreviventes (não detectados)
─────────────────────────────────────────────
Kill Rate = 95/100 = 95% 🏆 EXCELENTE!
```

### Benchmark da Indústria

| Kill Rate | Nível | Status |
|-----------|-------|--------|
| < 50% | ❌ Crítico | Testes muito fracos |
| 50-70% | ⚠️ Alerta | Testes com lacunas |
| 70-85% | ✅ Bom | Testes competentes |
| 85-95% | 🌟 Excelente | Testes de alta qualidade |
| > 95% | 🏆 Profissional | Testes exemplares |

---

## 🚀 Instalação e Configuração

### 1. Instalar Stryker (cosmic-ray)

```bash
pip install cosmic-ray
```

Já incluído em `requirements.txt`

### 2. Configurar `.cosmic-ray.toml`

```toml
[cosmic-ray]
module-path = gilded_rose        # Arquivo a testar
test-runner = pytest             # Framework de testes
tests-dir = tests/               # Diretório de testes
timeout = 10.0                   # Timeout por teste
exclude-files = conftest.py,__pycache__  # Excludir
```

### 3. Executar Stryker

```bash
# Script shell
cd python
./run_stryker.sh

# Ou comando direto
cosmic-ray init .cosmic-ray.toml
cosmic-ray exec tests/test_gilded_rose.py
cosmic-ray report
```

---

## 📈 Tipos de Mutantes Gerados

### Operadores de Mutação

| Tipo | Exemplo | Mutante |
|------|---------|---------|
| **Aritmético** | `x + 1` | `x - 1`, `x * 2` |
| **Comparação** | `x < 50` | `x <= 50`, `x > 50` |
| **Lógica** | `a and b` | `a or b`, `not a` |
| **Atribuição** | `x = 5` | `x = 0`, `x = -1` |
| **Return** | `return x` | `return None`, `return 0` |
| **Delete** | `x = 5` | `pass` (removido) |

---

## 🎯 Interpretação de Resultados

### Status dos Mutantes

```
KILLED (🟢):
├─ Teste detectou alteração
├─ Teste passou com original
└─ Teste falhou com mutante
└─ RESULTADO: BOM! ✅

SURVIVED (🔴):
├─ Teste não detectou alteração
├─ Teste passou com AMBOS (original e mutante)
└─ RESULTADO: TESTE FRACO! ❌

SKIPPED (⚫):
├─ Mutante não aplicável
└─ Exemplo: Remover comentário

TIMEOUT (🟡):
├─ Mutante causou loop infinito
└─ Pode indicar bug no código
```

---

## 📊 Exemplo de Relatório Stryker

```
Mutation Score: 85/100 = 85% ✅

KILLED:    85 (detectados)
SURVIVED:  10 (não detectados)
SKIPPED:    3 (não aplicáveis)
TIMEOUT:    2 (loop infinito)
────────────────────────────
TOTAL:    100 mutantes

Arquivo: gilded_rose.py
├─ update_quality(): 92% kill rate ✅
├─ apply_quality_change(): 85% kill rate ✅
├─ Item.__init__(): 75% kill rate ⚠️
└─ GildedRose.update_quality(): 90% kill rate ✅
```

---

## 🔄 Workflow Completo com Stryker

### Teste Local

```bash
# 1. Executar testes normais
cd python
python3 -m pytest tests/test_gilded_rose.py -v

# 2. Verificar cobertura (JaCoCo)
python3 -m pytest tests/ --cov=gilded_rose --cov-branch

# 3. Executar Stryker (mutation testing)
./run_stryker.sh

# 4. Ver relatórios
cosmic-ray report
```

### Resultado Esperado

```
════════════════════════════════════════════
✅ Testes: 77 passed
✅ Coverage: 97% linha, 100% branch
✅ Stryker: 85-95% kill rate 🌟
════════════════════════════════════════════
✨ CÓDIGO PRONTO PARA PRODUÇÃO! ✨
════════════════════════════════════════════
```

---

## 🛠️ Como Melhorar Kill Rate

### 1. Validar Valores Exatos

```python
# ❌ FRACO
assert result > 0

# ✅ FORTE
assert result == 26  # Valor exato
```

### 2. Testar Limites Precisamente

```python
# ❌ FRACO
assert quality <= 50

# ✅ FORTE
assert quality == 50   # Limite superior
assert quality == 49   # Abaixo do limite
assert quality == 0    # Limite inferior
```

### 3. Testar Efeitos Colaterais

```python
# ❌ FRACO - Só verifica quality
quality = update_quality(quality)

# ✅ FORTE - Verifica tudo
items = [Item(...)]
gilded_rose.update_quality(items)
assert items[0].quality == expected
assert items[0].sell_in == expected_sell_in
```

### 4. Usar Parametrização Extensa

```python
@pytest.mark.parametrize("input,expected", [
    (0, 0),      # Limite
    (1, 0),      # Transição
    (49, 48),    # Normal
    (50, 49),    # Limite
])
def test_quality(input, expected):
    assert update_quality(input) == expected
```

---

## 🎯 Expectativas para Gilded Rose

### Kill Rate Esperado: **85-95%** 🌟

**Por quê?**
- ✅ **100% branch coverage** - Todos os caminhos testados
- ✅ **77 testes parametrizados** - Muitos casos cobertos
- ✅ **Boundary testing** - Limites validados
- ⚠️ **5-15% pode sobreviver** - Normal (não crítico)

### Possíveis Sobreviventes

1. **Operadores Aritméticos**: `+1` vs `-1` em bordas
2. **Comparadores**: `<` vs `<=` em casos não testados
3. **Constantes Mágicas**: Se não validadas exatamente
4. **Reordenação**: Se não afetar resultado

---

## 📚 Integração em CI/CD

### GitHub Actions

```yaml
- name: Mutation Testing (Stryker)
  run: |
    cd python
    pip install cosmic-ray
    cosmic-ray init .cosmic-ray.toml
    cosmic-ray exec tests/test_gilded_rose.py
    cosmic-ray report
```

### GitLab CI

```yaml
mutation_testing:
  stage: test
  script:
    - cd python
    - pip install cosmic-ray
    - cosmic-ray init .cosmic-ray.toml
    - cosmic-ray exec tests/
    - cosmic-ray report
  artifacts:
    reports:
      junit: cosmic-ray-report.xml
```

---

## 💡 Melhores Práticas

### 1. Executar Regularmente
- Semanalmente no mínimo
- Rastrear tendências
- Alertar se cair abaixo de 80%

### 2. Investigar Sobreviventes
```bash
# Ver mutante específico
cosmic-ray show-mutant ID
```

### 3. Documentar Decisões
- Por que mutante sobrevivente não é crítico?
- Qual teste foi adicionado para detectá-lo?

### 4. Combinar Métricas

| Ferramenta | Métrica | Peso |
|-----------|---------|------|
| **JaCoCo** | Coverage | 40% |
| **Stryker** | Kill Rate | 60% |

**Combinação ideal**: Coverage > 85% + Kill Rate > 85% = Confiança total ✅

---

## ✅ Status do Projeto

### Implementação Stryker

- ✅ cosmic-ray instalado
- ✅ .cosmic-ray.toml configurado
- ✅ run_stryker.sh criado
- ✅ Documentação completa
- ✅ Pronto para execução

### Próximas Ações

```bash
cd python
./run_stryker.sh
cosmic-ray report
```

---

## 📊 Conclusão

**Stryker (cosmic-ray) fornece:**
- ✅ Análise rigorosa de qualidade de testes
- ✅ Identificação de testes fracos
- ✅ Relatórios detalhados por mutante
- ✅ Integração com CI/CD
- ✅ Garantia de confiança

**Esperado para Gilded Rose**: Kill Rate **85-95%** 🏆

---

**Stryker implementado com sucesso!** 🧬✅
