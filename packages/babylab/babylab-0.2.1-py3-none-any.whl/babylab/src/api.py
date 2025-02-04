#!/usr/bin/env python

"""
Functions to interact with the REDCap API.
"""

import json
import zipfile
import os
import re
import datetime
from dataclasses import dataclass
from collections import OrderedDict
import requests
from dateutil import relativedelta
import pandas as pd


@dataclass
class RecordList:
    """List of records"""

    records: dict

    def to_df(self) -> pd.DataFrame:
        """Transform a dictionary dataset to a Pandas DataFrame.
        Returns:
            pd.DataFrame: Tabular dataset.
        """
        db_list = []
        for v in self.records.values():
            d = pd.DataFrame(v.data.items())
            d = d.set_index([0])
            db_list.append(d.transpose())
        df = pd.concat(db_list)
        df.index = pd.Index(df[df.columns[0]])
        df = df[df.columns[1:]]
        return df


class Participant:
    """Participant in database"""

    def __init__(self, data, apt: RecordList = None, que: RecordList = None):
        data = {
            re.sub("participant_", "", k): v
            for k, v in data.items()
            if k.startswith("participant_") or k == "record_id"
        }
        self.record_id = data["record_id"]
        self.data = data
        self.appointments = apt
        self.questionnaires = que

    def __repr__(self):
        """Print class in console.

        Returns:
            str: Description to print in console.
        """
        n_apt = 0 if self.appointments is None else len(self.appointments.records)
        n_que = 0 if self.questionnaires is None else len(self.questionnaires.records)
        return f"Participant {self.record_id}: {n_apt} appointments, {n_que} questionnaires"  # pylint: disable=line-too-long

    def __str__(self):
        """Return class description as string.

        Returns:
            str: Description of class.
        """
        n_apt = 0 if self.appointments is None else len(self.appointments.records)
        n_que = 0 if self.questionnaires is None else len(self.questionnaires.records)
        return f"Participant {self.record_id}: {n_apt} appointments, {n_que} questionnaires"  # pylint: disable=line-too-long


class Appointment:
    """Appointment in database"""

    def __init__(self, data):
        data = {
            re.sub("appointment_", "", k): v
            for k, v in data.items()
            if k.startswith("appointment_")
            or k in ["record_id", "redcap_repeat_instance"]
        }
        self.record_id = data["record_id"]
        self.data = data
        self.appointment_id = (
            data["record_id"] + ":" + str(data["redcap_repeat_instance"])
        )
        self.status = data["status"]
        self.date = data["date"]

    def __repr__(self):
        """Print class in console.

        Returns:
            str: Description to print in console.
        """
        return f"Appointment {self.appointment_id}, participant {self.record_id}, {self.date}, {self.status}"  # pylint: disable=line-too-long

    def __str__(self):
        """Return class description as string.

        Returns:
            str: Description of class.
        """
        return f"Appointment {self.appointment_id}, participant {self.record_id}, {self.date}, {self.status}"  # pylint: disable=line-too-long


class Questionnaire:
    """Language questionnaire in database"""

    def __init__(self, data):
        data = {
            re.sub("language_", "", k): v
            for k, v in data.items()
            if k.startswith("language_") or k in ["record_id", "redcap_repeat_instance"]
        }
        self.record_id = data["record_id"]
        self.questionnaire_id = (
            data["record_id"] + ":" + str(data["redcap_repeat_instance"])
        )
        self.isestimated = data["isestimated"]
        self.data = data
        for i in range(1, 5):
            l = f"lang{i}_exp"
            self.data[l] = int(self.data[l]) if self.data[l] else 0

    def __repr__(self):
        """Print class in console.

        Returns:
            str: Description to print in console.
        """
        return (
            f" Language questionnaire {self.questionnaire_id} from participant {self.record_id}"  # pylint: disable=no-member
            + f"\n- L1 ({self.data['lang1']}) = {self.data['lang1_exp']}%"
            + f"\n- L2 ({self.data['lang2']}) = {self.data['lang2_exp']}%"
            + f"\n- L3 ({self.data['lang3']}) = {self.data['lang3_exp']}%"
            + f"\n- L4 ({self.data['lang4']}) = {self.data['lang4_exp']}%"
        )  # pylint: disable=line-too-long

    def __str__(self):
        """Return class description as string.

        Returns:
            str: Description of class.
        """
        return (
            f" Language questionnaire {self.questionnaire_id} from participant {self.record_id}"  # pylint: disable=no-member
            + f"\n- L1 ({self.data['lang1']}) = {self.data['lang1_exp']}%"
            + f"\n- L2 ({self.data['lang2']}) = {self.data['lang2_exp']}%"
            + f"\n- L3 ({self.data['lang3']}) = {self.data['lang3_exp']}%"
            + f"\n- L4 ({self.data['lang4']}) = {self.data['lang4_exp']}%"
        )  # pylint: disable=line-too-long


