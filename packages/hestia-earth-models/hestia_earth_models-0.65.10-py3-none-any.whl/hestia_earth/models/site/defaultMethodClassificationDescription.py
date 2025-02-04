"""
Default Method Classification Description.

When gap-filling `management` node on Site, the
`defaultMethodClassification` and `defaultMethodClassificationDescription` fields become required.
This model will use the first value in the `management` node.
"""
from hestia_earth.models.log import logRequirements, logShouldRun
from . import MODEL

REQUIREMENTS = {
    "Site": {
        "management": [{"@type": "Management", "methodClassification": "", "methodClassificationDescription": ""}]
    }
}
RETURNS = {
    "The methodClassification as a `string`": ""
}
MODEL_KEY = 'defaultMethodClassificationDescription'


def _should_run(site: dict):
    methodClassificationDescription = next((
        n.get('methodClassificationDescription')
        for n in site.get('management', [])
        if n.get('methodClassification')
    ), None)

    logRequirements(site, model=MODEL, model_key=MODEL_KEY,
                    methodClassificationDescription=methodClassificationDescription)

    should_run = all([methodClassificationDescription])
    logShouldRun(site, MODEL, None, should_run, model_key=MODEL_KEY)
    return should_run, methodClassificationDescription


def run(site: dict):
    should_run, value = _should_run(site)
    return value
