# Corner Betting Bot — Sistema de Análise Quantitativa Ultra-Refinado

**Autor:** Manus AI

Este projeto implementa um sistema automatizado completo (bot) em Python para análise de apostas esportivas, focado exclusivamente no mercado de escanteios (cantos) no futebol. O sistema foi submetido a uma série de refinamentos avançados, elevando sua precisão, robustez e capacidade de aprendizado contínuo a um nível institucional.

## 1. Novas Funcionalidades e Refinamentos Avançados

O sistema evoluiu de um modelo básico de Poisson para uma plataforma de análise quantitativa de nível profissional, com as seguintes melhorias:

### 1.1. Refinamento de Precisão e Redução de Variância
*   **Fatores Dinâmicos:** Integração de posição na liga, forma recente (últimos 5 jogos) e fatores de motivação para ajustar as taxas de Poisson ($\lambda$).
*   **Score de Confiança Aprimorado:** O `confidence_score` (0-100) agora considera a consistência dos dados (desvio padrão), volume de jogos analisados e estabilidade das estimativas.
*   **Filtros de Qualidade:** Apostas em ligas de alta eficiência (ex: Premier League) exigem um EV mínimo superior para compensar a precisão do mercado.

### 1.2. Peso Dinâmico entre Modelo e Mercado & Segmentação por Liga (CRÍTICO)
O sistema agora ajusta dinamicamente a confiança entre a predição do modelo e a percepção do mercado (odds sharp) com base na eficiência da liga:
*   **`model_weight`:** Um fator (0.0 a 1.0) que determina o quanto o modelo confia em sua própria predição versus a probabilidade implícita do mercado. Em ligas mais eficientes (ex: Premier League), o peso do modelo é menor, pois o mercado é mais preciso. Em ligas ineficientes (ex: Brasileirão Série B), o peso do modelo é maior.
*   **Configurações por Liga:** Cada liga possui parâmetros próprios (`efficiency_factor`, `model_weight`, `volatility_factor`), permitindo que o sistema se adapte ao comportamento distinto dos escanteios em diferentes contextos geográficos e competitivos (ex: Brasil com mais variação, Europa mais estável).

### 1.3. Módulo de Backtesting e Monte Carlo (`backtester.py`)
*   **Validação Histórica:** Permite testar estratégias em dados passados para calcular ROI, Yield e Sharpe Ratio reais.
*   **Simulação de Monte Carlo:** Executa milhares de simulações de trajetórias de banca para estimar o **Risco de Ruína** e a variância esperada no longo prazo.
*   **Análise de Drawdown:** Monitoramento estatístico do maior declínio da banca para ajustar limites de stop-loss.

### 1.4. Otimização de CLV e Sharp Line Tracking
*   **Sharp Line Tracking:** O sistema monitora as odds de casas "sharp" (como Pinnacle e Betfair Exchange) para identificar a "linha real" do mercado.
*   **Cálculo de CLV (Closing Line Value):** Compara a odd apostada com a odd de fechamento das casas sharp. O modelo prioriza apostas que maximizam o CLV, o principal indicador de lucratividade sustentável.
*   **Line Movement Score:** Integra a movimentação das odds no score final da aposta. Odds caindo após a detecção de valor aumentam a confiança na entrada.

### 1.5. Timing Automático de Entrada
O bot agora decide o momento ideal para realizar a aposta, considerando a análise de mercado e o tempo restante para o início do jogo:
*   **Entrada Early:** Se houver distorção de mercado e movimento de linha favorável com mais de 24 horas para o jogo.
*   **Entrada Pré-Jogo:** Se houver movimento favorável entre 2 e 24 horas antes do jogo, ou se a odd estiver próxima da linha sharp nas últimas 2 horas.
*   **Monitoramento Contínuo:** Caso as condições não sejam ideais para entrada imediata, o sistema continua monitorando o mercado.

### 1.6. Detecção de "Fake Value"
Um filtro avançado foi implementado para evitar apostas com EV alto, mas com baixa confiabilidade:
*   **Penalização de EV:** O sistema penaliza oportunidades com EV alto se a confiança for baixa, os dados históricos forem insuficientes ou inconsistentes, ou se a linha do mercado parecer mal formada (ex: odds muito discrepantes entre casas).
*   **Thresholds Rigorosos:** Os limites para classificação de confiança (Alta, Média, Baixa) foram ajustados para serem mais rigorosos, descartando apostas de baixíssima confiança.

### 1.7. Otimização de Stake por Volatilidade
O Critério de Kelly fracionado agora é ajustado pela volatilidade da liga:
*   **`volatility_factor`:** Um fator (0.0 a 1.0) que indica a volatilidade esperada de escanteios em uma liga. Em ligas mais voláteis, o stake é reduzido para mitigar o risco. Em ligas mais estáveis, o stake pode ser ligeiramente maior.
*   **Ajuste Dinâmico:** O stake final é multiplicado por um fator de ajuste de volatilidade, que pode reduzir o stake base em até 50% em cenários de alta volatilidade.

### 1.8. Análise de Erro Automática (`post_game_analyzer.py`)
Após cada aposta, o bot realiza uma análise automática para aprendizado contínuo:
*   **Comparação Pós-Jogo:** Compara o resultado real de escanteios com as predições do modelo e o resultado da aposta.
*   **Classificação de Erro:** Identifica se o desvio foi devido à variância estatística normal ou a uma falha na modelagem, fornecendo insights para futuros ajustes.
*   **Resumo de Aprendizado:** Gera um resumo periódico da performance do modelo, incluindo taxa de acerto e precisão, para auxiliar na otimização dos parâmetros.

## 2. Arquitetura do Sistema

A arquitetura modular garante separação de responsabilidades:

*   **`data_collector.py`:** Coleta de fixtures, estatísticas de times, classificações e odds (com suporte a API-Football e modo Demo).
*   **`statistical_model.py`:** Modelagem de Poisson, cálculo de EV, Critério de Kelly, classificação de confiança, peso dinâmico e ajuste de stake por volatilidade.
*   **`market_analyzer.py`:** Detecção de distorções, tracking de casas sharp, monitoramento de line movement, timing de entrada e gestão de banca.
*   **`backtester.py`:** Simulador histórico e motor de Monte Carlo.
*   **`post_game_analyzer.py`:** Módulo de análise pós-jogo e aprendizado contínuo.
*   **`report_generator.py`:** Geração de relatórios em TXT, Markdown e JSON.
*   **`bot.py`:** Orquestrador principal do pipeline diário.

## 3. Como Executar

### 3.1. Instalação
```bash
pip install -r requirements.txt
```

### 3.2. Execução do Bot (Modo Diário)
Para rodar a análise do dia com dados simulados:
```bash
python bot.py --demo --bankroll 1000
```

### 3.3. Execução do Backtest e Testes Integrados
Para validar os novos módulos e ver as métricas de performance:
```bash
python test_suite.py
```

## 4. Gestão de Risco Profissional
*   **Kelly Fracionado (25%):** Stake dinâmico baseado no edge e na probabilidade, agora ajustado pela volatilidade da liga.
*   **Limite de Exposição:** Máximo de 3% por aposta e 7.5% de exposição diária total.
*   **Stop-Loss Automático:** O sistema pausa se o drawdown atingir 15%, protegendo o capital contra variações extremas.

---
**AVISO:** Este sistema é uma ferramenta de análise quantitativa. Apostas envolvem risco financeiro. O uso deste software não garante lucros e deve ser feito com responsabilidade.
