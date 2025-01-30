"""Component Link"""

# Copyright (C) 2022-2024 CSIRO
# Australia Telescope National Facility (ATNF)
# Commonwealth Scientific and Industrial Research Organisation (CSIRO)
# PO Box 76, Epping NSW 1710, Australia
# atnf-enquiries@csiro.au

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = "Matt Austin <matt.austin@csiro.au>"

__copyright__ = "Copyright 2022-2024 CSIRO"

__license__ = "Apache-2.0"

__title__ = "clink"

__url__ = "https://bitbucket.csiro.au/projects/ASKAPSDP/repos/clink/"

try:
    import importlib.metadata

    __version__ = importlib.metadata.version("clink")

except ImportError:
    import pkg_resources

    __version__ = pkg_resources.get_distribution("clink").version
