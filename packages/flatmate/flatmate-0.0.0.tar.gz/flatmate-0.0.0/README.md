# flatmate
Your Friendly Data Flattener.  Convert Nested JSON from an API into a List of Single-Depth Dictionaries for Writing to a CSV.

## install
```sh
pip install flatmate
```

## basic usage
```python
# in JSON-compatible format
data = {
  "agency": "GSA",
  "measurementType": {
    "method": "modules"
  },
  "version": "2.0.0",
  "releases": [
    {
      "name": "usasearch",
      "description": "System now maintained in open repo https://github.com/GSA/search-gov.",
      "permissions": {
        "licenses": None,
        "usageType": "governmentWideReuse"
      },
      "tags": [
        "GSA"
      ]
    },
    # ...
  ]
}
```

```python
from flatmate import flatten

# flatten data into a list of flat single-depth dictionaries
flatten(data, start="releases")
[
  {
    "releases.name": "usasearch",
    "releases.description": "System now maintained in open repo https://github.com/GSA/search-gov.",
    "releases.permissions.licenses": "null",
    "releases.permissions.usageType": "governmentWideReuse",
    "releases.tags": "GSA",
    # ...
  },
  # ...
]
```

# advanced usage
coming soon
