<div align="center">

![Offline Gym Banner](docs/screenshots/banner.jpg)

# Offline Gym

### Seu treino organizado. Seus registros no seu aparelho. Sem depender de internet.

O **Offline Gym** é um aplicativo completo para Android e iOS para planejar treinos, registrar séries e cargas, aprender a executar cada exercício com segurança, acompanhar calorias, passos, hábitos e a evolução do corpo — **100% gratuito, sem anúncios, sem login e funcionando offline**.

**Versão atual:** `v1.7.1` (build `13`) · [Novidades desta versão](RELEASE_NOTES.md) · Repositório: [github.com/LuanThierry/offline-gym](https://github.com/LuanThierry/offline-gym)

[🤖 Baixar para Android (.apk)](https://github.com/LuanThierry/offline-gym/releases/latest/download/Offline-Gym.apk) · [🍎 Baixar para iPhone (.ipa)](https://github.com/LuanThierry/offline-gym/releases/latest/download/Offline-Gym-iOS.ipa) · [📦 Todas as versões](https://github.com/LuanThierry/offline-gym/releases) · [🔒 Política de Privacidade](PRIVACY_POLICY.md) · [✉️ Suporte](mailto:luanthierry.suporte@gmail.com)

![Flutter](https://img.shields.io/badge/Flutter-app-02569B?logo=flutter&logoColor=white)
![Dart](https://img.shields.io/badge/Dart-language-0175C2?logo=dart&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-dados%20locais-003B57?logo=sqlite&logoColor=white)
![Android](https://img.shields.io/badge/Android-8.0%2B-3DDC84?logo=android&logoColor=white)
![iOS](https://img.shields.io/badge/iOS%20%2F%20iPhone-IPA%20Sideload-000000?logo=apple&logoColor=white)
![Offline-first](https://img.shields.io/badge/Privacidade-100%25%20Offline-6C5CE7)
![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-blue.svg)

</div>

---

## 👋 Sobre o projeto

O Offline Gym é um projeto pessoal e de código aberto **idealizado e desenvolvido por [Luan Thierry](https://github.com/LuanThierry)**: um app para levar para a academia que **não precisa de internet**, não pede cadastro em servidor, **não tem anúncios** e guarda tudo no próprio celular. Ele calcula cargas, descansos, recuperação muscular, calorias e hábitos diários localmente, e ensina a executar cada exercício com fotos e dicas para evitar lesão.

> **Em resumo:** abra, diga seu objetivo, idade, peso e altura, e o app monta seu plano, mostra o melhor exercício do dia, acompanha a recuperação de cada músculo no corpo e o seu balanço de calorias — sem nenhum dado sair do aparelho.

---

## 🎬 Vídeos de apresentação
| [▶️ **Anúncio 1** — `Offline-Gym-Anuncio-Correto.mp4`](docs/Offline-Gym-Anuncio-Correto.mp4) | [▶️ **Anúncio 2** — `Offline-Gym-Anuncio-Correto2.mp4`](docs/Offline-Gym-Anuncio-Correto2.mp4) |


> Toque no link para abrir o vídeo no GitHub e use o botão **Download** (ou **View raw**) para assistir em tela cheia.

---

## 📸 Capturas de tela

<table align="center">
  <tr>
    <td align="center" width="33%"><img src="docs/screenshots/01_hoje.png" alt="Hoje — treino do dia e melhor exercício" width="100%"><br><sub><b>Hoje</b><br>Treino do dia + melhor exercício (Coach <code>!!</code>)</sub></td>
    <td align="center" width="33%"><img src="docs/screenshots/02_hoje_treino.png" alt="Hoje — treino em andamento" width="100%"><br><sub><b>Treino em andamento</b><br>Séries, cargas e ações rápidas</sub></td>
    <td align="center" width="33%"><img src="docs/screenshots/09_ajuste_carga.png" alt="Ajuste de carga e repetições" width="100%"><br><sub><b>Ajuste de carga</b><br>Botões de ±0,5 / ±2,5 kg e ±1 rep</sub></td>
  </tr>
  <tr>
    <td align="center" width="33%"><img src="docs/screenshots/03_guia_exercicio.png" alt="Guia de execução do exercício" width="100%"><br><sub><b>Guia do exercício (ⓘ)</b><br>Foto, passo a passo e como evitar lesão</sub></td>
    <td align="center" width="33%"><img src="docs/screenshots/04_corpo.png" alt="Corpo — mapa de recuperação" width="100%"><br><sub><b>Corpo</b><br>% de recuperação direto nos músculos</sub></td>
    <td align="center" width="33%"><img src="docs/screenshots/05_corpo_musculo.png" alt="Corpo — conselhos do músculo" width="100%"><br><sub><b>Conselhos do músculo</b><br>Séries semanais, combinações e exercícios</sub></td>
  </tr>
  <tr>
    <td align="center" width="33%"><img src="docs/screenshots/06_semana.png" alt="Semana — planos" width="100%"><br><sub><b>Semana</b><br>Planos e rotinas de cada dia</sub></td>
    <td align="center" width="33%"><img src="docs/screenshots/07_nutricao.png" alt="Nutrição — calorias do dia" width="100%"><br><sub><b>Nutrição</b><br>Consumiu, gastou, saldo e macros</sub></td>
    <td align="center" width="33%"><img src="docs/screenshots/08_historico.png" alt="Histórico — ofensiva e consistência" width="100%"><br><sub><b>Histórico</b><br>Ofensiva, consistência e evolução</sub></td>
  </tr>
</table>

<sub>Capturas geradas a partir do próprio app com dados de exemplo (sem dados pessoais), no tema escuro. Para regenerar: <code>GERAR_CAPTURAS=1 flutter test --update-goldens test/capturas</code>.</sub>

---

## ✨ Recursos e Funcionalidades (v1.7.1)

O app tem **5 abas**: **Hoje** (treino do dia, hábitos e tarefas), **Corpo** (mapa muscular, Coach e montagem do plano), **Semana** (planos), **Nutrição** (comida, calorias e passos) e **Histórico** (calendário, recordes, peso, medidas e fotos).

### 🧬 Tudo personalizado pelo seu cadastro

No primeiro acesso o app pede **sexo biológico, idade, peso e altura**. Com isso:

- **Coach:** o tempo de recuperação muscular se ajusta à idade (+15% a partir de 40 anos, +30% a partir de 55) e ao sexo (mulheres recuperam ~10% mais rápido entre sessões).
- **Co-piloto de plano:** menores de 18 e 55+ não recebem séries de força máxima (mínimo de 8 reps, esforço até RPE 8); 40+ ganham mais descanso; IMC ≥ 30 ou 55+ trocam exercícios de impacto e de carga pesada na coluna por equivalentes mais seguros (ex.: agachamento livre → leg press, barra fixa → puxada).
- **Guia `ⓘ`:** seção **Para você** com cuidados específicos para sua idade e IMC em cada exercício.
- **Nutrição:** metabolismo (Mifflin-St Jeor), metas de macros e água calculados com seus dados.
- **Mapa corporal:** mostra só o corpo do sexo escolhido.

### 📖 Guia ilustrado em todos os +2.000 exercícios

- **Foto real de execução (início → fim, animada)** em cerca de 85% dos exercícios, embutida no app (nada é baixado). Boxe, natação, pilates clássico e isometrias avançadas de calistenia usam animações vetoriais próprias.
- **Botão `ⓘ` neon** no treino, no catálogo e nos planos: passo a passo, respiração, **como evitar lesão**, erros comuns, músculos principais e sinergistas, articulações exigidas, dica de ouro, dicas da variação (drop-set, elástico, unilateral, cadência…) e volume semanal recomendado.

### 🧍 Aba Corpo — tudo sobre o seu corpo em um só lugar

- **Mapa anatômico** (frente e costas) com **% de recuperação escrito nos músculos** e modos **Volume (7d)** e **Simetria**.
- **Toque em um músculo** para ver exercícios recomendados na ordem ideal (academia ou em casa), o que combina com o quê, o que ele afeta, frequência e **séries semanais** (mínimo efetivo, faixa ideal e teto), com botão "adicionar ao meu plano".
- **Coach Fisiológico, Radar de Simetria e Volume Semanal por Músculo** ficam nesta aba.
- **Co-piloto de plano:** objetivo (hipertrofia, emagrecimento, força ou saúde), nível, dias por semana (2 a 6) e local → o Coach monta a divisão (Corpo Inteiro, Superior/Inferior ou PPL), escolhe exercícios, define séries/reps/descanso e explica cada decisão.

### 💎 Coach "Brilhante" (`!!`)

- Card **Melhor exercício de hoje** na aba Hoje, escolhido pelo objetivo, recuperação e volume da semana.
- **Revisão completa** no estilo de análise de partida de xadrez: nota da semana e classificação de cada músculo — `!!` brilhante, `!` excelente, `!?` atenção, `?` abaixo do ideal, `??` excesso/deload — com platôs e balanço nutricional.

### 🏋️ Treino sem atrito

- **Ajuste de carga por botões grandes** (−2,5 / −0,5 / +0,5 / +2,5 kg) e de repetições (±1). Segurar o botão repete e acelera. Sem teclado e sem roleta: rápido até em celulares simples.
- **Calculadora de anilhas por lado** com barra de 20, 15 ou 10 kg, avisando quando sobra peso sem anilha.
- **Barra de ações do exercício:** trocar (aparelho ocupado), ±série, calculadora de cargas/1RM e rampa de aquecimento em 1 toque.
- **Marcadores de série** (normal, aquecimento, drop-set, falha), bi-sets, notas fixadas de regulagem, *ghost values* da última sessão, cronômetro de descanso com contagem 3-2-1 e alarme com a tela bloqueada sem pausar sua música.

### 🥗 Aba Nutrição — consumiu, gastou e saldo do dia

- **+230 alimentos e refeições brasileiras** (TACO/TBCA/USDA) com porções caseiras, alimentos próprios e lançamento rápido só de kcal; refeições do dia e "repetir ontem".
- **Gasto do dia:** metabolismo + rotina, treinos concluídos e atividades extras por MET.
- **Saldo** (déficit/superávit explicado), macros, água em copos e tendência dos últimos 7 dias.

### 👟 Passos, Samsung Health e Google Fit (Health Connect)

- **Contador de passos** pelo sensor do celular, sem internet e sem conta, com meta diária.
- **Health Connect** (ponte oficial do Android usada por Samsung Health, Google Fit, Mi Fitness, Garmin e relógios): lê passos, calorias ativas e peso; grava os treinos concluídos e o peso. Tudo opcional, em **Configurações › Integrações & passos**.
- **Samsung Health:** em Samsung Health › Configurações › Health Connect, permita a sincronização. O **Google Fit** já envia ao Health Connect automaticamente.

### 🧠 Ciência do treino

- **Estimativa de recuperação por músculo** ponderada pelo volume e RPE da última sessão.
- **Volume semanal (MEV/MAV/MRV)** por grupo, com sinergistas contando meia série.
- **Deload reversível em 1 toque**, detecção de platôs e check-in de prontidão (sono, energia, dor).
- **Compartilhamento de ficha offline** por código `OGYM1` ou QR Code, e **importador CSV** de Strong, Hevy e do próprio Offline Gym.

### 🎨 Personalização, hábitos e evolução

- **11 paletas neon**, seletor livre de cores, tema claro/escuro e **modo AMOLED** (#000000).
- **17 sons de cronômetro** sintetizados e vibração configurável.
- **Hábitos e tarefas** do dia com ofensiva e escudos.
- **Medidas corporais**, peso, **fotos de evolução** com comparador antes/depois, diário de treino e **relatórios em PDF/CSV** gerados no aparelho.
- **Backup criptografado** (`.ogb`, AES-256-GCM + Argon2id) e PIN local opcional.

---

## 🔐 Assinatura, privacidade e publicação

O repositório não contém `android/key.properties`, `.jks`, `.keystore`, senhas, tokens ou backups reais. O build de release do Android falha de propósito sem uma assinatura válida, o que impede assinar um APK de produção com a chave de debug.

Para o build local, mantenha a chave fora do Git e configure `android/key.properties` ou as variáveis `ANDROID_KEYSTORE_PATH`, `ANDROID_KEY_ALIAS`, `ANDROID_KEY_PASSWORD` e `ANDROID_STORE_PASSWORD`. No GitHub Actions, o workflow roda `flutter analyze` e `flutter test` e gera o pacote iOS (`.ipa` não assinado, para sideload pessoal).

O app é offline-first: dados de treino, saúde e backups ficam no armazenamento privado do app e o backup automático do Android está desativado. Para levar um backup a outro aparelho, use a exportação protegida por senha.

---

## 📥 Downloads

- **Android:** [Baixar `Offline-Gym.apk`](https://github.com/LuanThierry/offline-gym/releases/latest/download/Offline-Gym.apk) — Android 8.0 ou superior. *(Em breve também na Google Play.)*
- **iPhone (iOS):** [Baixar `Offline-Gym-iOS.ipa`](https://github.com/LuanThierry/offline-gym/releases/latest/download/Offline-Gym-iOS.ipa) — instalação por sideload (passo a passo abaixo).

### ⚠️ Para quem já usa uma versão anterior

Atualizar por cima mantém seus dados. Se você usa uma versão muito antiga (anterior à **1.1.0**, que tinha outro identificador), faça antes:

1. No app antigo, **Configurações → Exportar backup** e guarde o arquivo `.ogb`.
2. Instale o novo Offline Gym.
3. No novo app, **Configurações → Importar backup**.

[⭐ Apoie com uma estrela no GitHub](https://github.com/LuanThierry/offline-gym) · [💖 Apoie o criador via LivePix (PIX)](https://livepix.gg/luanthierry)

---

## 📱 Como Baixar e Instalar no seu iPhone (Guia Simples para Leigos)

Diferente do Android, a Apple não permite que aplicativos sejam baixados diretamente do navegador Safari sem passar pela App Store oficial. Porém, existe uma forma **100% gratuita, oficial e segura** chamada _Sideloading_ (instalação pessoal autorizada pela própria Apple).

O arquivo de instalação do iPhone é o **`.ipa`** (que é o equivalente ao `.apk` do Android).

### 🚀 Método 1: No Windows ou macOS (Com o programa gratuito Sideloadly)

Este é o método mais fácil e recomendado para quem usa computador com Windows ou Mac:

1. **Baixe o arquivo do aplicativo:**  
   No seu computador ou celular, baixe o arquivo [**`Offline-Gym-iOS.ipa`**](https://github.com/LuanThierry/offline-gym/releases/latest/download/Offline-Gym-iOS.ipa).
2. **Instale o Sideloadly no seu computador:**  
   Acesse o site oficial [sideloadly.io](https://sideloadly.io/) e baixe a versão para Windows ou Mac. Instale e abra o programa.
3. **Conecte seu iPhone no computador:**  
   Plugue o iPhone no computador usando o cabo USB (o mesmo do carregador). Se o iPhone perguntar _"Confiar neste computador?"_, toque em **Confiar** e digite o código de desbloqueio da tela.
4. **Instale o app pelo Sideloadly:**
   - Arraste o arquivo `Offline-Gym-iOS.ipa` para dentro da tela do Sideloadly.
   - No campo **Apple ID**, digite o seu e-mail da Apple (o mesmo que você usa no iPhone).
   - Clique no botão verde **Start**. (O Sideloadly pedirá sua senha da Apple apenas para assinar o app diretamente nos servidores da Apple com seu perfil gratuito de usuário).
   - Aguarde aparecer a mensagem **Done!** (o ícone do Offline Gym aparecerá na tela do seu iPhone).
5. **Autorize o app a abrir no iPhone (Apenas no primeiro uso):**
   - No seu iPhone, abra o aplicativo **Ajustes** (Configurações).
   - Vá em **Geral → Gestão de VPN e Dispositivos** (ou _Gerenciamento de Dispositivos_).
   - Toque no seu e-mail Apple que aparece na lista e clique em **"Confiar em [Seu E-mail]"**.
   - _(Se o seu iPhone estiver no iOS 16 ou superior)_: Vá em **Ajustes → Privacidade e Segurança**, role até o fim da página, toque em **Modo Desenvolvedor** e ative-o (o iPhone reiniciará uma vez).
6. **Pronto!** O Offline Gym está pronto para abrir e usar na academia com zero internet!

---

### 🐧 Método 2: No Linux (Ubuntu, Debian, Fedora, Arch, Pop!\_OS, Mint)

Se o seu computador roda Linux, você também pode assinar e instalar o `Offline-Gym-iOS.ipa` no seu iPhone de forma 100% gratuita usando ferramentas de terminal open-source:

#### Passo 1: Instale o suporte a USB do iPhone no Linux

Abra o terminal da sua distribuição Linux e instale o pacote `usbmuxd` (serviço que comunica o Linux com dispositivos iOS):

```bash
# No Ubuntu, Debian, Pop!_OS e Linux Mint:
sudo apt update && sudo apt install -y usbmuxd libimobiledevice6 libimobiledevice-utils

# No Fedora e RHEL:
sudo dnf install -y usbmuxd libimobiledevice libimobiledevice-utils

# No Arch Linux e Manjaro:
sudo pacman -S usbmuxd libimobiledevice
```

Inicie o serviço de conexão USB:

```bash
sudo systemctl start usbmuxd
```

#### Passo 2: Conecte o iPhone e emparelhe

Conecte o iPhone na porta USB. Desbloqueie a tela do iPhone, toque em **"Confiar neste computador"** e execute no terminal:

```bash
idevicepair pair
```

_(Deve exibir uma mensagem de sucesso: `SUCCESS: Paired with device ...`)_.

#### Passo 3: Assine e instale com o AltServer-Linux

1. Baixe o [**AltServer-Linux** (Release oficial do NyaMisty)](https://github.com/NyaMisty/AltServer-Linux/releases) no seu Linux.
2. Baixe o arquivo [**`Offline-Gym-iOS.ipa`**](https://github.com/LuanThierry/offline-gym/releases/latest/download/Offline-Gym-iOS.ipa).
3. Dê permissão de execução e instale no iPhone:

```bash
chmod +x AltServer-x86_64
./AltServer-x86_64 -u $(idevice_id -l) -a seu-email@apple.com -p sua-senha Offline-Gym-iOS.ipa
```

O aplicativo será assinado pelo seu Apple ID gratuito e instalado instantaneamente no seu iPhone!

---

### 📲 Método 3: Direto pelo próprio iPhone (Sem precisar de PC toda semana)

- **Se você já utiliza o [SideStore](https://sidestore.io/) ou [AltStore](https://altstore.io/):**  
  Basta baixar o arquivo [**`Offline-Gym-iOS.ipa`**](https://github.com/LuanThierry/offline-gym/releases/latest/download/Offline-Gym-iOS.ipa) pelo Safari no iPhone, tocar no arquivo baixado e selecionar **"Abrir com SideStore / AltStore"**. O app será assinado e instalado direto no celular via Wi-Fi!
- **Se você utiliza o [TrollStore](https://github.com/opa334/TrollStore) (iOS compatíveis):**  
  Basta baixar o `.ipa` no Safari e tocar em **"Install with TrollStore"**. O app fica instalado para sempre, sem limite de 7 dias e sem precisar assinar novamente.

> 💡 **Dica de Ouro:** Para quem instala com o Apple ID gratuito (Métodos 1 e 2), a Apple concede 7 dias de assinatura. Ao final de 7 dias, basta reconectar o iPhone e clicar em "Start" (ou rodar o comando) novamente para renovar — todos os seus treinos, dados e histórico permanecem 100% salvos e intactos!

---

## 🤖 Como Baixar e Instalar no Android

1. Abra a página de [Releases](https://github.com/LuanThierry/offline-gym/releases).
2. Baixe o arquivo [**`Offline-Gym.apk`**](https://github.com/LuanThierry/offline-gym/releases/latest/download/Offline-Gym.apk).
3. Abra o arquivo baixado no seu celular. Se o Android perguntar se você autoriza a instalação de fontes desconhecidas do seu navegador/gerenciador de arquivos, toque em **Permitir**.
4. Toque em **Instalar** e abra o Offline Gym!

---

---

## 🛠️ Seção Técnica: Arquitetura, Engenharia e Compilação

Esta seção detalha as escolhas de engenharia, arquitetura de software e automação de compilação do projeto.

### 🏛️ Estrutura Arquitetural

O projeto adota princípios pragmáticos de **Clean Architecture** com separação explícita de responsabilidades em camadas desacopladas:

```text
lib/
├── banco_dados/    # Camada de Persistência SQLite nativa (DatabaseHelper, migrações e índices)
├── modelos/        # Data Transfer Objects (DTOs) com serialização/desserialização JSON e Map
├── dominio/        # Regras de negócio puras (Coach fisiológico, volume muscular, gamificação)
├── servicos/       # Serviços locais do dispositivo (Áudios sintetizados, criptografia, backups)
├── provedores/     # Gerenciamento de estado reativo unificado via Provider (ChangeNotifier)
├── componentes/    # Widgets reutilizáveis, modais, gráficos de radar e seletores customizados
├── telas/          # Views estruturadas das abas principais e fluxos de navegação
├── versao_do_app.dart # Versão exibida no app (testada contra o pubspec)
└── main.dart       # Ponto de entrada, injeção de dependências e configuração de temas
```

### 🔒 Persistência e Segurança Criptográfica

- **Armazenamento Primário:** Banco de dados relacional SQLite nativo via `sqflite` (schema `v18`, com as tabelas de nutrição), com índices compostos em chaves estrangeiras, whitelist estrita de colunas na restauração (**anti-SQLi**) e isolamento contra backup automático em nuvem (`allowBackup="false"` no Android e `NSURLIsExcludedFromBackupKey` no iOS).
- **Criptografia Autenticada de Backups (`OGYMBKP2`):** Backups `.ogb` são gerados em `Isolate` dedicado utilizando o pacote `cryptography` (mantendo retrocompatibilidade total de leitura com `OGYMBKP1`):
  - **KDF:** Derivação de chave segura com **Argon2id** (memória: 19 MiB / 19.456 KiB conforme recomendação OWASP, paralelismo: 1, iterações: 2, salt criptográfico aleatório de 16 bytes via CSPRNG).
  - **Cifra:** **AES-256-GCM** com nonce aleatório de 12 bytes, cabeçalho KDF autenticado via **AAD** (*Additional Authenticated Data*), tag de integridade de 16 bytes, limpeza explícita de buffers sensíveis em RAM e proteção **anti-ZIP Bomb** na restauração.
- **Segurança Local Opcional no Aparelho:** Bloqueio opcional por **PIN Criptográfico Local** (4 a 8 dígitos derivados com Argon2id + comparação em tempo constante + backoff exponencial), bloqueio de capturas de tela (`FLAG_SECURE` no Android) e cortina de privacidade no seletor de apps recentes (*App Switcher*).

### 📊 Algoritmos e Biomecânica Computacional

- **Estimativa de Força Máxima (1RM):** Fórmulas combinadas de **Epley** $\text{1RM} = w \cdot (1 + \frac{r}{30})$ e **Brzycki** $\text{1RM} = w \cdot \frac{36}{37 - r}$ para suavização de dispersão estatística em repetições entre 1 e 12.
- **Equilíbrio Muscular Posterior vs Quadríceps:** Avaliação biomecânica da proporção funcional flexor/extensor para distribuição equilibrada de cargas articulares e harmonia no desenvolvimento de pernas.
- **Taxa Metabólica Basal (TMB):** Equação **Mifflin-St Jeor** ponderada por sexo, peso, altura e idade, multiplicada por fatores de atividade física validados pela literatura de fisiologia do esporte.

## 🛡️ Segurança, Privacidade e Seus Dados

- **Zero rastreamento:** O aplicativo não inclui Firebase Analytics, Google Ads, Crashlytics ou qualquer biblioteca de telemetria.
- **Sem servidores intermediários:** Seus dados nunca saem do seu aparelho sem sua ação explícita de exportar um backup.
- **Isolamento de permissões:** O aplicativo não solicita permissão de acesso à internet nos manifestos do Android e iOS. As permissões de Galeria e Câmera são opcionais e solicitadas apenas se você decidir tirar fotos de evolução.
- **Passos e Health Connect são opcionais:** `ACTIVITY_RECOGNITION` só é pedida quando você ativa o contador de passos, e as permissões do Health Connect só quando você toca em "Conectar". A troca acontece entre apps do próprio celular; nada vai para servidores. Detalhes em [PRIVACY_POLICY.md](PRIVACY_POLICY.md).

---

### 🧪 Qualidade e ferramentas

Projeto idealizado e desenvolvido por Luan Thierry, com apoio de ferramentas de IA
(assistentes de código) em partes da implementação, dos testes e da revisão. Todo o código
passa por `flutter analyze` sem avisos e por mais de 170 testes automatizados — incluindo a
navegação completa do app em telas pequenas e grandes, a auditoria das fórmulas (TMB,
macros, 1RM, MET) e a verificação de que todos os +2.000 exercícios têm guia e imagem.

### 🖼️ Créditos de conteúdo

- **Fotos de execução dos exercícios:** [free-exercise-db](https://github.com/yuhonas/free-exercise-db) (yuhonas) — domínio público (The Unlicense).
- **Traçados do mapa corporal:** [MuscleMap](https://github.com/melihcolpan/MuscleMap) de Melih Colpan (MIT), na mesma conversão usada pelo [openGym](https://github.com/alexpcosta/opengym).
- **Tabela de alimentos:** médias públicas TACO / TBCA / USDA.
- Textos completos das licenças em [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

### 🤝 Agradecimentos e Ferramentas Open-Source

A distribuição gratuita da versão iOS e a compatibilidade multiplataforma com Linux são viabilizadas pelo trabalho de projetos abertos da comunidade aos quais deixamos nosso reconhecimento:

- [**libimobiledevice**](https://libimobiledevice.org/) & [**usbmuxd**](https://github.com/libimobiledevice/usbmuxd) — bibliotecas fundamentais que permitem ao Linux comunicar com o iPhone via USB.
- [**AltServer-Linux (NyaMisty)**](https://github.com/NyaMisty/AltServer-Linux) & [**SideStore**](https://sidestore.io/) — ferramentas que tornam possível assinar pacotes `.ipa` em distribuições Linux e direto no iPhone sem fios.
- [**Sideloadly**](https://sideloadly.io/) — solução descomplicada para instalação pessoal no Windows e Mac.
- [**subosito/flutter-action**](https://github.com/subosito/flutter-action) — automação de compilação multiplataforma no GitHub Actions.

---

## 👤 Criador, Autoria e Licença

- **Criador e Desenvolvedor:** **Luan Thierry** ([@LuanThierry](https://github.com/LuanThierry))
- **E-mail de Contato & Suporte Oficial:** [luanthierry.suporte@gmail.com](mailto:luanthierry.suporte@gmail.com)
- **Como Apoiar:** Se o aplicativo ajuda nos seus treinos e rotina diária, considere apoiar voluntariamente o projeto pelo [**LivePix (`livepix.gg/luanthierry`)**](https://livepix.gg/luanthierry) ou deixando uma **Estrela (⭐)** aqui no GitHub!

O código-fonte está licenciado sob a licença [MIT](LICENSE). Consulte [`docs/LICENCA_E_DADOS.md`](docs/LICENCA_E_DADOS.md) para detalhes sobre dados locais, backups e chaves de compilação.

---

<div align="center">
  <b>Offline Gym</b> — Feito por quem treina, para quem treina. 💪
</div>
