# **Genetic Algorithm in Flexible Flow Shop Scheduling Problem**

## Configurations
<p align="left">
 <a href=""><img src="https://img.shields.io/badge/python-3.9-aff.svg"></a>
</p>

### Run locally
- Create conda environment, note that python version should be <span style="color:#9BB8ED;">Python 3.9</span>
```
conda create --name genetic_al python=3.9
conda activate genetic_al
```

- Install required packages

```
pip install -r requirements.txt --no-cache-dir
```

## **Pipeline**

<div align="center"> Main Pipeline</div>

```zsh
python main.py > log_python.txt
```

The best result is stored inside [log file](log_python.txt)

According to the last running:

| Generation | Best Objective |
-|-
1|40.81999999999999
2|40.81999999999999
3|40.81999999999999
4|40.81999999999999
5|32.00999999999999
6|32.00999999999999
7|32.00999999999999
8|32.00999999999999
...|...
20|23.870000000000005
21|23.870000000000005
22|23.870000000000005
23|23.870000000000005
24|23.870000000000005

And the solution to get `objective` equal to `23.870000000000005` is:

```txt
5 11 20 4 2 7 10 16 14 9 12 6 3 18 1 17 19 13 15 8
```

## Reference
- ...
