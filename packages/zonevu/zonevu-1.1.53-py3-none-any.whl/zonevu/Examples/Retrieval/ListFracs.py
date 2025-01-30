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

from ...Zonevu import Zonevu


def main_list_fracs(zonevu: Zonevu, well_name: str):
    """
    This script will find the named well, and list the fracs on its primary wellbore
    :param zonevu: Zonevu instance
    :param well_name: Name of well to work with
    :return:
    """
    # Get needed Web API services
    print('Listing of fracs for primary wellbore of well "%s"' % well_name)
    well_svc = zonevu.well_service
    well = well_svc.get_first_named(well_name, True)
    if well is None:
        print('Could not find the well named"%s"' % well_name)
        return
    if well.primary_wellbore is None:
        print('Could not find primary wellbore on well')
        return

    completions_svc = zonevu.completions_service
    frac_entries = completions_svc.get_fracs(well.primary_wellbore.id)
    if len(frac_entries) == 0:
        print('There are no fracs on that well')
    else:
        print('Fracs:')
        for frac in frac_entries:
            print('   Frac %s - %s (%s)' % (frac.name, frac.frac_type, frac.id))

    frac_entry = frac_entries[1]
    frac = completions_svc.find_frac(frac_entry.id)
    print('Execution complete')
