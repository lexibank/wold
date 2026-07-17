# Releasing WOLD

Recreate the CLDF:
```shell
cldfbench lexibank.makecldf lexibank_wold.py --glottolog-version v5.3 --clts-version v2.3.0 --concepticon-version v3.4.0
```

```shell
pytest
```

```shell
cldfbench cldfreadme lexibank_wold.py
```

```shell
cldfbench cldfviz.map cldf/ --language-properties Family --out map.svg --format svg --with-ocean --pacific-centered --no-legend --width 10 --padding-top 7 --padding-bottom 7 --language-labels
```
