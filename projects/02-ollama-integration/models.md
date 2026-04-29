# Available Ollama Models

## Quick Start

```bash
# Pull model
ollama pull mistral

# Run Ollama server
ollama serve
```

## Popular Models

### Mistral (Recommended)
```bash
ollama pull mistral
```
- **Size**: 7B parameters
- **Speed**: Fast ⚡
- **Quality**: High quality responses
- **Use case**: General purpose, coding, analysis
- **Memory**: ~4GB

### Neural Chat
```bash
ollama pull neural-chat
```
- **Size**: 7B parameters
- **Speed**: Fast ⚡
- **Quality**: Optimized for conversation
- **Use case**: Dialogue, customer service
- **Memory**: ~4GB

### Llama 2
```bash
ollama pull llama2
```
- **Variants**: 7B, 13B, 70B
- **Speed**: Medium to Slow (depends on variant)
- **Quality**: Very high quality
- **Use case**: General purpose, high-quality responses
- **Memory**: 4GB (7B), 8GB (13B), 40GB+ (70B)

### Orca Mini
```bash
ollama pull orca-mini
```
- **Size**: 3B parameters
- **Speed**: Very fast ⚡⚡
- **Quality**: Good for lightweight tasks
- **Use case**: Quick responses, low-resource systems
- **Memory**: ~2GB

### Yi
```bash
ollama pull yi
```
- **Size**: 6B, 34B parameters
- **Speed**: Medium
- **Quality**: High
- **Use case**: Programming, analysis
- **Memory**: ~4GB (6B)

## Model Performance Comparison

| Model | Size | Speed | Quality | Memory | Best For |
|-------|------|-------|---------|--------|----------|
| orca-mini | 3B | Very Fast | Good | 2GB | Fast responses |
| mistral | 7B | Fast | High | 4GB | General purpose |
| neural-chat | 7B | Fast | High | 4GB | Conversation |
| yi | 6B | Medium | High | 4GB | Programming |
| llama2 | 7B | Medium | Very High | 4GB | Quality responses |

## Benchmarks

Typical response times (on CPU):
- Orca Mini: 50-100ms per token
- Mistral: 100-200ms per token  
- Llama 2: 200-400ms per token
- (On GPU: 10-50ms per token)

## Recommendations

**For Development**: Mistral or Neural Chat
```bash
ollama pull mistral
```

**For Low Resources**: Orca Mini
```bash
ollama pull orca-mini
```

**For Best Quality**: Llama 2 (13B)
```bash
ollama pull llama2:13b
```

## Check Installed Models

```bash
# List all installed models
curl http://localhost:11434/api/tags
```

## Uninstall Model

```bash
ollama rm mistral
```
