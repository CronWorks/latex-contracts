# /usr/bin/env python

from latex_contracts.Contract import Contract, Person
from latex_python.JinjaBase import Money
from py_base.PySystem import PySystem

class RentalApplication(Contract):

    showInitialsBox = False
    applicant = None
    
    title = 'Rental Application'
    subtitle = "This document is an Application for Occupancy of a residential property."
    lessorNames = 'the owner(s) or their agents'
    agencyShortName = 'E-Renter USA'
    agencyContactInformation = '''E-Renter USA Ltd.\\\\
                                  4200 Meridian St. Suite 208\\\\
                                  Bellingham, WA 98226\\\\
                                  Toll-Free: 877 332 0078\\\\
                                  support@e-renter.com'''
    applicationFee = Money(35.00)

    def getSigningPeople(self):
        if self.applicant:
            return [self.applicant]
        return [Person(name='Applicant',
                       address='',
                       phone='',
                       email='')]

