def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


def test_forms(cldf_dataset):
    assert len(list(cldf_dataset["FormTable"])) == 64289
    assert any(f["Form"] == "lume" for f in cldf_dataset["FormTable"])


def test_parameters(cldf_dataset):
    assert len(list(cldf_dataset["ParameterTable"])) == 1814


def test_languages(cldf_sqlite_database):
    assert cldf_sqlite_database.query('select count(*) from languagetable')[0][0] == 41
