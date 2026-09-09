# Neurogenetic algorithm for Snake game

<p align="center">
<img width="500" height="491" alt="snake" src="https://github.com/user-attachments/assets/6e18aaf7-6c55-4474-9d1b-e05549b88f0b" />
</p>

# Install
```bash
git clone https://github.com/falcon-oliver/ai_snake.git
cd ai_snake
pip install -r requirements.txt
```


# Usage

Default train and test model. <code>iterations=20 start_population=100</code>
```bash
python3 main.py
```

Save model
```bash
python3 main.py -s ./models/out.pt
```

Load model
```bash
python3 main.py -l ./models/example.pt
```

Play the game
```bash
python3 main.py -t
```

Change iterations
```bash
python3 main.py -i 100
```

Change start population
```bash
python3 main.py -p 200
```