class BadTokenException(Exception):
    """If token is ill-formed."""


def post_request(
    fields: dict,
    token: str,
    timeout: int = (5, 10),
) -> dict:
    """Make a POST request to the REDCap database.

    Args:
        fields (dict): Fields to retrieve.
        token (str): API token.
        timeout (int, optional): Timeout of HTTP request in seconds. Defaults to 10.

    Raises:
        requests.exceptions.HTTPError: If HTTP request fails.
        BadTokenException: If API token contains non-alphanumeric characters.

    Returns:
        dict: HTTP request response in JSON format.
    """
    fields = OrderedDict(fields)
    fields["token"] = token
    fields.move_to_end("token", last=False)

    try:
        if not token.isalnum():
            raise BadTokenException("Token contains non-alphanumeric characters")
        r = requests.post(
            "https://apps.sjdhospitalbarcelona.org/redcap/api/",
            data=fields,
            timeout=timeout,
        )
        r.raise_for_status()
        return r
    except requests.exceptions.HTTPError as e:
        print(f"{e}:\n{re.sub('<.*?>', '', r.text)}")
    except BadTokenException:
        print("Token contains non-alphanumeric characters")
    return None


def get_redcap_version(**kwargs) -> str:
    """Get REDCap version.
    Args:
        **kwargs: Arguments passed to ``post_request``.
    Returns:
        str: REDCAp version number.
    """
    fields = {
        "content": "version",
    }
    r = post_request(fields=fields, **kwargs)
    if r:
        return r.content.decode("utf-8")
    return None


def get_data_dict(**kwargs):
    """Get data dictionaries for categorical variables

    Returns:
        **kwargs: Additional arguments passed tp ``post_request``.
    """
    items = [
        "participant_sex",
        "participant_birth_type",
        "participant_hearing",
        "participant_source",
        "appointment_study",
        "appointment_status",
        "language_lang1",
        "language_lang2",
        "language_lang3",
        "language_lang4",
    ]
    fields = {
        "content": "metadata",
        "format": "json",
        "returnFormat": "json",
    }

    for idx, i in enumerate(items):
        fields[f"fields[{idx}]"] = i
    r = json.loads(post_request(fields=fields, **kwargs).text)
    items_ordered = [i["field_name"] for i in r]
    dicts = {}
    for k, v in zip(items_ordered, r):
        options = v["select_choices_or_calculations"].split("|")
        options_parsed = {}
        for o in options:
            x = o.split(", ")
            options_parsed[x[0].strip()] = x[1].strip()
        dicts[k] = options_parsed
    return dicts


def datetimes_to_strings(data: dict):
    """Return formatted datatimes as strings following the ISO 8061 date format.

    It first tries to format the date as Y-m-d H:M. If error, it assumes the Y-m-d H:M:S is due and tries to format it accordingly.

    Args:
        data (dict): Dictionary that may contain datetimes.

    Returns:
        dict: Dictionary with datetimes formatted as strings.
    """  # pylint: disable=line-too-long
    for k, v in data.items():
        if isinstance(v, datetime.datetime):
            data[k] = datetime.datetime.strftime(v, "%Y-%m-%d %H:%M:%S")
            if not v.second:
                data[k] = datetime.datetime.strftime(v, "%Y-%m-%d %H:%M")
    return data


