#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


from py_base.JobOutput import JobOutput
from py_base.PySystem import PySystem
from latex_python.JinjaBase import Date
from latex_contracts.LeaseContract import LeaseContract, Tenant, Occupant

lease = LeaseContract()

lease.property = Property(address="620 Northeast Finster Avenue",
                          county="Meyer",
                          rent=Money(1505),
                          deposit=Money(1000),
                          rooms=[Bedroom("Main"),
                                 Bathroom("Main"),
                                 Kitchen(),
                                 ],
                          occupantLimit=2,
                          utilitiesIncluded=['Water/Sewer/Garbage'],
                          furnished=True,
                          tenantMaintainsYard=False,
                          )

lease.lessors.append(Lessor(name="Herman S. Muller",
                     address="4544 South Winston, Springfield, ME 12345",
                     phone="+1 234 567 8900",
                     email="herman.muller@emailaddress.com",
                     signatureFilename='SignatureSample.pdf')
                     )

lease.tenants.append(Tenant(name="First Tenant",
                            address="123 Fake Street, Springfield, MO, 12345",
                            phone="123 456 7890",
                            email="first.tenant@gmail.com"))
lease.tenants.append(Tenant(name="Second Tenant",
                            address="321 Fake Street, Springfield, MO, 54321",
                            phone="098 765 4321",
                            email="second.tenant@gmail.com"))
lease.occupants.append(Occupant(name="First Occupant"))
lease.occupants.append(Occupant(name="Second Occupant"))

lease.agreementDate = Date(2013, 7, 30)
lease.leaseStartDate = Date(2013, 3, 1)
lease.leaseEndDate = Date(2014, 3, 1)

lease.monthToMonth = False
lease.renewal = False

lease.signSections = [1, 2, 3, 4]

system = PySystem(JobOutput())
filename = __file__ + '.pdf'
lease.generate(filename, system)

from subprocess import Popen
Popen(['evince', filename])
