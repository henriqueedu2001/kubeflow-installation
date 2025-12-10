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

**Clonar Repositório de manifests do Kubeflow**
```bash
git clone https://github.com/kubeflow/manifests.git
cd manifests
```

**Instalar a Plataforma**
```bash
while ! kustomize build example | kubectl apply --server-side --force-conflicts -f -; do
  echo "Retrying to apply resources"
  sleep 20
done
```
Este comando demora, então aguarde cerca de 10 min. Após verifique os pods com o comando: 

```bash
kubectl get pods -A
```
Caso tenha algum pod com `Creating`, `CrashLoopBackOf` ou algo semelhante espere alguns minutos para eles se normalizarem !!

# Acesso ao kubeflow

**Acesso ao dashboard completo**
```bash
kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80
```

Usuário padrão: user@example.com
Senha padrão: 12341234

**Acesso ao Kubeflow Pipelines**
```bash
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```

# Como criar um Pipeline

**Instalar Pacote para .env (Caso ainda não esteja instalada)**
```bash
sudo apt install python3-venv -y
```

**Criar ambiente virtual (Caso ainda não criada)**
```bash
python3 -m venv kfp-env
```

**Ativar**
```bash
source kfp-env/bin/activate
```
o retorno será `(kfp-env) user@vm:~`

**Instalar versão KFP (Caso ainda não esteja instalada)**
```bash
pip install kfp==2.14.3
```

ou

```bash
pip install kfp
```

**Criar um arquivo .py com o pipeline dentro**
```bash
vim exemplo.py
```

**Gerar Pipeline**
```bash
python3 exemplo.py
```

**Verificar se geroul .YAML**
```bash
ls
```
O retorno deve terum arquivo YAML

### Baixar Arquivo YAML da VM
Caso você tenha feito o arquivo .YAML através do **Asimov** você precisará baixa-lo em sua maquina pra conseguir coloca-lo em um pipeline no **Kubeflow**.

**Baixar**
```bash
scp -P PORTA_VM oper@IP_DA_VM:/home/oper/exemplo.yaml .
```

### Criar e Rodar um Pipeline no Kubeflow 
Vá até Pipelines no menu lateral 
!imagem

**Upload Pipeline**
!imagem

**Criar Pipeline**
Coloque o nome do pipeline e uma descrição 
!imagem

Faça o Upload do arquivo .YAML e clique em criar
!imagem

**Experiments**
Ir até Experiments no menu lateral 
!imagem

**Create Experiment**
!imagem

**Criar Experiment**
Coloque o nome do experiment e uma descrição 
!imagem

**Detalhes**
Escolha o Pipeline já criado anteriormente
!imagem

De um nome e descrição para a Run
!imagem

Caso tenha parâmetros coloca-los (Imagem de Exemplo apenas)
!imagem

Só apertar em start e já  irá começar a run
!imagem

# Erros Encontrados

### Recursos Necessários
Para utilização do você precisa dos seguintes recursos computacionais:

- 8 CPUs
- 60GB RAM

Sem isso os nós eles não sobem e você nunca conseguira subir o Kubeflow completo. (Caso queira alguns componentes é melhor pesquisar quanto é necessário pra cada um)

### Snap
Na instalação de cada um dos requisitos evite de instalar através do snap, pois a instalação não vem corretamente. 

### Tempo
A instalação do Kubeflow é bem demorada, então o ideal é que depois de rodar o comando de instalação esperar até que o comando seja finalizado. Caso o comando demore mais de 15min a 20min é bem provavel que tenha dado erro em alguma parte da instalação.

### ErrPullImage
Esse erro acontece ao tentar fazer instalação apenas do componente de Kubeflow pipelines usando o addon do **minikube**. Esse erro acontece porque ele tenta puxar a imagem de um local que não a possui mais. (Não conseguimos resolver)

### CrashLoopBackOf
Erro indica que o pod nã foi iniciado corretamente. Acontece por dois motivos, o primeiro e mais provável é que esse pod depende de outro assim ele não inicia corretamente e o segundo pode ser uma falha dentro do pod. Para tentar descobrir onde está a falha de o seguinte comando `kubectl describe pod <nome-do-pod>` ou `kubectl logs <nome-do-pod> -n <namespace>`