def get_records(record_id: str | list = None, **kwargs):
    """Return records as JSON.

    Args:
        kwargs (str): Additional arguments passed to ``post_request``.

    Returns:
        dict: REDCap records in JSON format.
    """
    fields = {
        "content": "record",
        "format": "json",
        "type": "flat",
    }

    if record_id:
        fields["records[0]"] = record_id
        if isinstance(record_id, list):
            for r in record_id:
                fields[f"records[{record_id}]"] = r

    records = post_request(fields=fields, **kwargs).json()
    records = [datetimes_to_strings(r) for r in records]
    return records


def get_participant(ppt_id: str, **kwargs):
    """Get participant record.

    Args:
        ppt_id: ID of participant (record_id).
        **kwargs: Additional arguments passed to ``post_request``

    Returns:
        api.Participant: Participant object.
    """
    fields = {
        "content": "record",
        "action": "export",
        "format": "json",
        "type": "flat",
        "csvDelimiter": "",
        "records[0]": ppt_id,
        "rawOrLabel": "raw",
        "rawOrLabelHeaders": "raw",
        "exportCheckboxLabel": "false",
        "exportSurveyFields": "false",
        "exportDataAccessGroups": "false",
        "returnFormat": "json",
    }
    for i, f in enumerate(["participants", "appointments", "language"]):
        fields[f"forms[{i}]"] = f
    recs = post_request(fields, **kwargs).json()
    apt = {}
    que = {}
    for r in recs:
        repeat_id = f"{str(r['record_id'])}:{str(r['redcap_repeat_instance'])}"
        form = r["redcap_repeat_instrument"]
        if form == "appointments":
            apt[repeat_id] = Appointment(r)
        if form == "language":
            que[repeat_id] = Questionnaire(r)
    ppt = Participant(recs[0], apt=RecordList(apt), que=RecordList(que))
    return ppt


def add_participant(data: dict, modifying: bool = False, **kwargs):
    """Add new participant to REDCap database.

    Args:
        data (dict): Participant data.
        modifying (bool, optional): Modifying existent participant?
        *kwargs: Additional arguments passed to ``post_request``.
    """
    fields = {
        "content": "record",
        "action": "import",
        "format": "json",
        "type": "flat",
        "overwriteBehavior": "normal" if modifying else "overwrite",
        "forceAutoNumber": "false" if modifying else "true",
        "data": f"[{json.dumps(datetimes_to_strings(data))}]",
    }
    return post_request(fields=fields, **kwargs)


def delete_participant(data: dict, **kwargs):
    """Delete participant from REDCap database.

    Args:
        data (dict): Participant data.
        modifying (bool, optional): Modifying existent participant?
        *kwargs: Additional arguments passed to ``post_request``.
    """
    fields = {
        "content": "record",
        "action": "delete",
        "returnFormat": "json",
        "instrument": "",
        "records[0]": f"{data['record_id']}",
    }
    return post_request(fields=fields, **kwargs)


def add_appointment(data: dict, **kwargs):
    """Add new appointment to REDCap database.

    Args:
        record_id (dict): ID of participant.
        data (dict): Appointment data.
        *kwargs: Additional arguments passed to ``post_request``.
    """
    fields = {
        "content": "record",
        "action": "import",
        "format": "json",
        "type": "flat",
        "overwriteBehavior": "overwrite",
        "forceAutoNumber": "false",
        "data": f"[{json.dumps(datetimes_to_strings(data))}]",
    }
    return post_request(fields=fields, **kwargs)


def delete_appointment(data: dict, **kwargs):
    """Delete appointment from REDCap database.

    Args:
        data (dict): Participant data.
        modifying (bool, optional): Modifying existent participant?
        *kwargs: Additional arguments passed to ``post_request``.
    """
    fields = {
        "content": "record",
        "action": "delete",
        "returnFormat": "json",
        "instrument": "appointments",
        "repeat_instance": int(data["redcap_repeat_instance"]),
        f"records[{data['record_id']}]": f"{data['record_id']}",
    }
    return post_request(fields=fields, **kwargs)


