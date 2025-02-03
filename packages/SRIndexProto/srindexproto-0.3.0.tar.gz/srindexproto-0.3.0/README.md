# SRIndexProto
- Prototype of calculator for Social Relationship Index 

# Use
```bash
$ srindex 

Please read the script and think of people around you carefully.
Please answer the questions faithfully.

You can estimate the Index of overall by calculating average.
and also the Index of case(person) individually.

BUT, PLEASE DO NOT BE SERIOUS.

Results are shown as follows:

--------------------------------- RESULT ----------------------------------------
The importance of each elements you answered: scale of 100
- money: 38.46
- time: 30.77
- emotion: 30.77

The average performance of each elements you answered: scale of 100
- money: 70.00
- time: 55.00
- emotion: 75.00
*The criteria for converting to a score out of 100 are as follows:
point1: 0 | point2: 25 | point3: 50 | point4: 75 | point5: 100

The table of 'Performance' for each case of each element is as follows:
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┓
┃ Case ID ┃ Money ┃ Time ┃ Emotion ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━┩
│ Average │  70.0 │ 55.0 │    75.0 │
│    1    │  75.0 │ 50.0 │    75.0 │
│    2    │  25.0 │ 75.0 │    50.0 │
│    3    │  75.0 │ 50.0 │    75.0 │
│    4    │ 100.0 │ 75.0 │   100.0 │
│    5    │  75.0 │ 25.0 │    75.0 │
└─────────┴───────┴──────┴─────────┘

Totally, the Social Relationship Index is: 66.92

The table of 'Index'(=Importance*Performance) by case is as follows:
┏━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Case ID ┃ Money ┃ Time  ┃ Emotion ┃ Social Relationship Index ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Average │ 26.92 │ 16.92 │  23.08  │           66.92           │
│    1    │ 28.85 │ 15.38 │  23.08  │           67.31           │
│    2    │ 9.62  │ 23.08 │  15.38  │           48.08           │
│    3    │ 28.85 │ 15.38 │  23.08  │           67.31           │
│    4    │ 38.46 │ 23.08 │  30.77  │           92.31           │
│    5    │ 28.85 │ 7.69  │  23.08  │           59.62           │
└─────────┴───────┴───────┴─────────┴───────────────────────────┘
---------------------------------------------------------------------------------

```

## Requirements
```bash
To calculate the Index, you need to collect data of arguments as follows:
- Money: give-and-take between each other
- Time: meetings spent together
- Emotion: contact exchanged with each other
and each arguments is quantified as "Performance", measured by scaling on a 5-point scale

On a scale of 1 to 5, please rate the "Importance" of Money, Time, and Emotion invested in your social relationships, based on your personal values. 

Weight of arguments are calculated by using importance1,2,3 as follows:
- (importance of argument / total) * 100
*total: summation of importance 

The Social Relationship Index is "Weighted Sum" of arguments.
 
In order to produce the Social Relationship Index,
please read carefully the Introduction of index and the criteria for evaluating arguments.   
```

# Development environment setting guide
```bash
# install PDM
# git clone ...
# pdm venv create
$ source .venv/bin/activate
$ pdm install
# $ vi ...


# TEST
$ pdm install
$ pdm test
$ pip install .

$ git add <FILE_NAME>
$ git commit -a
$ git push
$ pdm publish --username __token__ --password $PYPI_TOKEN

View at:
https://pypi.org/project/SRIndexProto/

# PR - Merge
# Tag - Releases
```

### Test
- https://docs.pytest.org/en/stable/
```bash
# $ pdm add -dG test pytest pytest-cov
$ pytest
$ pytest -s
$ pytest --cov
```

### Ref
- https://pdm-project.org/en/latest/
- https://packaging.python.org/en/latest/tutorials/packaging-projects/
- [console_scripts](https://packaging.python.org/en/latest/specifications/entry-points/#entry-points-specification)

