# kubeflow-installation
Este repositório documenta como é feita a instalação do Kubeflow completo e como criar seu primeiro pipeline. Executando-se o script main.py, gera-se uma especificação de pipeline pipeline.yaml, que pode ser enviada para um backend de Kubeflow e executada nele em uma run.

O pipeline de exemplo é composto por um único componente `say_hello(name)`, que, munido de uma string `name`, imprime a string `Hello, <name>!`, conforme a implementação abaixo.

```python
@dsl.component
def say_hello(name: str) -> str:
    hello_text = f'Hello, {name}!'
    print(hello_text)
    return hello_text
```

# Instalação Kubeflow
Na instalação do Kubeflow primeiro é necessário a instalação de alguns componentes para termos o funcionamento completo da plataforma.


### Docker
Docker é uma ferramenta que nos permite executar aplicações em contêineres.

**Remover Versões Antigas** 
```bash
sudo apt remove docker docker-engine docker.io containerd runc
```

**Configurar Repositório**
```bash
sudo apt update
sudo apt install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

**Adicionar Repositório Docker**
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**Instalar Docker Engine**
```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

**Permitir rodar Docker sem Sudo**
```bash
sudo usermod -aG docker $USER
```

Agora reinicie seu sistema !!!

**Teste de Funcionamento**
```bash
docker run hello-world
```
O retorno será um Hello World e a criação de um conteiner. 

(Caso tenha algum erro na hora de tentar rodar o teste utilize o comando sudo ou volte para o Passo anterior ao Teste)

### Kubectl
Kubectl é uma ferramenta de linha de comando para controlar cluster Kubernetes

**Instalação**
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

**Verificar Instalação**
```bash
kubectl version --client
```
O retorno será o terminal mostrando a versão da ferramenta

### Kustomize
Kustomize é  uma ferramenta nativa do Kubernetes para personalizar arquivos de configuração YAWML sem usar modelos.

**Baixar aquivo**
```bash
curl -LO https://github.com/kubernetes-sigs/kustomize/releases/latest/download/kustomize_linux_amd64.tar.gz
tar -xvf kustomize_linux_amd64.tar.gz
chmod +x kustomize
```

**Mover para um local Global**
```bash
sudo mv kustomize /usr/local/bin/
rm kustomize_linux_amd64.tar.gz
```

**Verificar Instalação**
```bash
kustomize version
```

O retorno será o terminal mostrando a versão da ferramenta

### Kind
O Kind é uma ferramenta que executa cluster Kubernetes locais usando contêineres Docker.

**Instalação**
```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x kind
sudo mv kind /usr/local/bin/
```

**Verificar Instalação**
```bash
kind --version
```

O retorno será o terminal mostrando a versão da ferramenta

___

### Instalação da Plataforma Kubeflow

**Criar CLuster Kubernetes com Kind**
 ```bash
cat <<EOF | kind create cluster --name=kubeflow --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    image: kindest/node:v1.31.0
    kubeadmConfigPatches:
      - |
        kind: ClusterConfiguration
        apiServer:
          extraArgs:
            "service-account-issuer": "kubernetes.default.svc"
            "service-account-signing-key-file": "/etc/kubernetes/pki/sa.key"
EOF
```

**Verificar se contexto aponta para cluster Correto**
```bash
kubectl cluster-info --context kind-kubeflow
```
