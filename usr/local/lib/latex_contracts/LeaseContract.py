# /usr/bin/env python

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


from latex_python.JinjaBase import JsonSerializable, Money, Percent
from Contract import Contract, Person

class Lessor(Person):
    pass  # _required & __init__ are the same

class Tenant(Person):
    def __init__(self, **kwargs):
        self.forwardingAddress = ''
        self.forwardingCityStateZip = ''
        self.forwardingPhoneNumber = ''
        super(Tenant, self).__init__(**kwargs)

class Occupant(Person):
    pass # _required & __init__ are the same

ELEMENT_LABELS = {'appliances': 'Appliances',
                  'cleanliness':'General Cleanliness',
                  'closet': 'Closet Space',
                  'countertops': 'Sink, Faucet, Counter tops',
                  'cupboards':'Cupboards, Drawers',
                  'electrical': 'Lights, Outlets',
                  'electricMeter': 'Electric Meter Reading',
                  'furniture': 'Any furniture owned by Lessor',
                  'gasMeter': 'Gas Meter Reading',
                  'heatingOil': 'Heating Oil Level',
                  'shower': 'Shower',
                  'smokeDetectors': 'List any inoperable smoke detectors',
                  'toilet': 'Toilet',
                  'walls': 'Walls, Floors, Windows, Blinds',
                  'washer': 'Washer/Dryer',
                  'waterMeter': 'Water Meter Reading',
                  }

class SubjectToInspection(JsonSerializable):
    _inspectionItems = []  # items to attach to the room (subclass as appropriate)
    _moveInConditions = {}
    _moveOutConditions = {}

    def setCondition(self, itemId, moveInOrOut, condition):
        conditionDict = getattr(self, '_%sConditions' % moveInOrOut, {})
        if not conditionDict:
            setattr(self, '_%sConditions' % moveInOrOut, conditionDict)
        conditionDict[itemId] = condition

    def getConditionsTuples(self, moveInOrOut):
        conditionDict = getattr(self, '_%sConditions' % moveInOrOut, {})
        resultDict = {}
        for itemId in sorted(self._inspectionItems):
            label = ELEMENT_LABELS[itemId]
            condition = getattr(conditionDict, itemId, '')
            resultDict[label] = condition
        return [(label, resultDict[label]) for label in sorted(resultDict.keys())]

class Room(SubjectToInspection):
    _required = ['label']
    def __init__(self, label=None, **kwargs):
        if label != None:
            kwargs['label'] = label  # shortcut for instantiation syntax
        else:
            kwargs['label'] = ''
        super(Room, self).__init__(**kwargs)

    def __str__(self):
        return '%s %s' % (self.label, self.__class__.__name__.strip())

class Kitchen(Room):
    _inspectionItems = ['cleanliness',
                        'countertops',
                        'cupboards',
                        'electrical',
                        'walls']

class Bedroom(Room):
    _inspectionItems = ['cleanliness',
                  'closet',
                  'electrical',
                  'walls']

class Bathroom(Room):
    _inspectionItems = ['cleanliness',
                        'countertops',
                        'electrical',
                        'shower',
                        'toilet',
                        'walls']

class Property(SubjectToInspection):
    _required = ['address',
                 'county',
                 'rent',
                 'deposit',
                 'occupantLimit']

    # customize per property
    _inspectionItems = ['smokeDetectors',
                        'waterMeter',
                        'electricMeter',
                        'gasMeter',
                        'heatingOil']

    def __init__(self, **kwargs):
        self.clauses = {}  # format: {'sectionName': [clause list], ...}
        self.applicationFee = Money(35)
        self.depositNonRefundable = Money(250)
        self.furnished = False
        self.rooms = []
        self.roommateOnly = False
        self.tenantMaintainsYard = True
        self.utilitiesIncluded = []
        super(Property, self).__init__(**kwargs)

class LeaseContract(Contract):
    def __init__(self, searchPath=None, signatureFilePath=None, **kwargs):
        self.lessors = []
        self.occupants = []
        self.tenants = []
        self.property = None

        self.leaseStartDate = None
        self.leaseEndDate = None
        self.monthToMonth = False
        self.renewal = False
        self.signSections = []

        self.moveInTime = '2:00pm'
        self.moveOutTime = '12:00pm (noon)'
        self.administrativeGracePeriodDays = 7
        self.gracePeriodDays = 5
        self.dailyLatePenalty = Money(25)
        self.latePenaltyLimitPercent = Percent(10)
        self.bouncedCheckPenalty = Money(50)

        super(LeaseContract, self).__init__(searchPath, signatureFilePath, **kwargs)

        self.title = 'Lease/Rental Agreement'
        self.subtitle = "This document is a Lease Agreement (``Agreement'') between Lessor and Tenant for occupation of a residential property."

    def getSigningPeople(self):
        return self.tenants + self.lessors

    def multipleTenants(self):
        return len(self.tenants) + len(self.occupants) > 1

    def getNumberOfFooterRows(self):
        numberOfInitialsRows = max(len(self.lessors), len(self.tenants))
        return 2 + numberOfInitialsRows  # 2 for "initials:" label and "page x of y"

    def getInspectionFormContent(self, moveInOrOut):
        # \newcommand{\getInspectionFormContent}[1]{% format: \getInspectionFormContent{moveIn or moveOut}
        result = []
        for room in self.property.rooms:
            result += self.getInspectionContent(str(room), room, moveInOrOut)

        result += self.getInspectionContent('General', self.property, moveInOrOut)
        return '\n'.join(result)

    def getInspectionContent(self, label, thingToInspect, moveInOrOut):
        result = ['\\subsection{%s}' % label]
        for (label, condition) in thingToInspect.getConditionsTuples(moveInOrOut):
            result.append('\\formLine[%s]{%s}' % (condition, label))
        return result

    def generate(self, outputFilename, system, variables={}):
        # override default clauses with property's custom clauses
        for sectionName in self.property.clauses:
            for clause in self.property.clauses[sectionName]:
                self.addClause(sectionName, clause)
        super(LeaseContract, self).generate(outputFilename, system, variables)

