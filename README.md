# Simple Todo Api
## Run
1. Create .env like .env.example  
2. run docker-compose
```bash
docker-compose up --build
```

## Dev

### Test

#### Install

```bash
pip install pytest pytest-asyncio httpx
```

#### Run

```bash
pytest ./app
```

### Mypy checking

#### Install

```bash
pip install mypy
```

#### Run

```bash
mypy ./app
```

### Black formatting
```bash
pip install black
```

#### Run

```bash
black ./app
```
