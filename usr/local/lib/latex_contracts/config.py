# Copyright 2012, 2013, 2014 J. Luke Scott
# This file is part of latex-contracts.

# latex-contracts is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# latex-contracts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with latex-contracts.  If not, see <http://www.gnu.org/licenses/>.


from latex_contracts.Contract import Clause
from latex_contracts.LeaseContract import  LeaseContract, Property, \
    Bedroom, Bathroom, Kitchen, InspectionItem, Lessor, Tenant, Occupant

contractDataTypes = {'LeaseContract':LeaseContract,
                     'Lessor': Lessor,
                     'Tenant': Tenant,
                     'Occupant': Occupant,
                     'Clause': Clause,
                     'Property': Property,
                     'Bedroom': Bedroom,
                     'Bathroom': Bathroom,
                     'Kitchen': Kitchen,
                     'InspectionItem': InspectionItem,
                     }