def add_questionnaire(data: dict, **kwargs):
    """Add new questionnaire to REDCap database.

    Args:
        data (dict): Questionnaire data.
        *kwargs: Additional arguments passed to ``post_request``.
    """
    fields = {
        "content": "record",
        "action": "import",
        "format": "json",
        "type": "flat",
        "overwriteBehavior": "overwrite",
        "forceAutoNumber": "false",
        "data": f"[{json.dumps(datetimes_to_strings(data))}]",
    }

    return post_request(fields=fields, **kwargs)


def delete_questionnaire(data: dict, **kwargs):
    """Delete questionnaire from REDCap database.

    Args:
        data (dict): Participant data.
        modifying (bool, optional): Modifying existent participant?
        *kwargs: Additional arguments passed to ``post_request``.
    """
    fields = {
        "content": "record",
        "action": "delete",
        "returnFormat": "json",
        "instrument": "language",
        "repeat_instance": int(data["redcap_repeat_instance"]),
        f"records[{data['record_id']}]": f"{data['record_id']}",
    }
    return post_request(fields=fields, **kwargs)


def redcap_backup(dirpath: str = "tmp", **kwargs) -> dict:
    """Download a backup of the REDCap database

    Args:
        dirpath (str, optional): Output directory. Defaults to "tmp".

    Returns:
        dict: A dictionary with the key data and metadata of the project.
    """
    project = json.loads(
        post_request(
            fields={"content": "project", "format": "json", "returnFormat": "json"},
            **kwargs,
        ).text
    )
    fields = json.loads(
        post_request(
            fields={
                "content": "metadata",
                "format": "json",
                "returnFormat": "json",
            },
            **kwargs,
        ).text
    )
    instruments = json.loads(
        post_request(
            fields={"content": "instrument", "format": "json", "returnFormat": "json"},
            **kwargs,
        ).text
    )
    records = [datetimes_to_strings(r) for r in get_records(**kwargs)]
    backup = {
        "project": project,
        "instruments": instruments,
        "fields": fields,
        "records": records,
    }
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    for k, v in backup.items():
        fpath = os.path.join(dirpath, k + ".json")
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(v, f)
    file = (
        "backup_"
        + datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d-%H-%M-%S")
        + ".zip"
    )
    file = os.path.join(dirpath, file)
    for root, _, files in os.walk(dirpath, topdown=False):
        with zipfile.ZipFile(file, "w", zipfile.ZIP_DEFLATED) as z:
            for f in files:
                z.write(os.path.join(root, f))

    return file


