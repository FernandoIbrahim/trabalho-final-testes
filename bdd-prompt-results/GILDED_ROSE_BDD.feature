# language: pt-BR
Funcionalidade: Sistema de Inventário Gilded Rose
  Como gerente de inventário
  Quero que o sistema atualize automaticamente a qualidade e validade dos itens
  Para que eu possa controlar corretamente meu inventário

  Contexto:
    Dado que o sistema Gilded Rose está inicializado
    E possuo um inventário vazio

  # ============================================================================
  # NORMAL ITEMS - Items normais que degradam com o tempo
  # ============================================================================

  Cenário: Item normal com qualidade dentro dos limites
    Dado que tenho um item "Normal Item" com qualidade 25 e dias para vender 10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 24
    E os dias para vender devem ser 9

  Cenário: Item normal na qualidade máxima
    Dado que tenho um item "Normal Item" com qualidade 50 e dias para vender 10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 49
    E os dias para vender devem ser 9

  Cenário: Item normal na qualidade mínima não reduz abaixo de zero
    Dado que tenho um item "Normal Item" com qualidade 0 e dias para vender 10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 0
    E os dias para vender devem ser 9

  Cenário: Item normal com qualidade 1 (limite crítico)
    Dado que tenho um item "Normal Item" com qualidade 1 e dias para vender 10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 0
    E os dias para vender devem ser 9

  Cenário: Item normal expirado reduz qualidade em dobro
    Dado que tenho um item "Normal Item" com qualidade 10 e dias para vender -1
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 8
    E os dias para vender devem ser -2

  Cenário: Item normal expirado com qualidade 2 (limite crítico)
    Dado que tenho um item "Normal Item" com qualidade 2 e dias para vender -1
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 0
    E os dias para vender devem ser -2

  Cenário: Item normal expirado há muito tempo (qualidade não fica negativa)
    Dado que tenho um item "Normal Item" com qualidade 0 e dias para vender -10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 0
    E os dias para vender devem ser -11

  Cenário: Item normal evolução ao longo de 4 dias (antes e depois de expirar)
    Dado que tenho um item "Normal Item" com qualidade 10 e dias para vender 3
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 9
    E os dias para vender devem ser 2
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 8
    E os dias para vender devem ser 1
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 7
    E os dias para vender devem ser 0
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 5
    E os dias para vender devem ser -1

  # ============================================================================
  # AGED BRIE - Vinho que melhora com a idade (qualidade aumenta)
  # ============================================================================

  Cenário: Aged Brie aumenta em qualidade
    Dado que tenho um item "Aged Brie" com qualidade 25 e dias para vender 10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 26
    E os dias para vender devem ser 9

  Cenário: Aged Brie na qualidade mínima
    Dado que tenho um item "Aged Brie" com qualidade 0 e dias para vender 10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 1
    E os dias para vender devem ser 9

  Cenário: Aged Brie na qualidade máxima não excede o limite
    Dado que tenho um item "Aged Brie" com qualidade 50 e dias para vender 10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 50
    E os dias para vender devem ser 9

  Cenário: Aged Brie perto do limite máximo (qualidade 49)
    Dado que tenho um item "Aged Brie" com qualidade 49 e dias para vender 10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 50
    E os dias para vender devem ser 9

  Cenário: Aged Brie expirado aumenta qualidade em dobro
    Dado que tenho um item "Aged Brie" com qualidade 25 e dias para vender -1
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 27
    E os dias para vender devem ser -2

  Cenário: Aged Brie expirado não ultrapassa qualidade máxima
    Dado que tenho um item "Aged Brie" com qualidade 49 e dias para vender -1
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 50
    E os dias para vender devem ser -2

  Cenário: Aged Brie expirado com qualidade 48 (aumentaria para 50)
    Dado que tenho um item "Aged Brie" com qualidade 48 e dias para vender -1
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 50
    E os dias para vender devem ser -2

  Cenário: Aged Brie evolução ao longo de 4 dias (antes e depois de expirar)
    Dado que tenho um item "Aged Brie" com qualidade 10 e dias para vender 3
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 11
    E os dias para vender devem ser 2
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 12
    E os dias para vender devem ser 1
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 13
    E os dias para vender devem ser 0
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 15
    E os dias para vender devem ser -1

  # ============================================================================
  # BACKSTAGE PASSES - Ingressos que aumentam em valor conforme o show aproxima
  # ============================================================================

  Cenário: Backstage Pass com mais de 10 dias (aumento +1)
    Dado que tenho um item "Backstage passes to a TAFKAL80ETC concert" com qualidade 25 e dias para vender 11
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 26
    E os dias para vender devem ser 10

  Cenário: Backstage Pass com exatamente 10 dias (aumento +2)
    Dado que tenho um item "Backstage passes to a TAFKAL80ETC concert" com qualidade 25 e dias para vender 10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 27
    E os dias para vender devem ser 9

  Cenário: Backstage Pass com 6 a 10 dias (aumento +2)
    Dado que tenho um item "Backstage passes to a TAFKAL80ETC concert" com qualidade 25 e dias para vender 8
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 27
    E os dias para vender devem ser 7

  Cenário: Backstage Pass com exatamente 6 dias (aumento +2)
    Dado que tenho um item "Backstage passes to a TAFKAL80ETC concert" com qualidade 25 e dias para vender 6
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 27
    E os dias para vender devem ser 5

  Cenário: Backstage Pass com 5 dias (aumento +3)
    Dado que tenho um item "Backstage passes to a TAFKAL80ETC concert" com qualidade 25 e dias para vender 5
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 28
    E os dias para vender devem ser 4

  Cenário: Backstage Pass com 1 dia (aumento +3)
    Dado que tenho um item "Backstage passes to a TAFKAL80ETC concert" com qualidade 25 e dias para vender 1
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 28
    E os dias para vender devem ser 0

  Cenário: Backstage Pass expirado cai para qualidade zero
    Dado que tenho um item "Backstage passes to a TAFKAL80ETC concert" com qualidade 25 e dias para vender 0
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 0
    E os dias para vender devem ser -1

  Cenário: Backstage Pass muito expirado mantém qualidade zero
    Dado que tenho um item "Backstage passes to a TAFKAL80ETC concert" com qualidade 50 e dias para vender -5
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 0
    E os dias para vender devem ser -6

  Cenário: Backstage Pass na qualidade máxima com 10 dias (não ultrapassa 50)
    Dado que tenho um item "Backstage passes to a TAFKAL80ETC concert" com qualidade 49 e dias para vender 10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 50
    E os dias para vender devem ser 9

  Cenário: Backstage Pass com 5 dias e qualidade alta (não ultrapassa 50)
    Dado que tenho um item "Backstage passes to a TAFKAL80ETC concert" com qualidade 48 e dias para vender 5
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 50
    E os dias para vender devem ser 4

  Cenário: Backstage Pass evolução com aproximação do show
    Dado que tenho um item "Backstage passes to a TAFKAL80ETC concert" com qualidade 20 e dias para vender 15
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 21
    E os dias para vender devem ser 14
    Quando o sistema atualiza a qualidade 5 vezes
    Então a qualidade deve ser 26
    E os dias para vender devem ser 9
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 28
    E os dias para vender devem ser 8

  # ============================================================================
  # SULFURAS - Item lendário que nunca muda
  # ============================================================================

  Cenário: Sulfuras nunca muda qualidade nem validade
    Dado que tenho um item "Sulfuras, Hand of Ragnaros" com qualidade 80 e dias para vender 10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 80
    E os dias para vender devem ser 10

  Cenário: Sulfuras permanece inalterado mesmo após expiração
    Dado que tenho um item "Sulfuras, Hand of Ragnaros" com qualidade 80 e dias para vender -1
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 80
    E os dias para vender devem ser -1

  Cenário: Sulfuras com qualidade acima de 50 (especial para lendários)
    Dado que tenho um item "Sulfuras, Hand of Ragnaros" com qualidade 80 e dias para vender 0
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 80
    E os dias para vender devem ser 0

  Cenário: Sulfuras permanece inalterado após múltiplas atualizações
    Dado que tenho um item "Sulfuras, Hand of Ragnaros" com qualidade 80 e dias para vender 5
    Quando o sistema atualiza a qualidade 5 vezes
    Então a qualidade deve ser 80
    E os dias para vender devem ser 5

  # ============================================================================
  # CONJURED ITEMS - Itens Encantados (degradam 2x mais rápido)
  # ============================================================================

  Cenário: Conjured Item degrada duas vezes mais rápido que item normal
    Dado que tenho um item "Conjured Mana Cake" com qualidade 20 e dias para vender 10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 18
    E os dias para vender devem ser 9

  Cenário: Conjured Item na qualidade máxima
    Dado que tenho um item "Conjured Mana Cake" com qualidade 50 e dias para vender 10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 48
    E os dias para vender devem ser 9

  Cenário: Conjured Item na qualidade mínima não fica negativo
    Dado que tenho um item "Conjured Mana Cake" com qualidade 0 e dias para vender 10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 0
    E os dias para vender devem ser 9

  Cenário: Conjured Item com qualidade 1 (limite crítico)
    Dado que tenho um item "Conjured Mana Cake" com qualidade 1 e dias para vender 10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 0
    E os dias para vender devem ser 9

  Cenário: Conjured Item expirado degrada 4 vezes mais rápido
    Dado que tenho um item "Conjured Mana Cake" com qualidade 20 e dias para vender -1
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 16
    E os dias para vender devem ser -2

  Cenário: Conjured Item expirado não fica com qualidade negativa
    Dado que tenho um item "Conjured Mana Cake" com qualidade 1 e dias para vender -1
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 0
    E os dias para vender devem ser -2

  Cenário: Conjured Item evolução ao longo de múltiplos dias
    Dado que tenho um item "Conjured Mana Cake" com qualidade 20 e dias para vender 3
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 18
    E os dias para vender devem ser 2
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 16
    E os dias para vender devem ser 1
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 14
    E os dias para vender devem ser 0
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 10
    E os dias para vender devem ser -1

  # ============================================================================
  # MULTIPLE ITEMS - Múltiplos itens no inventário
  # ============================================================================

  Cenário: Múltiplos itens são atualizados independentemente
    Dado que tenho os itens no inventário:
      | Nome                                        | Qualidade | Dias |
      | Normal Item                                 | 20        | 10   |
      | Aged Brie                                   | 20        | 10   |
      | Backstage passes to a TAFKAL80ETC concert   | 20        | 10   |
      | Sulfuras, Hand of Ragnaros                  | 80        | 10   |
    Quando o sistema atualiza a qualidade
    Então o item "Normal Item" deve ter qualidade 19
    E o item "Aged Brie" deve ter qualidade 21
    E o item "Backstage passes to a TAFKAL80ETC concert" deve ter qualidade 22
    E o item "Sulfuras, Hand of Ragnaros" deve ter qualidade 80

  Cenário: Inventário vazio não causa erro
    Dado que tenho um inventário vazio
    Quando o sistema atualiza a qualidade
    Então nenhum erro deve ocorrer

  # ============================================================================
  # BOUNDARY CONDITIONS - Condições de limites extremos
  # ============================================================================

  Cenário: Item normal em todos os limites de qualidade
    Dado que tenho itens com qualidades "0", "1", "25", "49", "50" para item normal
    Quando o sistema atualiza todos os itens
    Então as qualidades devem ser "0", "0", "24", "48", "49"

  Cenário: Aged Brie em todos os limites de qualidade
    Dado que tenho itens com qualidades "0", "1", "25", "49", "50" para Aged Brie
    Quando o sistema atualiza todos os itens
    Então as qualidades devem ser "1", "2", "26", "50", "50"

  Cenário: Backstage Pass em transição crítica (5 dias)
    Dado que tenho um item "Backstage passes to a TAFKAL80ETC concert" com qualidade 48 e dias para vender 5
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 50
    E os dias para vender devem ser 4
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 50
    E os dias para vender devem ser 3

  Cenário: Item normal na beira da expiração (sell_in = 0)
    Dado que tenho um item "Normal Item" com qualidade 10 e dias para vender 0
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 8
    E os dias para vender devem ser -1

  # ============================================================================
  # QUALITY BOUNDS - Testes dos limites de qualidade
  # ============================================================================

  Cenário: Qualidade nunca fica negativa para nenhum item
    Dado que tenho um item "Normal Item" com qualidade 0 e dias para vender -5
    Quando o sistema atualiza a qualidade 10 vezes
    Então a qualidade deve ser 0

  Cenário: Qualidade nunca ultrapassa 50 para Aged Brie
    Dado que tenho um item "Aged Brie" com qualidade 40 e dias para vender -5
    Quando o sistema atualiza a qualidade 20 vezes
    Então a qualidade deve ser 50

  Cenário: Qualidade nunca ultrapassa 50 para Backstage Pass
    Dado que tenho um item "Backstage passes to a TAFKAL80ETC concert" com qualidade 40 e dias para vender 5
    Quando o sistema atualiza a qualidade 20 vezes
    Então a qualidade deve ser 50

  Cenário: Sulfuras pode ter qualidade diferente de 50
    Dado que tenho um item "Sulfuras, Hand of Ragnaros" com qualidade 80 e dias para vender 10
    Quando o sistema atualiza a qualidade
    Então a qualidade deve ser 80
