
Para debuguear script dev_gpt run, se necesita instalar debugpy y correr este comando:

```bash
python -m debugpy --listen 5678  --wait-for-client ./dev_gpt/cli.py run
```

luego hay que hacer attach en el proceso. Para más info: 
https://code.visualstudio.com/docs/python/debugging 