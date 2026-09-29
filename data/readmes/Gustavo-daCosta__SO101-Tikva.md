# LeRobot Docker Container

Container Docker baseado em Ubuntu 22.04 para executar o [LeRobot](https://github.com/huggingface/lerobot) da Hugging Face em qualquer computador.

## ⚡ CLI Customizado - Foco em Configuração de Hardware

Este container inclui um **CLI especializado em configuração de hardware** para facilitar o setup de robôs:

```bash
# 🔧 Comandos de Configuração (Principal)
lerobot find-ports              # Encontrar portas USB
lerobot find-cameras            # Encontrar câmeras
lerobot setup-motors            # Configurar motores
lerobot calibrate               # Calibrar robô/teleoperador
lerobot test-connection         # Testar conexão
lerobot robots                  # Listar dispositivos disponíveis
lerobot check-permissions       # Verificar permissões USB

# ⚙️ Teste Direto de Motores STServo (Fabricante)
lerobot motor-scan --port /dev/ttyUSB0              # Escanear motores
lerobot motor-ping --port /dev/ttyUSB0 --motor-id 1 # Testar conexão
lerobot motor-move --port /dev/ttyUSB0 --motor-id 1 --position 500
lerobot motor-change-id --current-id 1 --new-id 2   # Alterar ID
lerobot motor-test --port /dev/ttyUSB0 --motor-id 1 # Teste movimento

# 🚀 Comandos de Treinamento (Secundário)
lerobot train                   # Treinar modelos
lerobot eval                    # Avaliar modelos
lerobot visualize               # Visualizar datasets
```

### 📖 Documentação Completa

- **[CLI-ARCHITECTURE.md](CLI-ARCHITECTURE.md)** - 🏗️ **Arquitetura modular do CLI** (NOVO!)
- **[HARDWARE-CONFIG-GUIDE.md](HARDWARE-CONFIG-GUIDE.md)** - 🔧 Guia de configuração de hardware
- **[MOTOR-TESTING-GUIDE.md](MOTOR-TESTING-GUIDE.md)** - ⚙️ Guia de teste direto de motores
- **[CLI-GUIDE.md](CLI-GUIDE.md)** - Guia completo com todos os comandos

---

## 📋 Pré-requisitos

- Docker instalado (versão 20.10 ou superior)
- Docker Compose instalado (versão 1.29 ou superior)
- (Opcional) NVIDIA Docker para suporte a GPU

## 🚀 Instalação

### 1. Clonar ou criar o diretório do projeto

```bash
cd /home/guti/Documents/tikva-docker
```

### 2. Construir a imagem Docker

```bash
docker-compose build
```

Ou usando Docker diretamente:

```bash
docker build -t lerobot:latest .
```

## 💻 Uso

### Iniciar o container

```bash
docker-compose up -d
```

### Acessar o container

```bash
docker-compose exec lerobot /bin/bash
```

Ou usando Docker diretamente:

```bash
docker exec -it lerobot-container /bin/bash
```

### Parar o container

```bash
docker-compose down
```

## 📁 Estrutura de Diretórios

- `./data` - Datasets e dados de treinamento
- `./models` - Modelos treinados e checkpoints
- `./outputs` - Resultados e logs
- `./scripts` - Scripts personalizados

Esses diretórios são montados como volumes no container, permitindo persistência de dados.

## 🎯 Exemplos de Uso

### Usando o CLI (Recomendado) ⚡

```bash
# Ver informações do sistema e GPU
lerobot info

# Treinar um modelo
lerobot train --policy act --env aloha

# Avaliar um modelo
lerobot eval --policy act --env aloha

# Visualizar dataset
lerobot visualize --dataset lerobot/aloha_static_coffee

# Iniciar Jupyter Lab
lerobot jupyter
# Acesse: http://localhost:8888

# Iniciar TensorBoard
lerobot tensorboard
# Acesse: http://localhost:6006

# Listar modelos salvos
lerobot list

# Shell Python interativo
lerobot shell
```

📖 **[Guia Completo do CLI com todos os comandos](CLI-GUIDE.md)**

### Usando comandos diretos (Alternativa)

```bash
# Treinar
python -m lerobot.train policy=act env=aloha

# Avaliar
python -m lerobot.eval policy=act env=aloha

# Visualizar
python -m lerobot.visualize_dataset --repo-id lerobot/aloha_static_coffee
```

## 🎮 Usando com GPU (NVIDIA)

### Instalar NVIDIA Docker

```bash
# Ubuntu/Debian
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

### Verificar GPU no container

```bash
docker-compose exec lerobot nvidia-smi
```

## 🔧 Customização

### Adicionar dependências Python

Edite o arquivo `requirements.txt` e reconstrua a imagem:

```bash
docker-compose build --no-cache
```

### Modificar o Dockerfile

Edite o `Dockerfile` conforme necessário e reconstrua:

```bash
docker-compose build
```

## 📝 Notas

- O container usa Ubuntu 22.04 como base
- Python 3.10 está instalado por padrão
- Todas as dependências do LeRobot são instaladas automaticamente
- Suporte para GPU NVIDIA está configurado (requer NVIDIA Docker)
- Os dados são persistidos nos volumes montados

## 🐛 Troubleshooting

### Erro de permissão

Se encontrar erros de permissão nos volumes:

```bash
sudo chown -R $USER:$USER ./data ./models ./outputs ./scripts
```

### Container não inicia

Verifique os logs:

```bash
docker-compose logs lerobot
```

### GPU não detectada

Verifique se o NVIDIA Docker está instalado:

```bash
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

## 📚 Recursos Adicionais

- [Documentação do LeRobot](https://github.com/huggingface/lerobot)
- [Hugging Face Hub - LeRobot](https://huggingface.co/lerobot)
- [Docker Documentation](https://docs.docker.com/)

## 📄 Licença

Este container Docker é fornecido como está. O LeRobot possui sua própria licença - consulte o repositório oficial.
