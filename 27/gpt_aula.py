# Importações necessários
import torch
import torch.nn as nn
from torch.nn import functional as F

# parâmetros
batch_size = 16 # quantidade de sequências independentes que serão processadas em paralelo
block_size = 32 # máximo de tokens que o modelo pode ver
max_iters = 5000
eval_interval = 100
learning_rate = 1e-3
device = 'cuda' if torch.cuda.is_available() else 'cpu'
eval_iters = 200
n_embd = 64
n_head = 4
n_layer = 4
dropout = 0.0

torch.manual_seed(1337)

with open('27/input.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# aqui estão todos os caracteres únicos que ocorrem neste texto
chars = sorted(list(set(text)))
vocab_size = len(chars)
# cria um mapeamento de caracteres para inteiros
stoi = { ch:i for i,ch in enumerate(chars) }
itos = { i:ch for i,ch in enumerate(chars) }
encode = lambda s: [stoi[c] for c in s] # codificador: pega uma string, retorna uma lista de inteiros
decode = lambda l: ''.join([itos[i] for i in l]) # decodificador: pega uma lista de inteiros, retorna uma string

# Divisão de treino e teste
data = torch.tensor(encode(text), dtype=torch.long)
n = int(0.9*len(data)) # primeiros 90% serão treino, o restante será validação
train_data = data[:n]
val_data = data[n:]

# carregamento de dados
def get_batch(split):
    # gera um pequeno lote de dados de entradas x e alvos y
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    x, y = x.to(device), y.to(device)
    return x, y

@torch.no_grad()
def estimate_loss():
    out = {}
    model.eval()
    for split in ['train', 'val']:
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            X, Y = get_batch(split)
            logits, loss = model(X, Y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out

class Head(nn.Module):
    """ one head of self-attention """

    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        B,T,C = x.shape
        k = self.key(x)   # (B,T,C)
        q = self.query(x) # (B,T,C)
        # computa as pontuações de atenção ("afinidades")
        wei = q @ k.transpose(-2,-1) * C**-0.5 # (B, T, C) @ (B, C, T) -> (B, T, T)
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf')) # (B, T, T)
        wei = F.softmax(wei, dim=-1) # (B, T, T)
        wei = self.dropout(wei)
        # realiza a agregação ponderada dos valores
        v = self.value(x) # (B,T,C)
        out = wei @ v # (B, T, T) @ (B, T, C) -> (B, T, C)
        return out

class MultiHeadAttention(nn.Module):
    """ multiple heads of self-attention in parallel """

    def __init__(self, num_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
        self.proj = nn.Linear(n_embd, n_embd)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.dropout(self.proj(out))
        return out

class FeedFoward(nn.Module):
    """ a simple linear layer followed by a non-linearity """

    def __init__(self, n_embd):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),
            nn.ReLU(),
            nn.Linear(4 * n_embd, n_embd),
            nn.Dropout(dropout),
        )

    def forward(self, x):
        return self.net(x)

class Block(nn.Module):
    """ Transformer block: communication followed by computation """

    def __init__(self, n_embd, n_head):
        # n_embd: dimensão do embedding, n_head: o número de cabeças que queremos
        super().__init__()
        head_size = n_embd // n_head
        self.sa = MultiHeadAttention(n_head, head_size)
        self.ffwd = FeedFoward(n_embd)
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)

    def forward(self, x):
        x = x + self.sa(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x

# modelo bigram
class BigramLanguageModel(nn.Module):

    def __init__(self):
        super().__init__()
        # cada token lê diretamente os logits para o próximo token de uma tabela de consulta
        self.token_embedding_table = nn.Embedding(vocab_size, n_embd)
        self.position_embedding_table = nn.Embedding(block_size, n_embd)
        self.blocks = nn.Sequential(*[Block(n_embd, n_head=n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embd) # camada final de normalização
        self.lm_head = nn.Linear(n_embd, vocab_size)

    def forward(self, idx, targets=None):
        B, T = idx.shape

        # idx e targets são ambos tensores (B,T) de inteiros
        tok_emb = self.token_embedding_table(idx) # (B,T,C)
        pos_emb = self.position_embedding_table(torch.arange(T, device=device)) # (T,C)
        x = tok_emb + pos_emb # (B,T,C)
        x = self.blocks(x) # (B,T,C)
        x = self.ln_f(x) # (B,T,C)
        logits = self.lm_head(x) # (B,T,vocab_size)

        if targets is None:
            loss = None
        else:
            B, T, C = logits.shape
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)
            loss = F.cross_entropy(logits, targets)

        return logits, loss

    def generate(self, idx, max_new_tokens):
        # idx é um array (B, T) de índices no contexto atual
        for _ in range(max_new_tokens):
            # corta idx para os últimos block_size tokens
            idx_cond = idx[:, -block_size:]
            # obtém as previsões
            logits, loss = self(idx_cond)
            # foca apenas no último passo de tempo
            logits = logits[:, -1, :] # se torna (B, C)
            # aplica softmax para obter probabilidades
            probs = F.softmax(logits, dim=-1) # (B, C)
            # amostra da distribuição
            idx_next = torch.multinomial(probs, num_samples=1) # (B, 1)
            # anexa o índice amostrado à sequência em execução
            idx = torch.cat((idx, idx_next), dim=1) # (B, T+1)
        return idx

model = BigramLanguageModel()
m = model.to(device)
# imprime o número de parâmetros no modelo
print(sum(p.numel() for p in m.parameters())/1e6, 'M parâmetros')

# cria um otimizador PyTorch
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

for iter in range(max_iters):

    # de vez em quando avalia a perda nos conjuntos de treino e validação
    if iter % eval_interval == 0 or iter == max_iters - 1:
        losses = estimate_loss()
        print(f"passo {iter}: loss do treino {losses['train']:.4f}, loss da validacao {losses['val']:.4f}")

    # amostra um lote de dados
    xb, yb = get_batch('train')

    # avalia a perda
    logits, loss = model(xb, yb)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()

# gera a partir do modelo
context = torch.zeros((1, 1), dtype=torch.long, device=device)
print(decode(m.generate(context, max_new_tokens=2000)[0].tolist()))
