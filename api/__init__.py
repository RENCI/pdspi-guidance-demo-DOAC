import os
import requests

from api.utils import generate_time_series_data


pds_host = os.getenv("PDS_HOST", "localhost")
pds_port = os.getenv("PDS_PORT", "8080")
pds_version = os.getenv("PDS_VERSION", "v1")

config = {
    "title": "Guidance demo DOAC plugin",
    "piid": "pdspi-guidance-demo-DOAC",
    "pluginType": "g",
    "settingsDefaults": {
        "pluginSelectors": [ {
            "title": "Drug",
            "id": "dosing.rxCUI",
            "selectorValue": {
                "value": "rxCUI:1596450",
                "title": "Gentamicin"
            }
        },
        {
            "title": "Drug",
            "id": "dosing.rxCUI",
            "selectorValue": {
                "value":"rxCUI:1114195"
            }
        }  ],
        "modelParameters": [
        {
         "id": "current-time",
         "parameterDescription": "Compute variables relevant to this timestamp.",
         "parameterValue": { "value": "2019-09-20T00:00:01Z" },
         "legalValues": { "type": "string", "format": "time-stamp" }
        }],
        "patientVariables": [ {
            "id": "LOINC:30525-0",
            "title": "Age",
            "variableDescription": "Fractional age of patient relative to [current-time].",
            "legalValues": { "type": "number", "minimum": "0" }
        }, {
            "id": "1114195.extant",
            "title": "Rivoroxaban, extant",
            "variableDescription": "Dosing of rivoroxaban, based on the finding of any rxnorm codes found on the record that map to rxCUI 1114195.",
            "legalValues": { "type": "number" }
        }, {
            "id": "1114195.intensity",
            "title": "Rivoroxaban, dosage",
            "variableDescription": "Dosing of rivoroxaban.",
            "legalValues": { "type": "number", "minimum": 0  }
        }, {
            "id": "HP:0001892.extant.days",
            "title": "Bleeding, days since",
            "variableDescription": "Days since the last bleeding event, relative to current-time. A value < -age means never. Bleeding events are identified by one of 50 ICD10 codes or 42 ICD9 codes.",
            "legalValues": { "type": "number" }
        }, {
            "id": "HP:0000077.extant.boolean",
            "title": "Kidney dysfunction, extant",
            "variableDescription": "If true, then Kidney dysfunction was found in the record for the patient, relative to current-time.",
            "legalValues": { "type": "boolean" }
        }, {
            "id": "1114195.extant.count",
            "title": "Rivoroxaban dosing count",
            "variableDescription": "Number of times patient was dosed with Rivoroxaban.",
            "legalValues": { "type": "number" }
           }
        ]
    }
}


guidance = {
    "piid": "pdspi-guidance-demo-DOAC",
    "patientId": "38",
    "settingsRequested": {
      "timestamp": "2019-12-03T13:41:09.942+00:00",
      "modelParameters": [ {
                            "id": "pdspi-guidance-demo-DOAC:1",
                            "title": "Extended interval nomogram",
                            "parameterDescription": "This calculator uses one of four extended-interval nomograms. Please choose one nomogram.",
                            "parameterValue": { "value": "Hartford" }
                         } 
                       ],
      "patientVariables": [ {
                            "id": "LOINC:30525-0",
                            "title": "Age",
                            "variableValue": {
                            "value": "0.5",
                            "units": "years"
                            },
                            "how": "The value was specified by the end user."
                          }, 
                          {
                            "id": "LOINC:39156-5",
                            "title": "BMI",
                            "variableValue": {
                                            "value": "0.5",
                                            "units": "kg/m^2"
                            },
                            "how": "The value was specified by the end user."
                           } 
                      ]
    }
}


def generate_vis_spec(typeid, x_axis_title, y_axis_title, chart_title, chart_desc):
    json_post_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    vega_spec_input = {
        "typeid": typeid,
        "x_axis_title": x_axis_title,
        "y_axis_title": y_axis_title,
        "chart_title": chart_title,
        "chart_description": chart_desc
    }
    url_str = "http://{}:{}/{}/plugin/tx-vis/vega_spec".format(pds_host, pds_port, pds_version)
    resp = requests.post(url_str, headers=json_post_headers, json=vega_spec_input)
    # resp = requests.post("http://tx-vis:8080/vega_spec", headers=json_post_headers, json=vega_spec_input)
    if resp.status_code == 200:
        return resp.json()
    else:
        return {}


def generate_vis_outputs(age=None, weight=None, bmi=None, dose=None, tau=None, num_cycles=None):
    outputs = [
        {
            "id": "oid-1",
            "name": "Time-series data",
            "description": "Information about time-series data",
            "data": generate_time_series_data(50),
            "specs": [
                generate_vis_spec("line_chart", "X Axis", "Y Axis", "Line chart", "Time-series line chart"),
                generate_vis_spec("area_chart", "X Axis", "Y Axis", "Area chart", "Time-series area chart")
            ]
        }
        
    ]
    return outputs


def get_config():
    return config


def get_guidance(body):
    return guidance