class Records:
    """REDCap records"""

    def __init__(self, record_id: str | list = None, **kwargs):

        records = get_records(record_id, **kwargs)
        participants = {}
        appointments = {}
        questionnaires = {}
        for r in records:
            if r["redcap_repeat_instance"] and r["appointment_status"]:
                r["appointment_id"] = (
                    r["record_id"] + ":" + str(r["redcap_repeat_instance"])
                )
                appointments[r["appointment_id"]] = Appointment(r)
            if r["redcap_repeat_instance"] and r["language_lang1"]:
                r["questionnaire_id"] = (
                    r["record_id"] + ":" + str(r["redcap_repeat_instance"])
                )
                questionnaires[r["questionnaire_id"]] = Questionnaire(r)
            if not r["redcap_repeat_instrument"]:
                participants[r["record_id"]] = Participant(r)

        # add appointments and questionnaires to each participant
        for p, v in participants.items():
            apps = {k: v for k, v in appointments.items() if v.record_id == p}
            v.appointments = RecordList(apps)
            ques = {k: v for k, v in questionnaires.items() if v.record_id == p}
            v.questionnaires = RecordList(ques)

        self.participants = RecordList(participants)
        self.appointments = RecordList(appointments)
        self.questionnaires = RecordList(questionnaires)

    def __repr__(self):
        """Print class in console.

        Returns:
            str: Description to print in console.
        """
        return (
            "REDCap database:"
            + f"\n- {len(self.participants.records)} participants"
            + f"\n- {len(self.appointments.records)} appointments"
            + f"\n- {len(self.questionnaires.records)} language questionnaires"  # pylint: disable=line-too-long
        )

    def __str__(self):
        """Return class description as string.

        Returns:
            str: Description of class.
        """
        return (
            "REDCap database:"
            + f"\n- {len(self.participants.records)} participants"
            + f"\n- {len(self.appointments.records)} appointments"
            + f"\n- {len(self.questionnaires.records)} language questionnaires"  # pylint: disable=line-too-long
        )

    def update_record(self, record_id: str, record_type: str, **kwargs):
        """Fetch appointment information from REDCap database and updated Records.

        Args:
            record_id (str): ID of record.
            record_type (str): Type of record. Must be one of "participant", "appointment" or "questionnaire"
            **kwargs: Additional arguments passed to ``post_request``.

        Raises:
            ValueError: If `record_type` is not one of "participant", "appointment", "questionnaire".
        """  # pylint: disable=line-too-long
        if not record_type in ["participant", "appointment", "questionnaire"]:
            raise ValueError(
                "`record_type` must be one of 'participant', 'appointment', 'questionnaire'"
            )

        data = {
            "content": "record",
            "action": "export",
            "format": "json",
            "type": "flat",
            "csvDelimiter": "",
            "records[0]": record_id,
            "forms[0]": "participants",
            "rawOrLabel": "raw",
            "rawOrLabelHeaders": "raw",
            "exportCheckboxLabel": "false",
            "exportSurveyFields": "false",
            "exportDataAccessGroups": "false",
            "returnFormat": "json",
        }

        if record_type != "participant":
            ppt_id, repeat_id = record_id.split(":")
            data["records[0]"] = int(ppt_id)
            data["redcap_repeat_instance"] = repeat_id
            data["forms[1]"] = "appointments"
        if record_type == "questionnaire":
            data["forms[1]"] = "languages"

        r = post_request(data, **kwargs).json()
        if record_type == "participant":
            self.participants.records[record_id] = Participant(r)
        elif record_type == "appointment":
            r[1]["record_id"] = r[0]["record_id"]
            self.appointments.records[record_id] = Appointment(r[1])
        else:
            r[1]["record_id"] = r[0]["record_id"]
            self.questionnaires.records[record_id] = Questionnaire(r[1])


def get_age(
    birth_date: str | datetime.datetime, timestamp: str | datetime.datetime = None
):
    """Estimate age in months and days at some timestamp based on date of birth.

    Args:
        birth_date (str | datetime.datetime): Birthdate as ``datetime`` object or str in "Y-m-d" format. Defaults to current date (``datetime.today()``).
        timestamp (str | datetime.datetime, optional): Time for which the age is calculated. Defaults to None.

    Returns:
        list[int]: Age in months and days.
    """  # pylint: disable=line-too-long
    if timestamp is None:
        timestamp = datetime.datetime.today()
    if isinstance(timestamp, str):
        timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d")
    if isinstance(birth_date, str):
        birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d")
    delta = relativedelta.relativedelta(timestamp, birth_date)
    return [delta.months + (delta.years * 12), delta.days]


def get_birth_date(age: str, timestamp: str | datetime.datetime = None):
    """Calculate date of birth based on age at some timestamp.

    Args:
        age (str): Age in months and days (``m:d`` format) at the timestamp.
        timestamp (str | datetime, optional): Time at which age was calculated. Defaults to ``datetime.today()``.

    Returns:
        _type_: _description_
    """  # pylint: disable=line-too-long
    if timestamp is None:
        timestamp = datetime.datetime.today()
    if not isinstance(timestamp, datetime.datetime):
        timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d")
    age_parsed = age.split(":")
    days_diff = int(float(age_parsed[0]) * 30.437 + float(age_parsed[1]))
    return timestamp - relativedelta.relativedelta(days=days_diff)
