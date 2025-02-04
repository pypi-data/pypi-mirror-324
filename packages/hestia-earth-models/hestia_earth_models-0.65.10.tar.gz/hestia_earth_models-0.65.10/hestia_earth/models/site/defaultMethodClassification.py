"""
Default Method Classification.

When gap-filling `management` node on Site, the
`defaultMethodClassification` and `defaultMethodClassificationDescription` fields become required.
This model will use the first value in the `management` node.
"""
from hestia_earth.models.log import logRequirements, logShouldRun
from . import MODEL

REQUIREMENTS = {
    "Site": {
        "management": [{"@type": "Management", "methodClassification": ""}]
    }
}
RETURNS = {
    "The methodClassification as a `string`": ""
}
MODEL_KEY = 'defaultMethodClassification'


def _should_run(site: dict):
    methodClassification = next((n.get('methodClassification') for n in site.get('management', [])), None)

    logRequirements(site, model=MODEL, model_key=MODEL_KEY,
                    methodClassification=methodClassification)

    should_run = all([methodClassification])
    logShouldRun(site, MODEL, None, should_run, model_key=MODEL_KEY)
    return should_run, methodClassification


def run(site: dict):
    should_run, value = _should_run(site)
    return value
