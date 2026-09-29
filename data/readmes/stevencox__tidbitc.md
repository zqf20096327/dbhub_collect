# tidbitc

**tidbitc** compiles a yaml definition file into a translator tidbit. 

The config file looks like this:
```
header:
  name: workflow-5
  theme: ananke
  title: What phenotypes are associated with chemical exposure in a cohort?
body:
  - name: Question
    text: |
      This is the biomedical question.
      ![Overview](/thumbnail_JD.jpg)
  - name: Background
    issue_id: 36
    text: |
      ![Background](/thumbnail_JD.jpg)
```

## Install

Install the Hugo website generator. (On OS X, `brew install hugo`).

## Run

Generate the Hugo project from the tidbit configuration.

```python gentidbit.py <config-file>```

Change to the new directory. It will be named after the value of the `name` tag in the config file.

```
cd <tidbit-name>
hugo server -D
```

Then, visit [http://localhost:1313](http://localhost:1313)
