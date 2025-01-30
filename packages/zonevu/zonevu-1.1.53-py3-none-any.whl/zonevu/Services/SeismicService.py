#  Copyright (c) 2024 Ubiterra Corporation. All rights reserved.
#  #
#  This ZoneVu Python SDK software is the property of Ubiterra Corporation.
#  You shall use it only in accordance with the terms of the ZoneVu Service Agreement.
#  #
#  This software is made available on PyPI for download and use. However, it is NOT open source.
#  Unauthorized copying, modification, or distribution of this software is strictly prohibited.
#  #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
#  PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
#  FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#
#
#
#
#
from ..DataModels.Seismic.Fault import Fault, FaultEntry
from ..DataModels.Seismic.SeisHorizon import SeisHorizon
from ..DataModels.Seismic.SeismicSurvey import SeismicSurveyEntry, SeismicSurvey, SeismicDataset
from ..DataModels.Seismic.SeismicRegistration import SeismicRegistration
from .Client import Client, ZonevuError
from typing import Tuple, Union, Dict, Optional, Any, List
from ..Services.Storage import AzureCredential, Storage
from azure.storage.blob import BlobServiceClient
from pathlib import Path
import numpy as np


class SeismicService:
    client: Client

    def __init__(self, c: Client):
        self.client = c

    def get_surveys(self, match_token: Optional[str] = None) -> List[SeismicSurveyEntry]:
        """
        Gets a list of seismic surveys whose names start with the provided string token.
        :param match_token: If not provided, all surveys from this zonevu account will be retrieved.
        :return: a list of partially loaded seismic surveys
        """
        url = "seismic/surveys"
        if match_token is not None:
            url += "/%s" % match_token
        items = self.client.get_list(url)
        entries = [SeismicSurveyEntry.from_dict(w) for w in items]
        return entries

    def get_first_named(self, name: str) -> Optional[SeismicSurvey]:
        """
        Get first seismic survey with the specified name, populate it, and return it.
        :param name: name or project to get
        :return: a fully loaded seismic survey
        """
        entries = self.get_surveys(name)
        if len(entries) == 0:
            return None
        surveyEntry = entries[0]
        survey = self.get_survey(surveyEntry.id)
        return survey

    def survey_exists(self, name: str) -> Tuple[bool, int]:
        """
        Determine if a seismic survey with the provided name exists in the users zonevu account.
        :param name:
        :return:
        """
        surveys = self.get_surveys(name)
        exists = len(surveys) > 0
        project_id = surveys[0].id if exists else -1
        return exists, project_id

    def get_survey(self, survey_id: int) -> Optional[SeismicSurvey]:
        """
        Get the seismic survey with the provided system survey id
        :param survey_id:
        :return: a fully loaded seismic survey
        """
        url = "seismic/survey/%s" % survey_id
        item = self.client.get(url)
        project = SeismicSurvey.from_dict(item)
        return project

    def load_survey(self, survey: SeismicSurvey) -> None:
        """
        Fully load the provided partially loaded seismic survey.
        :param survey:
        :return:
        """
        loaded_survey = self.get_survey(survey.id)
        survey.merge_from(loaded_survey)

    def get_registration(self, dataset_id: int) -> SeismicRegistration:
        """
        Get the Segy, coordinate system, and datum for a specified seismic dataset
        :param dataset_id:
        :return: an info data structure
        """
        url = "seismic/registration/%s" % dataset_id
        item = self.client.get(url)
        info = None if item is None else SeismicRegistration.from_dict(item)
        return info

    def get_download_credential(self, dataset: SeismicDataset | int) -> AzureCredential:
        """
        Get a temporary download token for a seismic dataset
        :param dataset: the specified seismic dataset
        :return: A temporary download token
        """
        dataset_id = dataset if isinstance(dataset, int) else dataset.id
        url = f'seismic/dataset/downloadtoken/{dataset_id}'
        item = self.client.get(url, None, False)
        cred = AzureCredential.from_dict(item)
        return cred

    def download_dataset(self, dataset: SeismicDataset, directory: Path, filename: Optional[str] = None) -> None:
        """
        Download a SEGY seismic dataset
        :param dataset: the specified seismic dataset
        :param directory: path for output 3D seismic SEGY file.
        :param filename: optional filename for output volume SEGY file. If not provided, the original SEGY file name is used.
        :return:
        """
        cred = self.get_download_credential(dataset)
        blob_svc = BlobServiceClient(account_url=cred.url, credential=cred.token)
        client = blob_svc.get_blob_client(container=cred.container, blob=cred.path)

        exists = client.exists()
        if exists:
            try:
                output_path = directory / filename if filename else directory / dataset.segy_filename
                with open(output_path, 'wb') as output_file:
                    total_bytes = 0
                    for chunk in client.download_blob().chunks():
                        total_bytes += len(chunk)
                        output_file.write(chunk)
                        percent_downloaded = round(100 * total_bytes / (1024 * 1024 * dataset.size))
                        print('%s%% downloaded' % percent_downloaded)
            except ZonevuError as err:
                print('Download of the requested seismic dataset "%s" failed because.' % err.message)
                raise err
        else:
            print('The requested seismic dataset "%s" does not exist.' % dataset.name)

    def get_faults(self, survey: SeismicSurvey | SeismicSurveyEntry) -> List[Fault]:
        """
        Get a list of faults for a seismic survey.
        :param survey:
        :return:
        """
        url = f'seismic/faults/{survey.id}'
        items = self.client.get_list(url)
        surveys = [Fault.from_dict(w) for w in items]
        return surveys

    def get_fault(self, fault: int | FaultEntry) -> Optional[Fault]:
        """
        Get a list of faults for a seismic survey.
        :param fault: fault system id or fault entry
        :return:
        """
        fault_id = fault.id if isinstance(fault, FaultEntry) else fault
        url = f'seismic/fault/{fault_id}'
        item = self.client.get(url, None, True)
        instance = Fault.from_dict(item)
        return instance

    def get_horizon_depths(self, horizon: SeisHorizon) -> Optional[np.ndarray]:
        url = "seismic/horizon/%s/zvalues/%s" % ('depth', horizon.id)
        if horizon.geometry is not None:
            float_bytes = self.client.get_data(url)
            horizon.z_values = horizon.geometry.grid_info.load_z_values(float_bytes)
            return horizon.z_values
        else:
            return None




