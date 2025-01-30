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
from typing import List
from ...DataModels.Seismic.Fault import Fault
from ...Zonevu import Zonevu
from ...Services.Client import ZonevuError
from ...Services.Storage import AzureStorage
import json
from pathlib import Path

def main_get_surveys(zonevu: Zonevu):
    seismic_svc = zonevu.seismic_service
    entries = seismic_svc.get_surveys()  # Get all surveys
    print('Listing seismic surveys in zonevu account:')
    for entry in entries:
        survey = seismic_svc.get_survey(entry.id)
        print(f'  - {survey.full_name}, Type = {survey.type}  Num datasets = {len(survey.seismic_datasets)}')
        for dataset in survey.seismic_datasets:
            print(f'      - {dataset.name}, Type = {dataset.dataset_type}, Registered = {dataset.is_registered}')
            info = seismic_svc.get_registration(dataset.id)
            if info is None:
                print('         - No information available')
            else:
                fi = info.file_info
                print(f'         - File size = {fi.file_length / 1000000} MB, Num Traces = {fi.num_traces}')



def main_get_seismicsurvey_info(zonevu: Zonevu, seismic_survey_name: str):
    seismic_svc = zonevu.seismic_service

    print('Getting Seismic Info for seismic survey named "%s"' % seismic_survey_name)
    survey = seismic_svc.get_first_named(seismic_survey_name)
    if survey is None:
        raise ZonevuError.local('Could not locate the seismic survey named %s' % seismic_survey_name)

    volume = survey.seismic_datasets[0]
    print('Getting seismic info for seismic volume named %s' % volume.name)
    info = seismic_svc.get_registration(volume.id)
    info_dict = info.to_dict()
    print(json.dumps(info_dict, indent=3))

    # Get faults
    if len(survey.faults) > 0:
        num_fault_points = 0
        num_fault_segments = 0

        # Get the faults one at a time
        faults: List[Fault] = []
        for fault_entry in survey.faults:
            fault = seismic_svc.get_fault(fault_entry)
            faults.append(fault)

        # Get the faults all at once
        # faults = seismic_svc.get_faults(survey)

        for fault in faults:
            num_fault_segments += len(fault.segments)
            for segment in fault.segments:
                num_fault_points+= len(segment.points)
        print(f'Num faults = {len(faults)}')
        print(f'Num segments = {num_fault_segments}')
        print(f'Num points = {num_fault_points}')

    if len(survey.horizons) > 0:
        horizon = survey.horizons[0]  # Work with first horizon
        grid_info = horizon.geometry.grid_info
        print(f'Info for seismic horizon {horizon.name}')
        print(f'Inlines: {grid_info.inline_range.start} - {grid_info.inline_range.stop}')
        print(f'Crosslines: {grid_info.crossline_range.start} - {grid_info.crossline_range.stop}')
        print (f'Ave depth: {horizon.average_value}')
        depths = seismic_svc.get_horizon_depths(horizon)  # 'depths' is a 2D array of floats with horizon values.
        num_inlines, num_crosslines = depths.shape
        num_values = num_inlines * num_crosslines
        print(f'Num depth values: {num_values}')

    # Get info on first volume
    if len(survey.seismic_datasets) == 0:
        print('That seismic survey has no volumes')
        return

    # Download SEGY volume
    credential = seismic_svc.get_download_credential(volume)
    azure = AzureStorage(credential)
    file_path = Path(f'c:/delme/seismic/{volume.segy_filename}')
    print('Downloading SEGY file: ')
    azure.download_to_file(file_path, True)
    print()
    print('Download Complete')


    print("Execution was successful")

